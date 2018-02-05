from pyramid.response import Response
from pyramid.view import view_config
from pyramid.compat import bytes_
from snovault import Item
from collections import OrderedDict
from copy import deepcopy
import json
import os
from urllib.parse import (
    parse_qs,
    urlencode,
)
from snovault.elasticsearch.interfaces import ELASTIC_SEARCH
import time
from pkg_resources import resource_filename

import logging

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)

ASSEMBLY_DETAILS = {
    'GRCh38':         { 'species':          'Homo sapiens',     'assembly_reference': 'GRCh38',
                        'common_name':      'human',
                        'ucsc_assembly':    'hg38',
                        'ensembl_host':     'www.ensembl.org',
                        'quickview':        True,
                        'comment':          'Ensembl works'
    },
    'GRCh38-minimal': { 'species':          'Homo sapiens',     'assembly_reference': 'GRCh38',
                        'common_name':      'human',
                        'ucsc_assembly':    'hg38',
                        'ensembl_host':     'www.ensembl.org',
    },
    'hg19': {           'species':          'Homo sapiens',     'assembly_reference': 'GRCh37',
                        'common_name':      'human',
                        'ucsc_assembly':    'hg19',
                        'NA_ensembl_host':  'grch37.ensembl.org',
                        'quickview':        True,
                        'comment':          'Ensembl DOES NOT WORK'
    },
    'mm10': {           'species':          'Mus musculus',     'assembly_reference': 'GRCm38',
                        'common_name':      'mouse',
                        'ucsc_assembly':    'mm10',
                        'ensembl_host':     'www.ensembl.org',
                        'quickview':        True,
                        'comment':          'Ensembl works'
    },
    'mm10-minimal': {   'species':          'Mus musculus',     'assembly_reference': 'GRCm38',
                        'common_name':      'mouse',
                        'ucsc_assembly':    'mm10',
                        'ensembl_host':     'www.ensembl.org',
                        'quickview':        True,
                        'comment':          'Should this be removed?'
    },
    'mm9': {            'species':          'Mus musculus',     'assembly_reference': 'NCBI37',
                        'common_name':      'mouse',
                        'ucsc_assembly':    'mm9',
                        'NA_ensembl_host':  'may2012.archive.ensembl.org',
                        'quickview':        True,
                        'comment':          'Ensembl DOES NOT WORK'
    },
    'dm6': {    'species':          'Drosophila melanogaster',  'assembly_reference': 'BDGP6',
                'common_name':      'fruit fly',
                'ucsc_assembly':    'dm6',
                'NA_ensembl_host':  'www.ensembl.org',
                'quickview':        True,
                'comment':          'Ensembl DOES NOT WORK'
    },
    'dm3': {    'species':          'Drosophila melanogaster',  'assembly_reference': 'BDGP5',
                'common_name':      'fruit fly',
                'ucsc_assembly':    'dm3',
                'NA_ensembl_host':  'dec2014.archive.ensembl.org',
                'quickview':        True,
                'comment':          'Ensembl DOES NOT WORK'
    },
    'ce11': {   'species':          'Caenorhabditis elegans',   'assembly_reference': 'WBcel235',
                'common_name':      'worm',
                'ucsc_assembly':    'ce11',
                'NA_ensembl_host':  'www.ensembl.org',
                'quickview':        True,
                'comment':          'Ensembl DOES NOT WORK'
    },
    'ce10': {   'species':          'Caenorhabditis elegans',   'assembly_reference': 'WS220',
                'common_name':      'worm',
                'ucsc_assembly':    'ce10',
                'quickview':        True,
                'comment':          'Never Ensembl'
    },
    'ce6': {    'species':          'Caenorhabditis elegans',   'assembly_reference': 'WS190',
                'common_name':      'worm',
                'ucsc_assembly':    'ce6',
                'comment':          'Never Ensembl, not found in encoded'
    },
    'J02459.1': {   'species':      'Escherichia virus Lambda', 'assembly_reference': 'J02459.1',
                    'common_name':  'lambda phage',
                    'comment':      'Never visualized'
    },
}

# Distinct from ASSEMBLY_DETAILS['ucsc_assembly'] as that defines allowed mappings
ASSEMBLY_TO_UCSC_ID = {
    'GRCh38-minimal': 'hg38',
    'GRCh38': 'hg38',
    'GRCh37': 'hg19',
    'mm10-minimal': 'mm10',
    'GRCm38': 'mm10',
    'NCBI37': 'mm9',
    'BDGP6': 'dm6',
    'BDGP5': 'dm3',
    'WBcel235': 'ce11'
}


QUICKVIEW_STATUSES_BLOCKED = ["proposed", "started", "deleted", "revoked", "replaced"]

VISIBLE_DATASET_STATUSES = ["released"]
VISIBLE_FILE_STATUSES = ["released"]
BIGWIG_FILE_TYPES = ['bigWig']
BIGBED_FILE_TYPES = ['bigBed']
VISIBLE_FILE_FORMATS = BIGBED_FILE_TYPES + BIGWIG_FILE_TYPES
VISIBLE_DATASET_TYPES = ["Experiment", "Annotation"]
VISIBLE_DATASET_TYPES_LC = ["experiment", "annotation"]


# Supported tokens are the only tokens the code currently knows how to look up.
SUPPORTED_MASK_TOKENS = [
    "{replicate}",         # replicate that that will be displayed: ("rep1", "combined")
    "{rep_tech}",          # The rep_tech if desired ("rep1_1", "combined")
    "{replicate_number}",  # The replicate number displayed for visualized track: ("1", "0")
    "{biological_replicate_number}",
    "{technical_replicate_number}",
    "{assay_title}",
    "{assay_term_name}",                      # dataset.assay_term_name
    "{annotation_type}",                      # some datasets have annotation type and not assay
    "{output_type}",                          # files.output_type
    "{accession}", "{experiment.accession}",  # "{accession}" is assumed to be experiment.accession
    "{file.accession}",
    "{@id}", "{@type}",                       # dataset only
    "{target}", "{target.label}",             # Either is acceptible
    "{target.title}",
    "{target.name}",                          # Used in metadata URLs
    "{target.investigated_as}",
    "{biosample_term_name}", "{biosample_term_name|multiple}",  # "|multiple": none means multiple
    "{output_type_short_label}",                # hard-coded translation from output_type to very
                                                # short version
    "{replicates.library.biosample.summary}",   # Idan, Forrest and Cricket are conspiring to move
                                                # to dataset.biosample_summary & make it shorter
    "{replicates.library.biosample.summary|multiple}",   # "|multiple": none means multiple
    "{assembly}",                               # you don't need this in titles, but it is crucial
                                                # variable and seems to not be being applied
                                                # # correctly in the html generation
    "{lab.title}",                              # In metadata
    "{award.rfa}",                              # To distinguish vis_defs based upon award
    # TODO "{software? or pipeline?}",  # Cricket: "I am stumbling over the fact that we
    #                                   #    can't distinguish tophat and star produced files"
    # TODO "{phase}",                   # Cricket: "If we get to the point of being fancy
    #                                   #    in the replication timing, then we need this,
    #                                   #    otherwise it bundles up in the biosample summary now"
    ]

# Simple tokens are a straight lookup, no questions asked
SIMPLE_DATASET_TOKENS = ["{biosample_term_name}", "{accession}", "{assay_title}",
                         "{assay_term_name}", "{annotation_type}", "{@id}", "{@type}"]

# static group defs are keyed by group title (or special token) and consist of
# tag: (optional) unique terse key for referencing group
# groups: (optional) { subgroups keyed by subgroup title }
# group_order: (optional) [ ordered list of subgroup titles ]
# other definitions

# live group defs are keyed by tag and are the transformed in memory version of static defs
# title: (required) same as the static group's key
# groups: (if appropriate) { subgroups keyed by subgroup tag }
# group_order: (if appropriate) [ ordered list of subgroup tags ]

VIS_DEFS_FOLDER = "static/vis_defs/"
VIS_DEFS_BY_TYPE = {}
VIS_DEFS_DEFAULT = {}


# vis_defs may not have the default experiment group defined
EXP_GROUP = "Experiment"
DEFAULT_EXPERIMENT_GROUP = {"tag": "EXP", "groups": {"one": {"title_mask": "{accession}",
                            "url_mask": "experiments/{accession}"}}}

# Pennants are flags that display at UCSC next to composite definitions
PENNANTS = {
    "NHGRI":     ("https://www.encodeproject.org/static/img/pennant-nhgri.png "
                  "https://www.encodeproject.org/ "
                  "\"This trackhub was automatically generated from the files and metadata found "
                  "at the ENCODE portal\""),
    "ENCODE":    ("https://www.encodeproject.org/static/img/pennant-encode.png "
                  "https://www.encodeproject.org/ "
                  "\"This trackhub was automatically generated from the ENCODE files and metadata "
                  "found at the ENCODE portal\""),
    "modENCODE": ("https://www.encodeproject.org/static/img/pennant-encode.png "
                  "https://www.encodeproject.org/ "
                  "\"This trackhub was automatically generated from the modENCODE files and "
                  "metadata found at the ENCODE portal\""),
    "GGR":       ("https://www.encodeproject.org/static/img/pennant-ggr.png "
                  "https://www.encodeproject.org/ "
                  "\"This trackhub was automatically generated from  the Genomics of "
                  "Gene Regulation files files and metadata found at the "
                  "ENCODE portal\""),
    "REMC":      ("https://www.encodeproject.org/static/img/pennant-remc.png "
                  "https://www.encodeproject.org/ "
                  "\"This trackhub was automatically generated from the Roadmap Epigentics files "
                  "and metadata found at the ENCODE portal\"")
    # "Roadmap":   "encodeThumbnail.jpg "
    #              "https://www.encodeproject.org/ "
    #              "\"This trackhub was automatically generated from the Roadmap files and "
    #              "metadata found at https://www.encodeproject.org/\"",
    # "modERN":   "encodeThumbnail.jpg "
    #             "https://www.encodeproject.org/ "
    #             "\"This trackhub was automatically generated from the modERN files and "
    #             "metadata found at https://www.encodeproject.org/\"",
    }


# supported groups for arranging/sorting files in a visualization
SUPPORTED_SUBGROUPS = ["Biosample", "Targets", "Assay", "Replicates", "Views", EXP_GROUP]

# UCSC trackDb settings that are supported
SUPPORTED_TRACK_SETTINGS = [
    "type", "visibility", "longLabel", "shortLabel", "color", "altColor", "allButtonPair", "html",
    "scoreFilter", "spectrum", "minGrayLevel", "itemRgb", "viewLimits",
    "autoScale", "negateValues", "maxHeightPixels", "windowingFunction", "transformFunc",
    "signalFilter", "signalFilterLimits", "pValueFilter", "pValueFilterLimits",
    "qValueFilter", "qValueFilterLimits" ]
VIEW_SETTINGS = SUPPORTED_TRACK_SETTINGS

# UCSC trackDb settings that are supported
COMPOSITE_SETTINGS = ["longLabel", "shortLabel", "visibility", "pennantIcon", "allButtonPair",
                      "html"]
# UCSC settings for individual files (tracks)
TRACK_SETTINGS = ["bigDataUrl", "longLabel", "shortLabel", "type", "color", "altColor"]

# This dataset terms (among others) are needed in vis_dataset formatting
ENCODED_DATASET_TERMS = ['biosample_term_name', 'biosample_term_id', 'biosample_summary',
                    'biosample_type', 'assay_term_id', 'assay_term_name']

# Abbeviations  for output_type to fit in UCSC shortLabel
OUTPUT_TYPE_8CHARS = {
    # "idat green channel": "idat gr",     # raw data
    # "idat red channel": "idat rd",       # raw data
    # "reads":"reads",                     # raw data
    # "intensity values": "intnsty",       # raw data
    # "reporter code counts": "rcc",       # raw data
    # "alignments":"aln",                  # our plan is not to visualize alignments for now
    # "unfiltered alignments":"unflt aln", # our plan is not to visualize alignments for now
    # "transcriptome alignments":"tr aln", # our plan is not to visualize alignments for now
    "minus strand signal of all reads":     "all -",
    "plus strand signal of all reads":      "all +",
    "signal of all reads":                  "all sig",
    "normalized signal of all reads":       "normsig",
    # "raw minus strand signal":"raw -",   # these are all now minus signal of all reads
    # "raw plus strand signal":"raw +",    # these are all now plus signal of all reads
    "raw signal":                           "raw sig",
    "raw normalized signal":                "nraw",
    "read-depth normalized signal":         "rdnorm",
    "control normalized signal":            "ctlnorm",
    "minus strand signal of unique reads":  "unq -",
    "plus strand signal of unique reads":   "unq +",
    "signal of unique reads":               "unq sig",
    "signal p-value":                       "pval sig",
    "fold change over control":             "foldchg",
    "exon quantifications":                 "exon qt",
    "gene quantifications":                 "gene qt",
    "microRNA quantifications":             "miRNA qt",
    "transcript quantifications":           "trsct qt",
    "library fraction":                     "lib frac",
    "methylation state at CpG":             "mth CpG",
    "methylation state at CHG":             "mth CHG",
    "methylation state at CHH":             "mth CHH",
    "enrichment":                           "enrich",
    "replication timing profile":           "repli tm",
    "variant calls":                        "vars",
    "filtered SNPs":                        "f SNPs",
    "filtered indels":                      "f indel",
    "hotspots":                             "hotspt",
    "long range chromatin interactions":    "lrci",
    "chromatin interactions":               "ch int",
    "topologically associated domains":     "tads",
    "genome compartments":                  "compart",
    "open chromatin regions":               "open ch",
    "filtered peaks":                       "filt pk",
    "filtered regions":                     "filt reg",
    "DHS peaks":                            "DHS pk",
    "peaks":                                "peaks",
    "replicated peaks":                     "rep pk",
    "RNA-binding protein associated mRNAs": "RBP RNA",
    "splice junctions":                     "splice",
    "transcription start sites":            "tss",
    "predicted enhancers":                  "pr enh",
    "candidate enhancers":                  "can enh",
    "candidate promoters":                  "can pro",
    "predicted forebrain enhancers":        "fb enh",    # plan to fix these
    "predicted heart enhancers":            "hrt enh",       # plan to fix these
    "predicted whole brain enhancers":      "wb enh",  # plan to fix these
    "candidate regulatory elements":        "can re",
    # "genome reference":"ref",           # references not to be viewed
    # "transcriptome reference":"tr ref", # references not to be viewed
    # "transcriptome index":"tr rix",     # references not to be viewed
    # "tRNA reference":"tRNA",            # references not to be viewed
    # "miRNA reference":"miRNA",          # references not to be viewed
    # "snRNA reference":"snRNA",          # references not to be viewed
    # "rRNA reference":"rRNA",            # references not to be viewed
    # "TSS reference":"TSS",              # references not to be viewed
    # "reference variants":"var",         # references not to be viewed
    # "genome index":"ref ix",            # references not to be viewed
    # "female genome reference":"XX ref", # references not to be viewed
    # "female genome index":"XX rix",     # references not to be viewed
    # "male genome reference":"XY ref",   # references not to be viewed
    # "male genome index":"XY rix",       # references not to be viewed
    # "spike-in sequence":"spike",        # references not to be viewed
    "optimal idr thresholded peaks":        "oIDR pk",
    "conservative idr thresholded peaks":   "cIDR pk",
    "enhancer validation":                  "enh val",
    "semi-automated genome annotation":     "saga"
    }

# Track coloring is defined by biosample
BIOSAMPLE_COLOR = {
    "induced pluripotent stem cell line":       {"color": "80,49,120",
                                                 "altColor": "107,95,102"},  # Purple
    "stem cell":        {"color": "0,107,27",    "altColor": "0.0,77,20"},   # Dark Green
    "GM12878":          {"color": "153,38,0",    "altColor": "115,31,0"},    # Dark Orange-Red
    "H1-hESC":          {"color": "0,107,27",    "altColor": "0,77,20"},     # Dark Green
    "K562":             {"color": "46,0,184",    "altColor": "38,0,141"},    # Dark Blue
    "keratinocyte":     {"color": "179,0,134",   "altColor": "154,0,113"},   # Darker Pink-Purple
    "HepG2":            {"color": "189,0,157",   "altColor": "189,76,172"},  # Pink-Purple
    "HeLa-S3":          {"color": "0,119,158",   "altColor": "0,94,128"},    # Greenish-Blue
    "HeLa":             {"color": "0,119,158",   "altColor": "0,94,128"},    # Greenish-Blue
    "A549":             {"color": "204,163,0",   "altColor": "218,205,22"},  # Dark Yellow
    "endothelial cell of umbilical vein":       {"color": "224,75,0",
                                                 "altColor": "179,60,0"},    # Pink
    "MCF-7":            {"color": "22,219,206",  "altColor": "18,179,168"},  # Cyan
    "SK-N-SH":          {"color": "255,115,7",   "altColor": "218,98,7"},    # Orange
    "IMR-90":           {"color": "6,62,218",    "altColor": "5,52,179"},    # Blue
    "CH12.LX":          {"color": "86,180,233",  "altColor": "76,157,205"},  # Dark Orange-Red
    "MEL cell line":    {"color": "46,0,184",    "altColor": "38,0,141"},    # Dark Blue
    "brain":            {"color": "105,105,105", "altColor": "77,77,77"},    # Grey
    "eye":              {"color": "105,105,105", "altColor": "77,77,77"},    # Grey
    "spinal cord":      {"color": "105,105,105", "altColor": "77,77,77"},    # Grey
    "olfactory organ":  {"color": "105,105,105", "altColor": "77,77,77"},    # Grey
    "esophagus":        {"color": "230,159,0",   "altColor": "179,125,0"},   # Mustard
    "stomach":          {"color": "230,159,0",   "altColor": "179,125,0"},   # Mustard
    "liver":            {"color": "230,159,0",   "altColor": "179,125,0"},   # Mustard
    "pancreas":         {"color": "230,159,0",   "altColor": "179,125,0"},   # Mustard
    "large intestine":  {"color": "230,159,0",   "altColor": "179,125,0"},   # Mustard
    "small intestine":  {"color": "230,159,0",   "altColor": "179,125,0"},   # Mustard
    "gonad":            {"color": "0.0,158,115", "altColor": "0.0,125,92"},  # Darker Aquamarine
    "mammary gland":    {"color": "0.0,158,115", "altColor": "0.0,125,92"},  # Darker Aquamarine
    "prostate gland":   {"color": "0.0,158,115", "altColor": "0.0,125,92"},  # Darker Aquamarine
    "ureter":           {"color": "204,121,167", "altColor": "166,98,132"},  # Grey-Pink
    "urinary bladder":  {"color": "204,121,167", "altColor": "166,98,132"},  # Grey-Pink
    "kidney":           {"color": "204,121,167", "altColor": "166,98,132"},  # Grey-Pink
    "muscle organ":     {"color": "102,50,200 ", "altColor": "81,38,154"},   # Violet
    "tongue":           {"color": "102,50,200",  "altColor": "81,38,154"},   # Violet
    "adrenal gland":    {"color": "189,0,157",   "altColor": "154,0,128"},   # Pink-Purple
    "thyroid gland":    {"color": "189,0,157",   "altColor": "154,0,128"},   # Pink-Purple
    "lung":             {"color": "145,235,43",  "altColor": "119,192,35"},  # Mossy green
    "bronchus":         {"color": "145,235,43",  "altColor": "119,192,35"},  # Mossy green
    "trachea":          {"color": "145,235,43",  "altColor": "119,192,35"},  # Mossy green
    "nose":             {"color": "145,235,43",  "altColor": "119,192,35"},  # Mossy green
    "placenta":         {"color": "153,38,0",    "altColor": "102,27,0"},    # Orange-Brown
    "extraembryonic structure":                 {"color": "153,38,0",
                                                 "altColor": "102,27,0"},    # Orange-Brown
    "thymus":           {"color": "86,180,233",  "altColor": "71,148,192"},  # Baby Blue
    "spleen":           {"color": "86,180,233",  "altColor": "71,148,192"},  # Baby Blue
    "bone element":     {"color": "86,180,233",  "altColor": "71,148,192"},  # Baby Blue
    "blood":            {"color": "86,180,233",  "altColor": "71,148,192"},  # Baby Blue (red?)
    "blood vessel":     {"color": "214,0,0",     "altColor": "214,79,79"},   # Red
    "heart":            {"color": "214,0,0",     "altColor": "214,79,79"},   # Red
    "lymphatic vessel": {"color": "214,0,0",     "altColor": "214,79,79"},   # Red
    "skin of body":     {"color": "74,74,21",    "altColor": "102,102,44"},   # Brown
    }

VIS_CACHE_INDEX = "vis_cache"


class Sanitize(object):
    # Tools for sanitizing labels

    def escape_char(self, c, exceptions=['_'], htmlize=False, numeralize=False):
        '''Pass through for 0-9,A-Z.a-z,_, but then either html encodes, numeralizes or removes special
        characters.'''
        n = ord(c)
        if n >= 47 and n <= 57:  # 0-9
            return c
        if n >= 65 and n <= 90:  # A-Z
            return c
        if n >= 97 and n <= 122:  # a-z
            return c
        if c in exceptions:
            return c
        if n == 32:              # space
            return '_'
        if htmlize:
            return "&#%d;" % n
        if numeralize:
            return "%d" % n

        return ""

    def label(self, s):
        '''Encodes the string to swap special characters and leaves spaces alone.'''
        new_s = ""      # longLabel and shorLabel can have spaces and some special characters
        for c in s:
            new_s += self.escape_char(c, [' ', '_', '.', '-', '(', ')', '+'], htmlize=False)
        return new_s

    def title(self, s):
        '''Encodes the string to swap special characters and replace spaces with '_'.'''
        new_s = ""      # Titles appear in tag=title pairs and cannot have spaces
        for c in s:
            new_s += self.escape_char(c, ['_', '.', '-', '(', ')', '+'], htmlize=True)
        return new_s

    def tag(self, s):
        '''Encodes the string to swap special characters and remove spaces.'''
        new_s = ""
        first = True
        for c in s:
            new_s += self.escape_char(c, numeralize=True)
            if first:
                if new_s.isdigit():  # tags cannot start with digit.
                    new_s = 'z' + new_s
                first = False
        return new_s

    def name(self, s):
        '''Encodes the string to remove special characters swap spaces for underscores.'''
        new_s = ""
        for c in s:
            new_s += self.escape_char(c)
        return new_s

sanitize = Sanitize()


class VisDefines(object):
    # Loads vis_def static files and other defines for vis formatting
    # This class is also a swiss army knife of vis formatting conversions

    def __init__(self, dataset=None):
        # Make these global so that the same files are not continually reloaded
        global VIS_DEFS_BY_TYPE
        global VIS_DEFS_DEFAULT
        self.vis_defs = VIS_DEFS_BY_TYPE
        self.vis_def_default = VIS_DEFS_DEFAULT
        self.vis_type = "opaque"
        self.dataset = dataset

        if not self.vis_defs:
            self.load_vis_defs()

    def load_vis_defs(self):
        '''Loads 'vis_defs' (visualization definitions by assay type) from a static files.'''
        #global VIS_DEFS_FOLDER
        global VIS_DEFS_BY_TYPE
        global VIS_DEFS_DEFAULT
        folder = resource_filename(__name__, VIS_DEFS_FOLDER)
        files = os.listdir(folder)
        for filename in files:
            if filename.endswith('.json'):
                with open(folder + filename) as fh:
                    log.debug('Preparing to load %s' % (filename))
                    vis_def = json.load(fh)
                    # Could alter vis_defs here if desired.
                    if vis_def:
                        VIS_DEFS_BY_TYPE.update(vis_def)

        self.vis_defs = VIS_DEFS_BY_TYPE
        VIS_DEFS_DEFAULT = self.vis_defs.get("opaque",{})
        self.vis_def_default = VIS_DEFS_DEFAULT

    def get_vis_type(self):
        '''returns the best visualization definition type, based upon dataset.'''
        assert(self.dataset is not None)
        assay = self.dataset.get("assay_term_name", 'none')

        if isinstance(assay, list):
            if len(assay) == 1:
                assay = assay[0]
            else:
                log.debug("assay_term_name for %s is unexpectedly a list %s" %
                        (self.dataset['accession'], str(assay)))
                return "opaque"

        # simple rule defined in most vis_defs
        for vis_type in sorted(self.vis_defs.keys(), reverse=True):  # Reverse pushes anno to bottom
            if "rule" in self.vis_defs[vis_type]:
                rule = self.vis_defs[vis_type]["rule"].replace('{assay_term_name}', assay)
                if rule.find('{') != -1:
                    rule = self.convert_mask(rule)
                if eval(rule):
                    self.vis_type = vis_type
                    return self.vis_type

        # Ugly rules:
        vis_type = None
        if assay in ["RNA-seq", "single cell isolation followed by RNA-seq"]:
            reps = self.dataset.get("replicates", [])  # NOTE: overly cautious
            if len(reps) < 1:
                log.debug("Could not distinguish between long and short RNA for %s because there are "
                        "no replicates.  Defaulting to short." % (self.dataset.get("accession")))
                vis_type = "SRNA"  # this will be more noticed if there is a mistake
            else:
                size_range = reps[0].get("library", {}).get("size_range", "")
                if size_range.startswith('>'):
                    try:
                        min_size = int(size_range[1:])
                        max_size = min_size
                    except:
                        log.debug("Could not distinguish between long and short RNA for %s.  "
                                "Defaulting to short." % (self.dataset.get("accession")))
                        vis_type = "SRNA"  # this will be more noticed if there is a mistake
                elif size_range.startswith('<'):
                    try:
                        max_size = int(size_range[1:]) - 1
                        min_size = 0
                    except:
                        log.debug("Could not distinguish between long and short RNA for %s.  "
                                "Defaulting to short." % (self.dataset.get("accession")))
                        self.vis_type = "SRNA"  # this will be more noticed if there is a mistake
                        return self.vis_type
                else:
                    try:
                        sizes = size_range.split('-')
                        min_size = int(sizes[0])
                        max_size = int(sizes[1])
                    except:
                        log.debug("Could not distinguish between long and short RNA for %s.  "
                                "Defaulting to short." % (self.dataset.get("accession")))
                        vis_type = "SRNA"  # this will be more noticed if there is a mistake

                if vis_type is None:
                    if max_size <= 200 and max_size != min_size:
                        vis_type = "SRNA"
                    elif min_size >= 150:
                        vis_type = "LRNA"
                    elif (min_size + max_size)/2 >= 235:
                        # This is some wicked voodoo (SRNA:108-347=227; LRNA:155-315=235)
                        vis_type = "LRNA"
                    else:
                        vis_type = "SRNA"

        if vis_type is None:
            log.debug("%s (assay:'%s') has undefined vis_type" % (self.dataset['accession'], assay))
            vis_type = "opaque"  # This becomes a dict key later so None is not okay

        self.vis_type = vis_type
        return self.vis_type

    def get_vis_def(self, vis_type=None):
        '''returns the visualization definition set, based upon dataset.'''
        if vis_type is None:
            vis_type = self.vis_type

        vis_def = self.vis_defs.get(vis_type, self.vis_def_default)
        if "other_groups" in vis_def and EXP_GROUP not in vis_def["other_groups"]["groups"]:
            vis_def["other_groups"]["groups"][EXP_GROUP] = DEFAULT_EXPERIMENT_GROUP
        if "sortOrder" in vis_def and EXP_GROUP not in vis_def["sortOrder"]:
            vis_def["sortOrder"].append(EXP_GROUP)
        return vis_def

    def visible_file_statuses(self):
        return VISIBLE_FILE_STATUSES

    def supported_subgroups(self):
        return SUPPORTED_SUBGROUPS

    def encoded_dataset_terms(self):
        return ENCODED_DATASET_TERMS

    def pennants(self, project):
        return PENNANTS.get(project, PENNANTS['NHGRI'])

    def find_pennent(self):
        '''Returns an appropriate pennantIcon given dataset's award'''
        assert(self.dataset is not None)
        project = self.dataset.get("award", {}).get("project", "NHGRI")
        return self.pennants(project)

    def lookup_colors(self):
        '''Using the mask, determine which color table to use.'''
        assert(self.dataset is not None)
        color = None
        altColor = None
        coloring = {}
        biosample_term = self.dataset.get('biosample_type')
        if biosample_term is not None:
            if isinstance(biosample_term, list):
                if len(biosample_term) == 1:
                    biosample_term = biosample_term[0]
                else:
                    log.debug("%s has biosample_type %s that is unexpectedly a list" %
                            (self.dataset['accession'], str(biosample_term)))
                    biosample_term = "unknown"  # really only seen in test data!
            coloring = BIOSAMPLE_COLOR.get(biosample_term, {})
        if not coloring:
            biosample_term = self.dataset.get('biosample_term_name')
            if biosample_term is not None:
                if isinstance(biosample_term, list):
                    if len(biosample_term) == 1:
                        biosample_term = biosample_term[0]
                    else:
                        log.debug("%s has biosample_term_name %s that is unexpectedly a list" %
                                (self.dataset['accession'], str(biosample_term)))
                        biosample_term = "unknown"  # really only seen in test data!
                coloring = BIOSAMPLE_COLOR.get(biosample_term, {})
        if not coloring:
            organ_slims = self.dataset.get('organ_slims', [])
            if len(organ_slims) > 1:
                coloring = BIOSAMPLE_COLOR.get(organ_slims[1])
        if coloring:
            assert("color" in coloring)
            if "altColor" not in coloring:
                color = coloring["color"]
                shades = color.split(',')
                red = int(shades[0]) / 2
                green = int(shades[1]) / 2
                blue = int(shades[2]) / 2
                altColor = "%d,%d,%d" % (red, green, blue)
                coloring["altColor"] = altColor

        return coloring

    def add_living_color(self, live_format):
        '''Adds color and altColor.  Note that altColor is only added if color is found.'''
        colors = self.lookup_colors()
        if colors and "color" in colors:
            live_format["color"] = colors["color"]
            if "altColor" in colors:
                live_format["altColor"] = colors["altColor"]

    def rep_for_file(self, a_file):
        '''Determines best rep_tech or rep for a file.'''

        # Starting with a little cheat for rare cases where techreps are compared instead of bioreps
        if a_file.get("file_format_type", "none") in ["idr_peak"]:
            return "combined"
        if a_file['output_type'].endswith("idr thresholded peaks"):
            return "combined"

        bio_rep = 0
        tech_rep = 0
        if "replicate" in a_file:
            bio_rep = a_file["replicate"]["biological_replicate_number"]
            tech_rep = a_file["replicate"]["technical_replicate_number"]

        elif "tech_replicates" in a_file:
            # Do we want to make rep1_1.2.3 ?  Not doing it now
            tech_reps = a_file["tech_replicates"]
            if len(tech_reps) == 1:
                bio_rep = int(tech_reps[0].split('_')[0])
                tech_reps = tech_reps[0][2:]
                if len(tech_reps) == 1:
                    tech_rep = int(tech_reps)
            elif len(tech_reps) > 1:
                bio = 0
                for tech in tech_reps:
                    if bio == 0:
                        bio = int(tech.split('_')[0])
                    elif bio != int(tech.split('_')[0]):
                        bio = 0
                        break
                if bio > 0:
                    bio_rep = bio

        elif "biological_replicates" in a_file:
            bio_reps = a_file["biological_replicates"]
            if len(bio_reps) == 1:
                bio_rep = bio_reps[0]

        if bio_rep == 0:
            return "combined"

        rep = "rep%d" % bio_rep
        if tech_rep > 0:
            rep += "_%d" % tech_rep
        return rep

    def lookup_token(self, token, dataset, a_file=None):
        '''Encodes the string to swap special characters and remove spaces.'''
        # dataset might not be self.dataset

        if token not in SUPPORTED_MASK_TOKENS:
            log.warn("Attempting to look up unexpected token: '%s'" % token)
            return "unknown token"

        if token in SIMPLE_DATASET_TOKENS:
            term = dataset.get(token[1:-1])
            if term is None:
                return "Unknown " + token[1:-1].split('_')[0].capitalize()
            elif isinstance(term,list) and len(term) > 3:
                return "Collection of %d %ss" % (len(term),token[1:-1].split('_')[0].capitalize())
            return term
        elif token == "{experiment.accession}":
            return dataset['accession']
        elif token in ["{target}", "{target.label}", "{target.name}", "{target.title}"]:
            target = dataset.get('target', {})
            if isinstance(target, list):
                if len(target) > 0:
                    target = target[0]
                else:
                    target = {}
            if token.find('.') > -1:
                sub_token = token.strip('{}').split('.')[1]
            else:
                sub_token = "label"
            return target.get(sub_token, "Unknown Target")
        elif token in ["{target.name}", "{target.investigated_as}"]:
            target = dataset.get('target', {})
            if isinstance(target, list):
                if len(target) > 0:
                    target = target[0]
                else:
                    target = {}
            if token == "{target.name}":
                return target.get('label', "Unknown Target")
            elif token == "{target.investigated_as}":
                investigated_as = target.get('investigated_as', "Unknown Target")
                if not isinstance(investigated_as, list):
                    return investigated_as
                elif len(investigated_as) > 0:
                    return investigated_as[0]
                else:
                    return "Unknown Target"
        elif token in ["{replicates.library.biosample.summary}",
                    "{replicates.library.biosample.summary|multiple}"]:
            term = None
            replicates = dataset.get("replicates", [])
            if replicates:
                term = replicates[0].get("library", {}).get("biosample", {}).get("summary")
            if term is None:
                term = dataset.get("{biosample_term_name}")
            if term is None:
                if token.endswith("|multiple}"):
                    term = "multiple biosamples"
                else:
                    term = "Unknown Biosample"
            return term
        elif token == "{lab.title}":
            return dataset['lab'].get('title', 'unknown')
        elif token == "{award.rfa}":
            return dataset['award'].get('rfa', 'unknown')
        elif token == "{biosample_term_name|multiple}":
            return dataset.get("biosample_term_name", "multiple biosamples")
        # TODO: rna_species
        # elif token == "{rna_species}":
        #     if replicates.library.nucleic_acid = polyadenylated mRNA
        #        rna_species = "polyA RNA"
        #     elif replicates.library.nucleic_acid == "RNA":
        #        if "polyadenylated mRNA" in replicates.library.depleted_in_term_name
        #                rna_species = "polyA depleted RNA"
        #        else
        #                rna_species = "total RNA"
        elif a_file is not None:
            if token == "{file.accession}":
                return a_file['accession']
            elif token == "{output_type}":
                return a_file['output_type']
            elif token == "{output_type_short_label}":
                output_type = a_file['output_type']
                return OUTPUT_TYPE_8CHARS.get(output_type, output_type)
            elif token == "{replicate}":
                rep_tag = a_file.get("rep_tag")
                if rep_tag is not None:
                    while len(rep_tag) > 4:
                        if rep_tag[3] != '0':
                            break
                        rep_tag = rep_tag[0:3] + rep_tag[4:]
                    return rep_tag
                rep_tech = a_file.get("rep_tech")
                if rep_tech is not None:
                    return rep_tech.split('_')[0]  # Should truncate tech_rep
                rep_tech = self.rep_for_file(a_file)
                return rep_tech.split('_')[0]  # Should truncate tech_rep
            elif token == "{replicate_number}":
                rep_tag = a_file.get("rep_tag", a_file.get("rep_tech", self.rep_for_file(a_file)))
                if not rep_tag.startswith("rep"):
                    return "0"
                return rep_tag[3:].split('_')[0]
            elif token == "{biological_replicate_number}":
                rep_tech = a_file.get("rep_tech", self.rep_for_file(a_file))
                if not rep_tech.startswith("rep"):
                    return "0"
                return rep_tech[3:].split('_')[0]
            elif token == "{technical_replicate_number}":
                rep_tech = a_file.get("rep_tech", self.rep_for_file(a_file))
                if not rep_tech.startswith("rep"):
                    return "0"
                return rep_tech.split('_')[1]
            elif token == "{rep_tech}":
                return a_file.get("rep_tech", self.rep_for_file(a_file))
            else:
                return ""
        else:
            log.debug('Untranslated token: "%s"' % token)
            return "unknown"

    def convert_mask(self, mask, dataset=None, a_file=None):
        '''Given a mask with one or more known {term_name}s, replaces with values.'''
        working_on = mask
        # dataset might not be self.dataset
        if dataset is None:
            dataset = self.dataset
        chars = len(working_on)
        while chars > 0:
            beg_ix = working_on.find('{')
            if beg_ix == -1:
                break
            end_ix = working_on.find('}')
            if end_ix == -1:
                break
            term = self.lookup_token(working_on[beg_ix:end_ix+1], dataset, a_file=a_file)
            new_mask = []
            if beg_ix > 0:
                new_mask = working_on[0:beg_ix]
            new_mask += "%s%s" % (term, working_on[end_ix+1:])
            chars = len(working_on[end_ix+1:])
            working_on = ''.join(new_mask)

        return working_on

    def ucsc_single_composite_trackDb(self, vis_format, title):
        '''Given a single vis_format (vis_dataset or vis_by_type dict, returns single UCSC trackDb composite text'''
        if vis_format is None or len(vis_format) == 0:
            return "# Empty composite for %s.  It cannot be visualized at this time.\n" % title

        blob = ""
        # First the composite structure
        blob += "track %s\n" % vis_format["name"]
        blob += "compositeTrack on\n"
        blob += "type bed 3\n"
        for var in COMPOSITE_SETTINGS:
            val = vis_format.get(var)
            if val:
                blob += "%s %s\n" % (var, val)
        views = vis_format.get("view", [])
        if len(views) > 0:
            blob += "subGroup1 view %s" % views["title"]
            for view_tag in views["group_order"]:
                view_title = views["groups"][view_tag]["title"]
                blob += " %s=%s" % (view_tag, sanitize.title(view_title))
            blob += '\n'
        dimA_checked = vis_format.get("dimensionAchecked", "all")
        dimA_tag = ""
        if dimA_checked == "first":  # All will leave dimA_tag & dimA_checked empty, default to all on
            dimA_tag = vis_format.get("dimensions", {}).get("dimA", "")
        dimA_checked = None
        subgroup_ix = 2
        for group_tag in vis_format["group_order"]:
            group = vis_format["groups"][group_tag]
            blob += "subGroup%d %s %s" % (subgroup_ix, group_tag, sanitize.title(group["title"]))
            subgroup_ix += 1
            subgroup_order = None  # group.get("group_order")
            if subgroup_order is None or not isinstance(subgroup_order, list):
                subgroup_order = sorted(group["groups"].keys())
            for subgroup_tag in subgroup_order:
                subgroup_title = group["groups"][subgroup_tag]["title"]
                blob += " %s=%s" % (subgroup_tag, sanitize.title(subgroup_title))
                if group_tag == dimA_tag and dimA_checked is None:
                    dimA_checked = subgroup_tag

            blob += '\n'
        # sortOrder
        sort_order = vis_format.get("sortOrder")
        if sort_order:
            blob += "sortOrder"
            for sort_tag in sort_order:
                if title.startswith("ENCSR") and sort_tag == "EXP":
                    continue  # Single exp composites do not need to sort on EMP
                blob += " %s=+" % sort_tag
            blob += '\n'
        # dimensions
        actual_group_tags = ["view"]  # Not all groups will be used in composite, depending upon content
        dimensions = vis_format.get("dimensions", {})
        if dimensions:
            pairs = ""
            XY_skipped = []
            XY_added = []
            for dim_tag in sorted(dimensions.keys()):
                group = vis_format["groups"].get(dimensions[dim_tag])
                if group is None:  # e.g. "Targets" may not exist
                    continue
                if dimensions[dim_tag] != "REP":
                    if len(group.get("groups", {})) <= 1:
                        if dim_tag[-1] in ['X', 'Y']:
                            XY_skipped.append(dim_tag)
                        continue
                    elif dim_tag[-1] in ['X', 'Y']:
                        XY_added.append(dim_tag)
                pairs += " %s=%s" % (dim_tag, dimensions[dim_tag])
                actual_group_tags.append(dimensions[dim_tag])
            # Getting too fancy for our own good:
            # If one XY dimension has more than one member then we must add both X and Y
            if len(XY_skipped) > 0 and len(XY_added) > 0:
                for dim_tag in XY_skipped:
                    pairs += " %s=%s" % (dim_tag, dimensions[dim_tag])
                    actual_group_tags.append(dimensions[dim_tag])
            if len(pairs) > 0:
                blob += "dimensions%s\n" % pairs
        # filterComposite
        filter_composite = vis_format.get("filterComposite")
        if filter_composite:
            filterfish = ""
            for filter_tag in sorted(filter_composite.keys()):
                group = vis_format["groups"].get(filter_composite[filter_tag])
                if group is None or len(group.get("groups", {})) <= 1:  # e.g. "Targets" may not exist
                    continue
                filterfish += " %s" % filter_tag
                if filter_composite[filter_tag] == "one":
                    filterfish += "=one"
            if len(filterfish) > 0:
                blob += 'filterComposite%s\n' % filterfish
        elif dimA_checked is not None:
            blob += 'dimensionAchecked %s\n' % dimA_checked
        blob += '\n'

        # Now cycle through views
        for view_tag in views["group_order"]:
            view = views["groups"][view_tag]
            tracks = view.get("tracks", [])
            if len(tracks) == 0:
                continue
            blob += "    track %s_%s_view\n" % (vis_format["name"], view["tag"])
            blob += "    parent %s on\n" % vis_format["name"]
            blob += "    view %s\n" % view["tag"]
            for var in VIEW_SETTINGS:
                val = view.get(var)
                if val:
                    blob += "    %s %s\n" % (var, val)
            blob += '\n'

            # Now cycle through tracks in view
            for track in tracks:
                blob += "        track %s\n" % (track["name"])
                blob += "        parent %s_%s_view" % (vis_format["name"], view["tag"])
                dimA_subgroup = track.get("membership", {}).get(dimA_tag)
                if dimA_subgroup is not None and dimA_subgroup != dimA_checked:
                    blob += " off\n"
                else:
                    # Can set individual tracks off. Used when remodelling
                    blob += " %s\n" % track.get("checked", "on")
                if "type" not in track:
                    blob += "        type %s\n" % (view["type"])
                for var in TRACK_SETTINGS:
                    val = track.get(var)
                    if val:
                        blob += "        %s %s\n" % (var, val)
                # Now membership
                membership = track.get("membership")
                if membership:
                    blob += "        subGroups"
                    for member_tag in sorted(membership):
                        blob += " %s=%s" % (member_tag, membership[member_tag])
                    blob += '\n'
                # metadata line?
                metadata_pairs = track.get("metadata_pairs")
                if metadata_pairs is not None:
                    metadata_line = ""
                    for meta_tag in sorted(metadata_pairs.keys()):
                        metadata_line += ' %s=%s' % (meta_tag.lower(), metadata_pairs[meta_tag])
                    if len(metadata_line) > 0:
                        blob += "        metadata%s\n" % metadata_line

                blob += '\n'
        blob += '\n'
        return blob


# TODO: move to separate vis_cache module?
class VisCache(object):
    # Stores and recalls vis_dataset formatted json to/from es vis_cache

    def __init__(self, request):
        self.request = request
        self.es = self.request.registry.get(ELASTIC_SEARCH, None)
        self.index = VIS_CACHE_INDEX

    def create_cache(self):
        if not self.es:
            return None
        if not self.es.indices.exists(self.index):
            one_shard = {'index': {'number_of_shards': 1, 'max_result_window': 99999 }}
            mapping = {'default': {"enabled": False}}
            self.es.indices.create(index=self.index, body=one_shard, wait_for_active_shards=1)
            self.es.indices.put_mapping(index=self.index, doc_type='default', body=mapping)
            log.debug("created %s index" % self.index)

    def add(self, vis_id, vis_dataset):
        '''Adds a vis_dataset (aka vis_blob) json object to elastic-search'''
        if not self.es:
            return
        if not self.es.indices.exists(self.index):
            self.create_cache()  # Only bother creating on add

        self.es.index(index=self.index, doc_type='default', body=vis_dataset, id=vis_id)

    def get(self, vis_id=None, accession=None, assembly=None):
        '''Returns the vis_dataset json object from elastic-search, or None if not found.'''
        if vis_id is None and accession is not None and assembly is not None:
            vis_id = accession + '_' + ASSEMBLY_TO_UCSC_ID.get(assembly, assembly)
        if self.es:
            try:
                result = self.es.get(index=self.index, doc_type='default', id=vis_id)
                return result['_source']
            except:
                pass  # Missing index will return None
        return None

    def search(self, accessions, assembly):
        '''Returns a list of composites from elastic-search, or None if not found.'''
        if self.es:
            ucsc_assembly = ASSEMBLY_TO_UCSC_ID.get(assembly, assembly)  # Normalized accession
            vis_ids = [accession + "_" + ucsc_assembly for accession in accessions]
            try:
                query = {"query": {"ids": {"values": vis_ids}}}
                res = self.es.search(body=query, index=self.index, doc_type='default', size=99999)  # size=200?
                hits = res.get("hits", {}).get("hits", [])
                results = {}
                for hit in hits:
                    results[hit["_id"]] = hit["_source"]  # make this a generator? No... len(results)
                log.debug("ids found: %d" % (len(results)))
                return results
            except:
                pass
        return {}


# Not referenced in any other module
def visualizable_assemblies(
    assemblies,
    files,
    visible_statuses=VISIBLE_FILE_STATUSES
):
    '''Returns just the assemblies with visualizable files.'''
    file_assemblies = set()  # sets for comparing
    assemblies_set = set(assemblies)
    for afile in files:
        afile_assembly = afile.get('assembly')
        if afile_assembly is None or afile_assembly in file_assemblies:
            continue  # more efficient than simply relying on set()
        if (afile['status'] in visible_statuses and
                afile.get('file_format', '') in VISIBLE_FILE_FORMATS):
            file_assemblies.add(afile_assembly)
        if file_assemblies == assemblies_set:
            break  # Try not to go through the whole file list!
    return list(file_assemblies)


# Currently called in types/shared_calculated_properties.py
def browsers_available(
    status,
    assemblies,
    types,
    item_type=None,
    files=None,
    accession=None,
    request=None
):
    '''Returns list of browsers based upon vis_blobs or else files list.'''
    # NOTES:When called by visualize calculated property,
    #   vis_blob should be in vis_cache, but if not files are used.
    #       When called by visindexer, neither vis_cache nor files are
    #   used (could be called 'browsers_might_work').
    if "Dataset" not in types:
        return []
    if item_type is None:
        visualizabe_types = set(VISIBLE_DATASET_TYPES)
        if visualizabe_types.isdisjoint(types):
            return []
    elif item_type not in VISIBLE_DATASET_TYPES_LC:
            return []
    browsers = set()
    full_set = {'ucsc', 'ensembl', 'quickview'}
    file_assemblies = None
    if request is not None:
        vis_cache = VisCache(request)
    for assembly in assemblies:
        mapped_assembly = ASSEMBLY_DETAILS.get(assembly)
        if not mapped_assembly:
            continue
        vis_blob = None
        if (request is not None
                and accession is not None
                and status in VISIBLE_FILE_STATUSES):
            # use of find_or_make_acc_composite() will recurse!
            vis_blob = vis_cache.get(accession=accession, assembly=assembly)
        if not vis_blob and file_assemblies is None and files is not None:
            file_assemblies = visualizable_assemblies(assemblies, files)
        if ('ucsc' not in browsers
                and 'ucsc_assembly' in mapped_assembly.keys()):
            if vis_blob or files is None or assembly in file_assemblies:
                browsers.add('ucsc')
        if ('ensembl' not in browsers
                and 'ensembl_host' in mapped_assembly.keys()):
            if vis_blob or files is None or assembly in file_assemblies:
                browsers.add('ensembl')
        if ('quickview' not in browsers
                and 'quickview' in mapped_assembly.keys()):
            # NOTE: quickview may not have vis_blob as 'in progress'
            #   files can also be displayed
            #       Ideally we would also look at files' statuses and formats.
            #   However, the (calculated)files property only contains
            #   'released' files so it doesn't really help for quickview!
            if vis_blob is not None or status not in QUICKVIEW_STATUSES_BLOCKED:
                browsers.add('quickview')
        if browsers == full_set:  # No use continuing
            break
    return list(browsers)


# Currently called in visualization.py and in search.py
def object_is_visualizable(
    obj,
    assembly=None,
    check_files=False,
    exclude_quickview=False
):
    '''Returns true if it is likely that this object can be visualized.'''
    if 'accession' not in obj:
        return False
    if assembly is not None:
        assemblies = [ assembly ]
    else:
        assemblies = obj.get('assembly',[])
    files = None
    if check_files:
        # Returning [] instead of None is important
        files = obj.get('files', [])
    browsers = browsers_available(obj.get('status', 'none'),  assemblies,
                                  obj.get('@type', []), files=files)
    if exclude_quickview and 'quickview' in browsers:
        return len(browsers) > 1
    else:
        return len(browsers) > 0


# Currently called in types/shared_calculated_properties.py and in search.py
def vis_format_url(browser, path, assembly, position=None):
    '''Given a url to hub.txt, returns the url to an external browser or None.'''
    mapped_assembly = ASSEMBLY_DETAILS[assembly]
    if not mapped_assembly:
        return None
    if browser == "ucsc":
        ucsc_assembly = mapped_assembly.get('ucsc_assembly')
        if ucsc_assembly is not None:
            external_url = 'http://genome.ucsc.edu/cgi-bin/hgTracks?hubClear='
            external_url += path + '&db=' + ucsc_assembly
            if position is not None:
                external_url += '&position={}'.format(position)
            return external_url
    elif browser == "ensembl":
        ensembl_host = mapped_assembly.get('ensembl_host')
        if ensembl_host is not None:
            external_url = 'http://' + ensembl_host + '/Trackhub?url='
            external_url += path + ';species=' + mapped_assembly.get('species').replace(' ','_')
            ### TODO: remove redirect=no when Ensembl fixes their mirrors
            #external_url += ';redirect=no'
            ### TODO: remove redirect=no when Ensembl fixes their mirrors

            if position is not None:
                if position.startswith('chr'):
                    position = position[3:]  # ensembl position r=19:7069444-7087968
                external_url += '&r={}'.format(position)
            # GRCh38:   http://www.ensembl.org/Trackhub?url=https://www.encodeproject.org/experiments/ENCSR596NOF/@@hub/hub.txt
            # GRCh38:   http://www.ensembl.org/Trackhub?url=https://www.encodeproject.org/experiments/ENCSR596NOF/@@hub/hub.txt;species=Homo_sapiens
            # hg19/GRCh37:     http://grch37.ensembl.org/Trackhub?url=https://www.encodeproject.org/experiments/ENCSR596NOF/@@hub/hub.txt;species=Homo_sapiens
            # mm10/GRCm38:     http://www.ensembl.org/Trackhub?url=https://www.encodeproject.org/experiments/ENCSR475TDY@@hub/hub.txt;species=Mus_musculus
            # mm9/NCBIM37:      http://may2012.archive.ensembl.org/Trackhub?url=https://www.encodeproject.org/experiments/ENCSR000CNV@@hub/hub.txt;species=Mus_musculus
            # BDGP6:    http://www.ensembl.org/Trackhub?url=https://www.encodeproject.org/experiments/ENCSR040UNE@@hub/hub.txt;species=Drosophila_melanogaster
            # BDGP5:    http://dec2014.archive.ensembl.org/Trackhub?url=https://www.encodeproject.org/experiments/ENCSR040UNE@@hub/hub.txt;species=Drosophila_melanogaster
            # ce11/WBcel235: http://www.ensembl.org/Trackhub?url=https://www.encodeproject.org/experiments/ENCSR475TDY@@hub/hub.txt;species=Caenorhabditis_elegans
            return external_url
    elif browser == "quickview":
        file_formats = '&file_format=bigBed&file_format=bigWig'
        file_inclusions = '&status=released&status=in+progress'
        return ('/search/?type=File&assembly=%s&dataset=%s%s%s#browser' % (assembly,path,file_formats,file_inclusions))
    #else:
        # ERROR: not supported at this time
    return None

