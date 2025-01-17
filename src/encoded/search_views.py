from functools import partial
from pyramid.view import view_config

from encoded.cart_view import CartWithElements
from encoded.genomic_data_service import remote_get
from encoded.genomic_data_service import remote_stream_get
from encoded.genomic_data_service import set_status_and_parse_json
from encoded.genomic_data_service import set_status_and_parse_ndjson
from encoded.genomic_data_service import RNAGET_REPORT_URL
from encoded.genomic_data_service import RNAGET_SEARCH_STREAM_URL
from encoded.searches.caches import cached_fielded_response_factory
from encoded.searches.caches import get_redis_lru_cache
from encoded.searches.caches import make_key_from_request
from encoded.searches.caches import should_cache_search_results
from encoded.searches.defaults import DEFAULT_ITEM_TYPES
from encoded.searches.defaults import DEFAULT_RNA_EXPRESSION_SORT
from encoded.searches.defaults import HOMEPAGE_SEARCH_FACETS
from encoded.searches.defaults import RESERVED_KEYS
from encoded.searches.defaults import TOP_HITS_ITEM_TYPES
from encoded.searches.fields import CartSearchResponseField
from encoded.searches.fields import CartSearchWithFacetsResponseField
from encoded.searches.fields import CartReportWithFacetsResponseField
from encoded.searches.fields import CartMatrixWithFacetsResponseField
from encoded.searches.fields import CartFiltersResponseField
from encoded.searches.fields import ClearFiltersResponseFieldWithCarts
from encoded.searches.fields import RemoteResponseField
from encoded.searches.fields import TypeOnlyClearFiltersResponseFieldWithCarts
from encoded.searches.interfaces import RNA_CLIENT
from encoded.searches.interfaces import RNA_EXPRESSION
from snosearch.decorators import conditional_cache
from snosearch.interfaces import AUDIT_TITLE
from snosearch.interfaces import MATRIX_TITLE
from snosearch.interfaces import REPORT_TITLE
from snosearch.interfaces import SEARCH_TITLE
from snosearch.interfaces import SUMMARY_MATRIX
from snosearch.interfaces import SUMMARY_TITLE
from snosearch.fields import AuditMatrixWithFacetsResponseField
from snosearch.fields import AllResponseField
from snosearch.fields import BasicMatrixWithFacetsResponseField
from snosearch.fields import MissingMatrixWithFacetsResponseField
from snosearch.fields import BasicSearchResponseField
from snosearch.fields import BasicSearchWithFacetsResponseField
from snosearch.fields import BasicSearchWithoutFacetsResponseField
from snosearch.fields import BasicReportWithFacetsResponseField
from snosearch.fields import BasicReportWithoutFacetsResponseField
from snosearch.fields import CachedFacetsResponseField
from snosearch.fields import ClearFiltersResponseField
from snosearch.fields import ColumnsResponseField
from snosearch.fields import ContextResponseField
from snosearch.fields import DebugQueryResponseField
from snosearch.fields import FacetGroupsResponseField
from snosearch.fields import FiltersResponseField
from snosearch.fields import IDResponseField
from snosearch.fields import NotificationResponseField
from snovault.elasticsearch.searches.fields import NonSortableResponseField
from snosearch.fields import RawMatrixWithAggsResponseField
from snosearch.fields import RawSearchWithAggsResponseField
from snosearch.fields import RawTopHitsResponseField
from snosearch.fields import SearchBaseResponseField
from snosearch.fields import SortResponseField
from snosearch.fields import TitleResponseField
from snosearch.fields import TypeOnlyClearFiltersResponseField
from snosearch.fields import TypeResponseField
from snosearch.parsers import ParamsParser
from snosearch.responses import FieldedGeneratorResponse
from snosearch.responses import FieldedResponse

from snovault.elasticsearch.searches.interfaces import SEARCH_CONFIG


def includeme(config):
    config.add_route('search', '/search{slash:/?}')
    config.add_route('series_search', '/series-search{slash:/?}')
    config.add_route('single_cell', '/single-cell{slash:/?}')
    config.add_route('immune-cells', '/immune-cells{slash:/?}')
    config.add_route('encyclopedia', '/encyclopedia{slash:/?}')
    config.add_route('encode_software', '/encode-software{slash:/?}')
    config.add_route('searchv2_raw', '/searchv2_raw{slash:/?}')
    config.add_route('searchv2_quick', '/searchv2_quick{slash:/?}')
    config.add_route('report', '/report{slash:/?}')
    config.add_route('matrixv2_raw', '/matrixv2_raw{slash:/?}')
    config.add_route('matrix', '/matrix{slash:/?}')
    config.add_route('human_donor_matrix', '/human-donor-matrix{slash:/?}')
    config.add_route('reference-epigenome-matrix', '/reference-epigenome-matrix{slash:/?}')
    config.add_route('entex-matrix', '/entex-matrix{slash:/?}')
    config.add_route('brain-matrix', '/brain-matrix{slash:/?}')
    config.add_route('sescc-stem-cell-matrix', '/sescc-stem-cell-matrix{slash:/?}')
    config.add_route('chip-seq-matrix', '/chip-seq-matrix{slash:/?}')
    config.add_route('deeply-profiled-matrix', '/deeply-profiled-matrix{slash:/?}')
    config.add_route('deeply-profiled-uniform-batch-matrix', '/deeply-profiled-uniform-batch-matrix{slash:/?}')
    config.add_route('mouse-development-matrix', '/mouse-development-matrix{slash:/?}')
    config.add_route('encore-matrix', '/encore-matrix{slash:/?}')
    config.add_route('encore-rna-seq-matrix', '/encore-rna-seq-matrix{slash:/?}')
    config.add_route('degron-matrix', 'degron-matrix{slash:/?}')
    config.add_route('summary', '/summary{slash:/?}')
    config.add_route('audit', '/audit{slash:/?}')
    config.add_route('cart-search', '/cart-search{slash:/?}')
    config.add_route('cart-report', '/cart-report{slash:/?}')
    config.add_route('cart-matrix', '/cart-matrix{slash:/?}')
    config.add_route('top-hits-raw', '/top-hits-raw{slash:/?}')
    config.add_route('top-hits', '/top-hits{slash:/?}')
    config.add_route('rnaget-report', '/rnaget-report{slash:/?}')
    config.add_route('search-config-registry', '/search-config-registry{slash:/?}')
    config.add_route('homepage-search', '/homepage-search{slash:/?}')
    config.scan(__name__)


@view_config(route_name='search', request_method='GET', permission='search')
def search(context, request):
    # Note the order of rendering matters for some fields, e.g. AllResponseField and
    # NotificationResponseField depend on results from BasicSearchWithFacetsResponseField.
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title=SEARCH_TITLE
            ),
            TypeResponseField(
                at_type=[SEARCH_TITLE]
            ),
            IDResponseField(),
            ContextResponseField(),
            BasicSearchWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            AllResponseField(),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            ClearFiltersResponseField(),
            ColumnsResponseField(),
            SortResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='series_search', request_method='GET', permission='search')
def series_search(context, request):
    # Note the order of rendering matters for some fields, e.g. AllResponseField and
    # NotificationResponseField depend on results from BasicSearchWithFacetsResponseField.
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title="Series search"
            ),
            TypeResponseField(
                at_type=["SeriesSearch"]
            ),
            IDResponseField(),
            ContextResponseField(),
            BasicSearchWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            AllResponseField(),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            ClearFiltersResponseField(),
            ColumnsResponseField(),
            SortResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='single_cell', request_method='GET', permission='search')
def single_cell(context, request):
    # Note the order of rendering matters for some fields, e.g. AllResponseField and
    # NotificationResponseField depend on results from BasicSearchWithFacetsResponseField.
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title="Single cell"
            ),
            TypeResponseField(
                at_type=["SingleCell"]
            ),
            IDResponseField(),
            ContextResponseField(),
            BasicSearchWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES
            ),
            AllResponseField(),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            ClearFiltersResponseField(),
            ColumnsResponseField(),
            SortResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='encyclopedia', request_method='GET', permission='search')
def encyclopedia(context, request):
    # Note the order of rendering matters for some fields, e.g. AllResponseField and
    # NotificationResponseField depend on results from BasicSearchWithFacetsResponseField.
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title="Encyclopedia"
            ),
            TypeResponseField(
                at_type=["Encyclopedia"]
            ),
            IDResponseField(),
            ContextResponseField(),
            BasicSearchWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES
            ),
            AllResponseField(),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            ClearFiltersResponseField(),
            ColumnsResponseField(),
            SortResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='encode_software', request_method='GET', permission='search')
def encode_software(context, request):
    # Note the order of rendering matters for some fields, e.g. AllResponseField and
    # NotificationResponseField depend on results from BasicSearchWithFacetsResponseField.
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title="Software"
            ),
            TypeResponseField(
                at_type=["EncodeSoftware"]
            ),
            IDResponseField(),
            ContextResponseField(),
            BasicSearchWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            AllResponseField(),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            ClearFiltersResponseField(),
            ColumnsResponseField(),
            SortResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='searchv2_raw', request_method='GET', permission='search')
def searchv2_raw(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            RawSearchWithAggsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            )
        ]
    )
    return fr.render()


@view_config(route_name='searchv2_quick', request_method='GET', permission='search')
def searchv2_quick(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            BasicSearchResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            )
        ]
    )
    return fr.render()


def search_generator(request):
    '''
    For internal use (no view). Like search_quick but returns raw generator
    of search hits in @graph field.
    '''
    fgr = FieldedGeneratorResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            BasicSearchResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            )
        ]
    )
    return fgr.render()


def cart_search_generator(request):
    '''
    For internal use (no view). Like search_quick but returns raw generator
    of cart search hits in @graph field.
    '''
    fgr = FieldedGeneratorResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            CartSearchResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                cart=CartWithElements(request),
                reserved_keys=RESERVED_KEYS,
            )
        ]
    )
    return fgr.render()


def rna_expression_search_generator(request):
    '''
    For internal use (no view). Returns generator of newline-delmited JSON
    results in @graph field.
    '''
    fr = FieldedGeneratorResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            RemoteResponseField(
                how=remote_stream_get,
                where=RNAGET_SEARCH_STREAM_URL,
                then=set_status_and_parse_ndjson,
            ),
        ]
    )
    return fr.render()


@view_config(route_name='report', request_method='GET', permission='search')
def report(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title=REPORT_TITLE
            ),
            TypeResponseField(
                at_type=[REPORT_TITLE]
            ),
            IDResponseField(),
            ContextResponseField(),
            BasicReportWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            AllResponseField(),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            ColumnsResponseField(),
            NonSortableResponseField(),
            SortResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='matrixv2_raw', request_method='GET', permission='search')
def matrixv2_raw(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            RawMatrixWithAggsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            )
        ]
    )
    return fr.render()


@view_config(route_name='matrix', request_method='GET', permission='search')
def matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title=MATRIX_TITLE
            ),
            TypeResponseField(
                at_type=[MATRIX_TITLE]
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            BasicMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='human_donor_matrix', request_method='GET', permission='search')
def human_donor_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Human Donor Matrix'
            ),
            TypeResponseField(
                at_type=['HumanDonorMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            MissingMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='human_donor_matrix',
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='sescc-stem-cell-matrix', request_method='GET', permission='search')
def sescc_stem_cell_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Stem Cell Development Matrix (SESCC)'
            ),
            TypeResponseField(
                at_type=['SESCCStemCellMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            BasicMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='sescc_stem_cell_matrix',
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='immune-cells', request_method='GET', permission='search')
def immune_cells(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Immune Cells'
            ),
            TypeResponseField(
                at_type=['ImmuneCells']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            MissingMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='immune_cells',
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='chip-seq-matrix', request_method='GET', permission='search')
def chip_seq_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='ChIP-seq Matrix'
            ),
            TypeResponseField(
                at_type=['ChipSeqMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            MissingMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='chip_seq_matrix',
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='deeply-profiled-matrix', request_method='GET', permission='search')
def deeply_profiled_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Deeply Profiled Cell Lines'
            ),
            TypeResponseField(
                at_type=['DeeplyProfiledMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            MissingMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='deeply_profiled_matrix',
                reserved_keys=RESERVED_KEYS,
            ),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='deeply-profiled-uniform-batch-matrix', request_method='GET', permission='search')
def deeply_profiled_uniform_batch_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Deeply Profiled Cell Lines'
            ),
            TypeResponseField(
                at_type=['DeeplyProfiledUniformBatchMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            MissingMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='deeply_profiled_uniform_batch_matrix',
                reserved_keys=RESERVED_KEYS,
            ),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='reference-epigenome-matrix', request_method='GET', permission='search')
def reference_epigenome_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Reference Epigenome Matrix'
            ),
            TypeResponseField(
                at_type=['ReferenceEpigenomeMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            BasicMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='reference_epigenome',
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='entex-matrix', request_method='GET', permission='search')
def entex_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Epigenomes from four individuals (ENTEx)'
            ),
            TypeResponseField(
                at_type=['EntexMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            MissingMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='entex',
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='brain-matrix', request_method='GET', permission='search')
def brain_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Rush Alzheimer’s Disease Study'
            ),
            TypeResponseField(
                at_type=['BrainMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            MissingMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='brain_matrix',
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='mouse-development-matrix', request_method='GET', permission='search')
def mouse_development(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Mouse Development Matrix'
            ),
            TypeResponseField(
                at_type=['MouseDevelopmentMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            BasicMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='mouse_development',
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='encore-matrix', request_method='GET', permission='search')
def encore_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='ENCORE Matrix'
            ),
            TypeResponseField(
                at_type=['EncoreMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            BasicMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='encore_matrix',
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='encore-rna-seq-matrix', request_method='GET', permission='search')
def encore_rna_seq_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='ENCORE RNA-seq Matrix'
            ),
            TypeResponseField(
                at_type=['EncoreRnaSeqMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            MissingMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='encore_rna_seq_matrix',
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='degron-matrix', request_method='GET', permission='search')
def degron_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Protein knockdown using the auxin-inducible degron'
            ),
            TypeResponseField(
                at_type=['DegronMatrix']
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            MissingMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name='degron_matrix',
                reserved_keys=RESERVED_KEYS,
            ),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='summary', request_method='GET', permission='search')
def summary(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title=SUMMARY_TITLE
            ),
            TypeResponseField(
                at_type=[SUMMARY_TITLE]
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            BasicMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                matrix_definition_name=SUMMARY_MATRIX,
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='audit', request_method='GET', permission='search')
def audit(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title=AUDIT_TITLE
            ),
            TypeResponseField(
                at_type=[AUDIT_TITLE]
            ),
            IDResponseField(),
            SearchBaseResponseField(),
            ContextResponseField(),
            AuditMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            ),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            TypeOnlyClearFiltersResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='cart-search', request_method='GET', permission='search')
def cart_search(context, request):
    '''
    Like search but takes cart params.
    '''
    # Note the order of rendering matters for some fields, e.g. AllResponseField and
    # NotificationResponseField depend on results from CartSearchWithFacetsResponseField.
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Cart search'
            ),
            TypeResponseField(
                at_type=[SEARCH_TITLE]
            ),
            IDResponseField(),
            ContextResponseField(),
            CartSearchWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                cart=CartWithElements(request),
                reserved_keys=RESERVED_KEYS,
            ),
            AllResponseField(),
            NotificationResponseField(),
            CartFiltersResponseField(),
            ClearFiltersResponseFieldWithCarts(),
            ColumnsResponseField(),
            SortResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='cart-report', request_method='GET', permission='search')
def cart_report(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Cart report'
            ),
            TypeResponseField(
                at_type=[REPORT_TITLE]
            ),
            IDResponseField(),
            ContextResponseField(),
            CartReportWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                cart=CartWithElements(request),
                reserved_keys=RESERVED_KEYS,
            ),
            AllResponseField(),
            NotificationResponseField(),
            CartFiltersResponseField(),
            TypeOnlyClearFiltersResponseFieldWithCarts(),
            ColumnsResponseField(),
            NonSortableResponseField(),
            SortResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='cart-matrix', request_method='GET', permission='search')
def cart_matrix(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title='Cart matrix'
            ),
            TypeResponseField(
                at_type=[MATRIX_TITLE]
            ),
            IDResponseField(),
            SearchBaseResponseField(
                search_base='/cart-search/'
            ),
            ContextResponseField(),
            CartMatrixWithFacetsResponseField(
                default_item_types=DEFAULT_ITEM_TYPES,
                cart=CartWithElements(request),
                reserved_keys=RESERVED_KEYS,
            ),
            NotificationResponseField(),
            CartFiltersResponseField(),
            TypeOnlyClearFiltersResponseFieldWithCarts(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()


@view_config(route_name='top-hits-raw', request_method='GET', permission='search')
def top_hits_raw(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            RawTopHitsResponseField(
                default_item_types=TOP_HITS_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
            )
        ]
    )
    return fr.render()


@view_config(route_name='top-hits', request_method='GET', permission='search')
def top_hits(context, request):
    fr = FieldedResponse(
        response_fields=[
            TypeResponseField(
                at_type=['TopHitsSearch']
            )
        ]
    )
    return fr.render()


@view_config(route_name='rnaget-report', request_method='GET', permission='search')
@conditional_cache(
    cache=get_redis_lru_cache(),
    condition=should_cache_search_results,
    key=partial(make_key_from_request, 'rnaget-report'),
)
def rnaget_report(context, request):
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            RemoteResponseField(
                how=remote_get,
                where=RNAGET_REPORT_URL,
                then=set_status_and_parse_json,
            ),
            NonSortableResponseField(),
        ]
    )
    return fr.render()


@view_config(route_name='search-config-registry', request_method='GET', permission='config')
def search_config_registry(context, request):
    registry = request.registry[SEARCH_CONFIG]
    return dict(sorted(registry.as_dict().items()))


@view_config(route_name='homepage-search', request_method='GET', permission='search')
def homepage_search(context, request):
    # Searches over top hit item types and calculates one @type facet.
    fr = FieldedResponse(
        _meta={
            'params_parser': ParamsParser(request)
        },
        response_fields=[
            TitleResponseField(
                title=SEARCH_TITLE
            ),
            TypeResponseField(
                at_type=['HomePageSearch']
            ),
            IDResponseField(),
            ContextResponseField(),
            BasicSearchWithFacetsResponseField(
                default_item_types=TOP_HITS_ITEM_TYPES,
                reserved_keys=RESERVED_KEYS,
                facets=HOMEPAGE_SEARCH_FACETS,
            ),
            AllResponseField(),
            FacetGroupsResponseField(),
            NotificationResponseField(),
            FiltersResponseField(),
            ClearFiltersResponseField(),
            SortResponseField(),
            DebugQueryResponseField()
        ]
    )
    return fr.render()
