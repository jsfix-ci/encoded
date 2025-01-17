from snovault import (
    CONNECTION,
    upgrade_step,
)
from pyramid.traversal import find_root
from datetime import datetime, time


@upgrade_step('file', '', '2')
def file_0_2(value, system):
    # http://redmine.encodedcc.org/issues/1295
    # http://redmine.encodedcc.org/issues/1307
    if 'status' in value:
        value['status'] = value['status'].lower()


@upgrade_step('file', '2', '3')
def file_2_3(value, system):
    #  http://redmine.encodedcc.org/issues/1572
    file_format = value.get('file_format')
    file_name = value['download_path'].rsplit('/', 1)[-1]
    file_ext = file_name[file_name.find('.'):]

    # REJECTIONS
    if file_ext in ['.gtf.bigBed', '.pdf', '.pdf.gz', '.gff.bigBed', '.spikeins']:
        value['status'] = 'deleted'

    # Find the miscatorgorized bedMethyls
    if file_ext == '.bed.bigBed' and 'MethylRrbs' in value.get('submitted_file_name'):
        value['file_format'] = 'bedMethyl'
    if file_ext == '.bed.gz' and 'MethylRrbs' in value.get('submitted_file_name'):
        value['file_format'] = 'bed_bedMethyl'

    unknownDict = {'.CEL.gz': 'CEL',
                    '.bb': 'bedMethyl',
                    '.bed': 'bed',
                    '.bed.gz': 'bed',
                    '.bed.bigBed': 'bigBed',
                    '.bigBed': 'bigBed',
                    '.bed9': 'bedMethyl',
                    '.bed9.gz': 'bed_bedMethyl',
                    '.bedCluster.bigBed': 'bigBed',
                    '.bedLogR.bigBed': 'bedLogR',
                    '.bedRnaElements.bigBed': 'bedRnaElements',
                    '.bedRrbs.bigBed': 'bedMethyl',
                    '.broadPeak.gz': 'bed_broadPeak',
                    '.bigBed': 'bigBed',
                    '.csfasta.gz': 'csfasta',
                    '.csqual.gz': 'csqual',
                    '.fasta.gz': 'fasta',
                    '.gff.bigBed': 'bigBed',
                    '.gff.gz': 'gtf',
                    '.gp.bigBed': 'bigBed',
                    '.matrix.gz': 'tsv',
                    '.matrix.tgz': 'tar',
                    '.narrowPeak': 'bed_narrowPeak',
                    '.narrowPeak.gz': 'bed_narrowPeak',
                    '.pdf': 'tsv',  # These are going to be obsolete
                    '.pdf.gz': 'tsv',  # These are going to be obsolete
                    '.peaks.gz': 'tsv',
                    '.peptideMapping.bigBed': 'bigBed',
                    '.shortFrags.bigBed': 'bigBed',
                    '.sorted.bigBed': 'bigBed',
                    '.tab.gz': 'tsv',
                    '.tgz': 'tar',
                    '.txt': 'tsv',
                    '.xlsx': 'tsv',  # These need to be converted to tsv
                   }
    if file_format in ['unknown', 'customTrack']:
        value['file_format'] = unknownDict[file_ext]

    # http://redmine.encodedcc.org/issues/1429

    context = system['context']
    root = find_root(context)
    dataset = root.get_by_uuid(value['dataset']).upgrade_properties()

    dataset_status = dataset.get('status')
    status = value.get('status')

    if status == 'current':
        if dataset_status == 'released':
            value['status'] = 'released'
        else:
            value['status'] = 'in progress'

    if status == 'obsolete':
        if dataset_status in ['released', 'revoked']:
            value['status'] = 'revoked'
        else:
            value['status'] = 'deleted'

    # http://redmine.encodedcc.org/issues/568
    output_type_dict = {
                        '': 'raw data',
                        'Alignments': 'alignments',
                        'bigBed': 'sites',
                        'bigWig': 'sites',
                        'Clusters': 'clusters',
                        'Contigs': 'contigs',
                        'FastqRd1': 'reads',
                        'FastqRd2': 'reads',
                        'forebrain_enhancers': 'enhancers_forebrain',
                        'heart_enhancers': 'enhancers_heart',
                        'GreenIdat': 'idat green file',
                        'hotspot_broad_peaks': 'hotspots',
                        'hotspot_narrow_peaks': 'hotspots',
                        'hotspot_signal': 'hotspots',
                        'Hotspots': 'hotspots',
                        'Interactions': 'interactions',
                        'MinusRawSignal': 'raw minus signal',
                        'PlusRawSignal': 'raw plus signal',
                        'macs2_dnase_peaks': 'peaks',
                        'macs2_dnase_signal': 'signal',
                        'MinusSignal': 'minus signal',
                        'minusSignal': 'minus signal',
                        'MultiMinus': 'multi-read minus signal',
                        'MultiPlus': 'multi-read plus signal',
                        'MultiSignal': 'multi-read signal',
                        'MultiUnstranded': 'multi-read signal',
                        'RawData2': 'reads',
                        'RedIdat': 'idat red file',
                        'peak': 'peaks',
                        'PeakCalls': 'peaks',
                        'Peaks': 'peaks',
                        'PlusSignal': 'plus signal',
                        'plusSignal': 'plus signal',
                        'predicted_enhancers_heart': 'enhancers_heart',
                        'RawSignal': 'raw signal',
                        'RawData': 'raw data',
                        'rcc': 'raw data',
                        'Read': 'reads',
                        'read': 'reads',
                        'read1': 'reads',
                        'rejected_reads': 'rejected reads',
                        'RepPeaks': 'peaks',
                        'RepSignal': 'signal',
                        'Signal': 'signal',
                        'SimpleSignal': 'signal',
                        'Sites': 'sites',
                        'Spikeins': 'spike-ins',
                        'Spikes': 'spike-ins',
                        'Splices': 'splice junctions',
                        'uniqueReads': 'unique signal',
                        'UniqueSignal': 'unique signal',
                        'uniqueSignal': 'unique signal',
                        'UniqueMinus': 'unique minus signal',
                        'uniqueMinusSignal': 'unique minus signal',
                        'UniquePlus': 'unique plus signal',
                        'uniquePlusSignal': 'unique plus signal',
                        'UniqueUnstranded': 'unique signal',
                        'UnstrandedSignal': 'signal',
                        'dataset_used': 'enhancers',
                        'TRAINING_DATA_MOUSE_VISTA': 'enhancers',
                        'method_description': 'enhancers',
                        'unknown': 'enhancers',
                        'Protocol': 'raw data',
                        }

    current_output_type = value['output_type']
    if current_output_type in output_type_dict:
        value['output_type'] = output_type_dict[current_output_type]

    # Help the raw data problem
    if value['output_type'] == 'raw data' and value['file_format'] == 'fastq':
        value['output_type'] = 'reads'


@upgrade_step('file', '3', '4')
def file_3_4(value, system):
    #  http://redmine.encodedcc.org/issues/1714

    context = system['context']
    root = find_root(context)
    dataset = root.get_by_uuid(value['dataset']).upgrade_properties()

    if 'download_path' in value:
        value.pop('download_path')

    value['lab'] = dataset['lab']
    value['award'] = dataset['award']

    # EDW User
    if value.get('submitted_by') == '0e04cd39-006b-4b4a-afb3-b6d76c4182ff':
        value['lab'] = 'fb0af3d0-3a4c-4e96-b67a-f273fe527b04'
        value['award'] = '8bafd685-aa17-43fe-95aa-37bc1c90074a'


@upgrade_step('file', '4', '5')
def file_4_5(value, system):
    #  http://redmine.encodedcc.org/issues/2566
    #  http://redmine.encodedcc.org/issues/2565
    # we need to remeber  bedRnaElements,

    bed_files = {
        'bed_bedLogR': 'bedLogR',
        'bed_bedMethyl': 'bedMethyl',
        'bed_broadPeak': 'broadPeak',
        'bed_gappedPeak': 'gappedPeak',
        'bed_narrowPeak': 'narrowPeak',
        'bed_bedRnaElements': 'bedRnaElements'
    }

    bigBed_files = [
        'bedLogR',
        'bedMethyl',
        'broadPeak',
        'narrowPeak',
        'gappedPeak',
        'bedRnaElements'
    ]

    current = value['file_format']

    if current in ['bed', 'bigBed']:
        value['file_format_type'] = 'unknown'
        # we do not know what those formats were,  wranglers  will need to investigate
    elif current in bigBed_files:
        value['file_format_type'] = current
        value['file_format'] = 'bigBed'
    elif current in bed_files:
        value['file_format_type'] = bed_files[current]
        value['file_format'] = 'bed'
    elif current in ['gff']:
        value['file_format_type'] = 'unknown'
        # all gffs todate were in gff3, but we wouldn't know without wranglers checking

    # classify the peptide stuff
    if value['output_type'] in ['mPepMapGcFt', 'mPepMapGcUnFt']:
        value['file_format_type'] = 'modPepMap'
    elif value['output_type'] in ['pepMapGcFt', 'pepMapGcUnFt']:
        value['file_format_type'] = 'pepMap'

    #  http://redmine.encodedcc.org/issues/2565
    output_mapping = {
        # Category: Raw data
        'idat green file': 'idat green channel',
        'idat red file': 'idat red channel',
        'reads': 'reads',
        'rejected reads': 'rejected reads',
        'rcc': 'reporter code counts',
        'CEL': 'intensity values',
        'raw data': 'raw data',

        'alignments': 'alignments',
        'transcriptome alignments': 'transcriptome alignments',
        'spike-ins': 'spike-in alignments',

        'multi-read minus signal': 'minus strand signal of multi-mapped reads',
        'multi-read plus signal': 'plus strand signal of multi-mapped reads',
        'multi-read signal': 'signal of multi-mapped reads',
        'multi-read normalized signal': 'normalized signal of multi-mapped reads',
        'raw minus signal': 'raw minus strand signal',
        'raw plus signal': 'raw plus strand signal',
        'raw signal': 'raw signal',
        'raw normalized signal': 'raw normalized signal',
        'unique minus signal': 'minus strand signal of unique reads',
        'unique plus signal': 'plus strand signal of unique reads',
        'unique signal': 'signal of unique reads',
        'signal': 'signal',
        'minus signal': 'minus strand signal',
        'plus signal': 'plus strand signal',
        'Base_Overlap_Signal': 'base overlap signal',
        'PctSignal': 'percentage normalized signal',
        'SumSignal': 'summed densities signal',
        'WaveSignal': 'wavelet-smoothed signal',
        'signal p-value': 'signal p-value',
        'fold change over control': 'fold change over control',

        'enrichment': 'enrichment',
        'exon quantifications': 'exon quantifications',
        'ExonsDeNovo': 'exon quantifications',
        'ExonsEnsV65IAcuff': 'exon quantifications',
        'ExonsGencV10': 'exon quantifications',
        'ExonsGencV3c': 'exon quantifications',
        'ExonsGencV7': 'exon quantifications',
        'GeneDeNovo': 'gene quantifications',
        'GeneEnsV65IAcuff': 'gene quantifications',
        'GeneGencV10': 'gene quantifications',
        'GeneGencV3c': 'gene quantifications',
        'GeneGencV7': 'gene quantifications',
        'genome quantifications': 'gene quantifications',
        'library_fraction': 'library fraction',
        'transcript quantifications': 'transcript quantifications',
        'TranscriptDeNovo': 'transcript quantifications',
        'TranscriptEnsV65IAcuff': 'transcript quantifications',
        'TranscriptGencV10': 'transcript quantifications',
        'TranscriptGencV3c': 'transcript quantifications',
        'TranscriptGencV7': 'transcript quantifications',
        'mPepMapGcFt': 'filtered modified peptide quantification',
        'mPepMapGcUnFt': 'unfiltered modified peptide quantification',
        'pepMapGcFt': 'filtered peptide quantification',
        'pepMapGcUnFt': 'unfiltered peptide quantification',

        'clusters': 'clusters',
        'CNV': 'copy number variation',
        'contigs': 'contigs',
        'enhancer validation': 'enhancer validation',
        'FiltTransfrags': 'filtered transcribed fragments',
        'hotspots': 'hotspots',
        'Junctions': 'splice junctions',
        'interactions': 'long range chromatin interactions',
        'Matrix': 'long range chromatin interactions',
        'PrimerPeaks': 'long range chromatin interactions',
        'sites': 'methylation state at CpG',
        'methyl CG': 'methylation state at CpG',
        'methyl CHG': 'methylation state at CHG',
        'methyl CHH': 'methylation state at CHH',
        'peaks': 'peaks',
        'replicated peaks': 'replicated peaks',
        'RbpAssocRna': 'RNA-binding protein associated mRNAs',
        'splice junctions': 'splice junctions',
        'Transfrags': 'transcribed fragments',
        'TssGencV3c': 'transcription start sites',
        'TssGencV7': 'transcription start sites',
        'Valleys': 'valleys',
        'Alignability': 'sequence alignability',
        'Excludable': 'blacklisted regions',
        'Uniqueness': 'sequence uniqueness',

        'genome index': 'genome index',
        'genome reference': 'genome reference',
        'Primer': 'primer sequence',
        'spike-in sequence': 'spike-in sequence',
        'reference': 'reference',

        'enhancers': 'predicted enhancers',
        'enhancers_forebrain': 'predicted forebrain enhancers',
        'enhancers_heart': 'predicted heart enhancers',
        'enhancers_wholebrain': 'predicted whole brain enhancers',
        'TssHmm': 'predicted transcription start sites',
        'UniformlyProcessedPeakCalls': 'optimal idr thresholded peaks',
        'Validation': 'validation',
        'HMM': 'HMM predicted chromatin state'
    }

    old_output_type = value['output_type']

    # The peptide mapping files from UCSC all assumed V10 hg19
    if old_output_type in ['mPepMapGcFt', 'mPepMapGcUnFt', 'pepMapGcFt', 'pepMapGcUnFt']:
        value['genome_annotation'] = 'V10'
        value['assembly'] = 'hg19'

    elif old_output_type in ['ExonsEnsV65IAcuff', 'GeneEnsV65IAcuff', 'TranscriptEnsV65IAcuff']:
        value['genome_annotation'] = 'ENSEMBL V65'

    elif old_output_type in ['ExonsGencV3c', 'GeneGencV3c', 'TranscriptGencV3c', 'TssGencV3c']:
        value['genome_annotation'] = 'V3c'

    elif old_output_type in ['ExonsGencV7', 'GeneGenc7', 'TranscriptGencV7', 'TssGencV7']:
        value['genome_annotation'] = 'V7'

    elif old_output_type in ['ExonsGencV10', 'GeneGenc10', 'TranscriptGencV10', 'TssGencV10']:
        value['genome_annotation'] = 'V10'

    elif old_output_type in ['spike-ins'] and value['file_format'] == 'fasta':
        old_output_type = 'spike-in sequence'

    elif old_output_type in ['raw data'] and value['file_format'] in ['fastq', 'csfasta', 'csqual', 'fasta']:
        old_output_type = 'reads'

    elif old_output_type in ['raw data'] and value['file_format'] in ['CEL', 'tar']:
        old_output_type = 'CEL'

    elif old_output_type in ['raw data'] and value['file_format'] in ['rcc']:
        old_output_type = 'rcc'

    elif old_output_type in ['raw data'] and value['lab'] == '/labs/timothy-hubbard/':
        old_output_type = 'reference'

    elif old_output_type in ['raw data']:
        if 'These are protocol documents' in value.get('notes', ''):
            old_output_type = 'reference'

    elif old_output_type == 'sites' and value['file_format'] == 'tsv':
        old_output_type = 'interactions'

    elif old_output_type in ['Validation'] and value['file_format'] == '2bit':
        old_output_type = 'genome reference'

    value['output_type'] = output_mapping[old_output_type]

    #  label the lost bedRnaElements files #2940
    bedRnaElements_files = [
        'transcript quantifications',
        'gene quantifications',
        'exon quantifications'
        ]
    if (
        value['output_type'] in bedRnaElements_files
        and value['status'] in ['deleted', 'replaced']
        and value['file_format'] == 'bigBed'
        and value['file_format_type'] == 'unknown'
    ):
        value['file_format_type'] = 'bedRnaElements'

    #  Get the replicate information
    if value.get('file_format') in ['fastq', 'fasta', 'csfasta']:
        context = system['context']
        root = find_root(context)
        if 'replicate' in value:
            replicate = root.get_by_uuid(value['replicate']).upgrade_properties()

            if 'read_length' not in value:
                value['read_length'] = replicate.get('read_length')
                if value['read_length'] is None:
                    del value['read_length']

            run_type_dict = {
                True: 'paired-ended',
                False: 'single-ended',
                None: 'unknown'
            }
            if 'run_type' not in value:
                value['run_type'] = run_type_dict[replicate.get('paired_ended')]

        if value.get('paired_end') in ['2']:
            value['run_type'] = 'paired-ended'

    # Backfill content_md5sum #2683
    if 'content_md5sum' not in value:
        md5sum_content_md5sum = system['registry'].get('backfill_2683', {})
        if value['md5sum'] in md5sum_content_md5sum:
            value['content_md5sum'] = md5sum_content_md5sum[value['md5sum']]


@upgrade_step('file', '5', '6')
def file_5_6(value, system):
    #  http://redmine.encodedcc.org/issues/3019

    import re

    if value.get('output_type') in [
            'minus strand signal of multi-mapped reads',
            'plus strand signal of multi-mapped reads',
            'signal of multi-mapped reads',
            'normalized signal of multi-mapped reads'
            ]:

        value['output_type'] = re.sub('multi-mapped', 'all', value['output_type'])


@upgrade_step('file', '6', '7')
def file_6_7(value, system):
    # http://redmine.encodedcc.org/issues/3063
    if 'file_format_specifications' in value:
        value['file_format_specifications'] = list(set(value['file_format_specifications']))

    if 'controlled_by' in value:
        value['controlled_by'] = list(set(value['controlled_by']))

    if 'derived_from' in value:
        value['derived_from'] = list(set(value['derived_from']))

    if 'supercedes' in value:
        value['supercedes'] = list(set(value['supersedes']))

    if 'aliases' in value:
        value['aliases'] = list(set(value['aliases']))


@upgrade_step('file', '7', '8')
def file_7_8(value, system):
    return


@upgrade_step('file', '8', '9')
def file_8_9(value, system):

    # http://redmine.encodedcc.org/issues/4183
    if (value['file_format'] == 'fastq') and ('assembly' in value):
        value.pop('assembly')

    # http://redmine.encodedcc.org/issues/1859
    if 'supercedes' in value:
        value['supersedes'] = value['supercedes']
        value.pop('supercedes', None)


def set_to_midnight(date_string):
    release_date = datetime.strptime(date_string, '%Y-%m-%d')
    min_pub_date_time = datetime.combine(release_date, time.min)
    return '{:%Y-%m-%dT%H:%M:%S.%f+00:00}'.format(min_pub_date_time)


@upgrade_step('file', '9', '10')
def file_9_10(value, system):
    # http://redmine.encodedcc.org/issues/5021
    # http://redmine.encodedcc.org/issues/4929
    # http://redmine.encodedcc.org/issues/4927
    # http://redmine.encodedcc.org/issues/4903
    # http://redmine.encodedcc.org/issues/4904

    date_created = value.get('date_created')
    if date_created.find('T') == -1:
        value['date_created'] = set_to_midnight(date_created)

    # http://redmine.encodedcc.org/issues/4748
    aliases = []
    if 'aliases' in value and value['aliases']:
        aliases = value['aliases']
    else:
        return

    aliases_to_remove = []
    for i in range(0, len(aliases)):
        new_alias = ''
        if 'roadmap-epigenomics' in aliases[i]:
            if '||' in aliases[i]:
                scrub_parts = aliases[i].split('||')
                date_split = scrub_parts[1].split(' ')
                date = "-".join([date_split[1].strip(),
                                date_split[2].strip(),
                                date_split[5].strip()])
                scrubbed_list = [scrub_parts[0].strip(), date.strip(), scrub_parts[2].strip()]
                if len(scrub_parts) == 4:
                    scrubbed_list.append(scrub_parts[3].strip())
                new_alias = '_'.join(scrubbed_list)
        parts = aliases[i].split(':') if not new_alias else new_alias.split(':')
        namespace = parts[0]
        if namespace in ['ucsc_encode_db', 'UCSC_encode_db', 'versionof']:
            # Remove the alias with the bad namespace
            aliases_to_remove.append(aliases[i])
            namespace = 'encode'
        if namespace in ['CGC']:
            namespace = namespace.lower()

        rest = '_'.join(parts[1:]).strip()
        # Remove or substitute bad characters and multiple whitespaces

        import re
        if '"' or '#' or '@' or '!' or '$' or '^' or '&' or '|' or '~'  or ';' or '`' in rest:
            rest = re.sub(r'[\"#@!$^&|~;`\/\\]', '', rest)
            rest = ' '.join(rest.split())
        if '%' in rest:
            rest = re.sub(r'%', 'pct', rest)
        if '[' or '{' in rest:
            rest = re.sub(r'[\[{]', '(', rest)
        if ']' or '}' in rest:
            rest = re.sub(r'[\]}]', ')', rest)

        new_alias = ':'.join([namespace, rest])
        if new_alias not in aliases:
            aliases[i] = new_alias

    if aliases_to_remove and aliases:
        for a in aliases_to_remove:
            if a in aliases:
                aliases.remove(a)


@upgrade_step('file', '10', '11')
def file_10_11(value, system):
    # http://redmine.encodedcc.org/issues/5049
    # http://redmine.encodedcc.org/issues/5081
    # http://redmine.encodedcc.org/issues/4924
    if not value.get('no_file_available'):
        value['no_file_available'] = False

    # The above change also required the files whose values should be set to True
    # to also be upgraded or patched. The patch was applied post-release and 
    # can be found in ./upgrade_data/file_10_to_11_patch.tsv


@upgrade_step('file', '11', '12')
def file_11_12(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-3347
    return


@upgrade_step('file', '12', '13')
def file_12_13(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-3809
    platform = value.get('platform', None)

    if platform and platform in [
        "ced61406-dcc6-43c4-bddd-4c977cc676e8",
        "c7564b38-ab4f-4c42-a401-3de48689a998"
        ]:        
            value.pop('read_length', None)
            value.pop('run_type', None)
    return


@upgrade_step('file', '13', '14')
def file_13_14(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-4613
    output_type = value.get('output_type', None)

    if output_type and output_type == 'candidate regulatory elements':
        value['output_type'] = 'candidate Cis-Regulatory Elements'


@upgrade_step('file', '14', '15')
def file_14_15(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-4641
    output_type = value.get('output_type', None)

    if output_type and output_type == 'optimal idr thresholded peaks':
        value['output_type'] = 'optimal IDR thresholded peaks'
    elif output_type and output_type == 'conservative idr thresholded peaks':
        value['output_type'] = 'conservative IDR thresholded peaks'
    elif output_type and output_type == 'pseudoreplicated idr thresholded peaks':
        value['output_type'] = 'pseudoreplicated IDR thresholded peaks'


@upgrade_step('file', '15', '16')
def file_15_16(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-4921
    platform = value.get('platform', None)

    if platform == "e2be5728-5744-4da4-8881-cb9526d0389e":
            value.pop('read_length', None)
            value.pop('run_type', None)
    return

@upgrade_step('file', '16', '17')
def file_16_17(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5050
    platform = value.get('platform', None)

    if platform and platform in [
        "6c275b37-018d-4bf8-85f6-6e3b830524a9",
        "8f1a9a8c-3392-4032-92a8-5d196c9d7810"
        ]:
            value.pop('read_length', None)
            value.pop('run_type', None)
    return


@upgrade_step('file', '17', '18')
def file_17_18(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5087
    output_type = value.get('output_type', None)

    if output_type == "subreads" and 'assembly' in value:
        value.pop('assembly', None)
    return


@upgrade_step('file', '18', '19')
def file_18_19(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5232
    output_type = value.get('output_type', None)

    if output_type == "representative dnase hypersensitivity sites":
        value['output_type'] = 'representative DNase hypersensitivity sites (rDHSs)'
    return


@upgrade_step('file', '19', '20')
def file_19_20(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5258
    platforms_to_exclude = [
        'ced61406-dcc6-43c4-bddd-4c977cc676e8',
        'c7564b38-ab4f-4c42-a401-3de48689a998',
        'e2be5728-5744-4da4-8881-cb9526d0389e',
        '6c275b37-018d-4bf8-85f6-6e3b830524a9',
        '8f1a9a8c-3392-4032-92a8-5d196c9d7810'
    ]
    formats_to_check = ['fastq', 'sra']
    file_format = value.get('file_format', None)
    platform = value.get('platform', None)
    run_type = value.get('run_type', None)
    notes = value.get('notes', '')

    if file_format in formats_to_check and \
            run_type is None and \
            platform not in platforms_to_exclude:
        value['run_type'] = 'single-ended'
        value['notes'] = (notes + ' The run_type of this file was automatically upgraded by ENCD-5258.').strip()
    return


@upgrade_step('file', '20', '21')
def file_20_21(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5271
    output_type = value.get('output_type', None)

    conn = system['registry'][CONNECTION]
    datasetContext = conn.get_by_uuid(value['dataset'])
    assay_type = datasetContext.properties.get('assay_term_name', None)

    if assay_type == 'DNase-seq' and output_type == 'enrichment':
        value['output_type'] = 'FDR cut rate'
    return


@upgrade_step('file', '21', '22')
def file_21_22(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5286
    output_type = value.get('output_type', None)
    notes = value.get('notes', '')
    if output_type == 'subreads':
        if 'replicate' not in value:
            value['replicate'] = '70d6e704-bba5-4475-97b8-03bf717eecf3'
            value['notes'] = notes + ' This file lacks its correct replicate specified.'


@upgrade_step('file', '22', '23')
def file_22_23(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5424
    output_type = value.get('output_type', None)
    if output_type == 'spike-in sequence':
        value['output_type'] = 'spike-ins'
    return


@upgrade_step('file', '23', '24')
def file_23_24(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5480
    if value.get('output_type', '') == 'stable peaks':
        value['output_type'] = 'pseudo-replicated peaks'


@upgrade_step('file', '24', '25')
def file_24_25(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5480
    if value.get('output_type', '') == 'smoothed methylation stage at CpG':
        value['output_type'] = 'smoothed methylation state at CpG'


@upgrade_step('file', '25', '26')
def file_25_26(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5573
    output_type = value.get('output_type', None)

    if output_type == "representative DNase hypersensitivity sites (rDHSs)":
        value['output_type'] = 'representative DNase hypersensitivity sites'
    elif output_type == "consensus DNase hypersensitivity sites (cDHSs)":
        value['output_type'] = 'consensus DNase hypersensitivity sites'
    return


@upgrade_step('file', '26', '27')
def file_26_27(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5662
    if value.get('output_type', '') == 'pseudo-replicated peaks':
        value['output_type'] = 'pseudoreplicated peaks'
    return


@upgrade_step('file', '27', '28')
def file_27_28(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5657
    term_pairs = [
        ('blacklisted regions', 'exclusion list regions'), 
        ('mitochondria blacklisted regions', 'mitochondrial exclusion list regions'),
    ]
    output_type = value.get('output_type', None)
    for old_term, new_term in term_pairs:
        if output_type == old_term:
            value['output_type'] = new_term


@upgrade_step('file', '28', '29')
def file_28_29(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5975
    platform = value.get('platform', None)

    if platform == "25acccbd-cb36-463b-ac96-adbac11227e6":
            value.pop('read_length', None)
    return


@upgrade_step('file', '29', '30')
def file_29_30(value, system):
    # https://igvf.atlassian.net/browse/ENCM-97
    term_pairs = [
        ('topologically associated domains', 'contact domains'),
        ('mapping quality thresholded chromatin interactions', 'mapping quality thresholded contact matrix'),
        ('chromatin interactions', 'contact matrix'),
        ('DNA accessibility raw signal', 'nuclease cleavage frequency'),
        ('long range chromatin interactions', 'loops'),
        ('nested topologically associated domains', 'nested contact domains'),
        ('allele-specific chromatin interactions', 'allele-specific contact domain'),
        ('variants chromatin interactions', 'variants contact matrix'),
        ('haplotype-specific chromatin interactions', 'haplotype-specific contact matrix'),
        ('haplotype-specific DNA accessibility raw signal', 'haplotype-specific nuclease cleavage frequency'),
        ('haplotype-specific DNA accessibility corrected signal', 'haplotype-specific nuclease cleavage corrected frequency')
    ]
    output_type = value.get('output_type', None)
    for old_term, new_term in term_pairs:
        if output_type == old_term:
            value['output_type'] = new_term
