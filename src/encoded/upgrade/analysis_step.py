from snovault import upgrade_step
from .upgrade_data.analysis_step_5_to_6 import (
    label_mapping,
    status_mapping,
    title_mapping,
    major_version_mapping,
    aliases_mapping
)


@upgrade_step('analysis_step', '1', '2')
def analysis_step_1_2(value, system):
    # http://redmine.encodedcc.org/issues/2770

    input_mapping = {
        'align-star-pe-v-1-0-2': ['reads'],
        'align-star-pe-v-2-0-0': ['reads'],
        'align-star-se-v-1-0-2': ['reads'],
        'align-star-se-v-2-0-0': ['reads'],
        'index-star-v-1-0-1': ['genome reference', 'spike-in sequence', 'reference genes'],
        'index-star-v-2-0-0': ['genome reference', 'spike-in sequence', 'reference genes'],
        'index-rsem-v-1-0-1': ['genome reference', 'spike-in sequence', 'reference genes'],
        'index-tophat-v-1-0-0': ['genome reference', 'spike-in sequence', 'reference genes'],
        'quant-rsem-v-1-0-2': ['transcriptome alignments'],
        'stranded-signal-star-v-1-0-1': ['alignments'],
        'stranded-signal-star-v-2-0-0': ['alignments'],
        'unstranded-signal-star-v-1-0-1': ['alignments'],
        'unstranded-signal-star-v-2-0-0': ['alignments'],
        'align-tophat-pe-v-1-0-1': ['reads'],
        'align-tophat-se-v-1-0-1': ['reads']
    }
    output_mapping = {
        'align-star-pe-v-1-0-2': ['alignments'],
        'align-star-pe-v-2-0-0': ['alignments'],
        'align-star-se-v-1-0-2': ['alignments'],
        'align-star-se-v-2-0-0': ['alignments'],
        'index-star-v-1-0-1': ['genome index'],
        'index-star-v-2-0-0': ['genome index'],
        'index-rsem-v-1-0-1': ['genome index'],
        'index-tophat-v-1-0-0': ['genome index'],
        'quant-rsem-v-1-0-2': ['gene quantifications'],
        'stranded-signal-star-v-1-0-1': [
            'minus strand signal of multi-mapped reads',
            'plus strand signal of multi-mapped reads',
            'minus strand signal of unique reads',
            'plus strand signal of unique reads'
        ],
        'stranded-signal-star-v-2-0-0': [
            'minus strand signal of multi-mapped reads',
            'plus strand signal of multi-mapped reads',
            'minus strand signal of unique reads',
            'plus strand signal of unique reads'
        ],
        'unstranded-signal-star-v-1-0-1': [
            'signal of multi-mapped reads',
            'signal of unique reads'
        ],
        'unstranded-signal-star-v-2-0-0': [
            'signal of multi-mapped reads',
            'signal of unique reads'
        ],
        'align-tophat-pe-v-1-0-1': ['alignments'],
        'align-tophat-se-v-1-0-1': ['alignments']
    }

    value['input_file_types'] = input_mapping[value['name']]
    value['output_file_types'] = output_mapping[value['name']]


@upgrade_step('analysis_step', '2', '3')
def analysis_step_2_3(value, system):
    # http://redmine.encodedcc.org/issues/3019

    import re

    if 'output_file_types' in value:
        for i in range(0, len(value['output_file_types'])):
            string = value['output_file_types'][i]
            value['output_file_types'][i] = re.sub('multi-mapped', 'all', string)
    if 'input_file_types' in value:
        for i in range(0, len(value['input_file_types'])):
            string = value['input_file_types'][i]
            value['input_file_types'][i] = re.sub('multi-mapped', 'all', string)

    # http://redmine.encodedcc.org/issues/3074
    del value['software_versions']

    # http://redmine.encodedcc.org/issues/3074 note 16 and 3073
    if value.get('name') in ['lrna-se-star-alignment-step-v-2-0',
                            'lrna-pe-star-alignment-step-v-2-0',
                            'lrna-pe-star-stranded-signal-step-v-2-0',
                            'lrna-pe-star-stranded-signals-for-tophat-step-v-2-0',
                            'lrna-se-star-unstranded-signal-step-v-2-0',
                            'lrna-se-star-unstranded-signals-for-tophat-step-v-2-0',
                            'index-star-v-2-0',
                            'rampage-grit-peak-calling-step-v-1-1'
                            ]:
        value['status'] = 'deleted'

    if value.get('name') == 'lrna-pe-rsem-quantification-v-1':
        value['parents'] = ['ace7163c-563a-43d6-a86f-686405af167d', #/analysis-steps/lrna-pe-star-alignment-step-v-1/'
                            '9ca04da2-5ef7-4ba1-b78c-41dfc4be0c11'  #/analysis-steps/index-rsem-v-1-0/'
                            ]
    elif value.get('name') == 'lrna-se-rsem-quantification-step-v-1':
        value['parents'] = ['3cad3827-7f21-4f70-9cbc-e718b5529775', #/analysis-steps/lrna-se-star-alignment-step-v-1/',
                            '9ca04da2-5ef7-4ba1-b78c-41dfc4be0c11'  #/analysis-steps/index-rsem-v-1-0/'
                            ]


@upgrade_step('analysis_step', '3', '4')
def analysis_step_3_4(value, system):
    # http://redmine.encodedcc.org/issues/3063
    if 'analysis_step_types' in value:
        value['analysis_step_types'] = list(set(value['analysis_step_types']))

    if 'input_file_types' in value:
        value['input_file_types'] = list(set(value['input_file_types']))

    if 'output_file_types' in value:
        value['output_file_types'] = list(set(value['output_file_types']))

    if 'qa_stats_generated' in value:
        value['qa_stats_generated'] = list(set(value['qa_stats_generated']))

    if 'parents' in value:
        value['parents'] = list(set(value['parents']))

    if 'aliases' in value:
        value['aliases'] = list(set(value['aliases']))

    if 'documents' in value:
        value['documents'] = list(set(value['documents']))


@upgrade_step('analysis_step', '5', '6')
def analysis_step_5_6(value, system):
    # http://redmine.encodedcc.org/issues/4987

    obj_aliases = value.get('aliases', None)
    if obj_aliases:
        if obj_aliases[0] in label_mapping:
            value['step_label'] = label_mapping[obj_aliases[0]]
        else:
            value['step_label'] = value['name']
        value.pop('name', None)
        if obj_aliases[0] in major_version_mapping:
            value['major_version'] = major_version_mapping[obj_aliases[0]]
        if obj_aliases[0] in title_mapping:
            value['title'] = title_mapping[obj_aliases[0]]
        if obj_aliases[0] in status_mapping:
            value['status'] = status_mapping[obj_aliases[0]]
        if obj_aliases[0] in aliases_mapping:
            value['aliases'].append(aliases_mapping[obj_aliases[0]])

    # http://redmine.encodedcc.org/issues/5050

    if value.get('status') == 'replaced':
        value['status'] = 'deleted'


@upgrade_step('analysis_step', '6', '7')
def analysis_step_6_7(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-4613

    input_file = value.get('input_file_types', None)
    output_file = value.get('output_file_types', None)
    if input_file and 'candidate regulatory elements' in input_file:
            input_file.remove('candidate regulatory elements')
            input_file.append('candidate Cis-Regulatory Elements')
            value['input_file_types'] = input_file

    if output_file and 'candidate regulatory elements' in output_file:
            output_file.remove('candidate regulatory elements')
            output_file.append('candidate Cis-Regulatory Elements')
            value['output_file_types'] = output_file


@upgrade_step('analysis_step', '7', '8')
def analysis_step_7_8(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-4641

    input_file_types = value.get('input_file_types', None)
    output_file_types = value.get('output_file_types', None)
    if input_file_types and 'optimal idr thresholded peaks' in input_file_types:
            input_file_types.remove('optimal idr thresholded peaks')
            input_file_types.append('optimal IDR thresholded peaks')
            value['input_file_types'] = input_file_types
    if input_file_types and 'conservative idr thresholded peaks' in input_file_types:
            input_file_types.remove('conservative idr thresholded peaks')
            input_file_types.append('conservative IDR thresholded peaks')
            value['input_file_types'] = input_file_types
    if input_file_types and 'pseudoreplicated idr thresholded peaks' in input_file_types:
            input_file_types.remove('pseudoreplicated idr thresholded peaks')
            input_file_types.append('pseudoreplicated IDR thresholded peaks')
            value['input_file_types'] = input_file_types

    if output_file_types and 'optimal idr thresholded peaks' in output_file_types:
            output_file_types.remove('optimal idr thresholded peaks')
            output_file_types.append('optimal IDR thresholded peaks')
            value['output_file_types'] = output_file_types
    if output_file_types and 'conservative idr thresholded peaks' in output_file_types:
            output_file_types.remove('conservative idr thresholded peaks')
            output_file_types.append('conservative IDR thresholded peaks')
            value['output_file_types'] = output_file_types
    if output_file_types and 'pseudoreplicated idr thresholded peaks' in output_file_types:
            output_file_types.remove('pseudoreplicated idr thresholded peaks')
            output_file_types.append('pseudoreplicated IDR thresholded peaks')
            value['output_file_types'] = output_file_types


@upgrade_step('analysis_step', '8', '9')
def analysis_step_8_9(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5232
    output_file_types = value.get('output_file_types', None)
    input_file_types = value.get('input_file_types', None)

    if output_file_types and 'representative dnase hypersensitivity sites' in output_file_types:
        output_file_types.remove('representative dnase hypersensitivity sites')
        output_file_types.append('representative DNase hypersensitivity sites (rDHSs)')
    if input_file_types and 'representative dnase hypersensitivity sites' in input_file_types:
        input_file_types.remove('representative dnase hypersensitivity sites')
        input_file_types.append('representative DNase hypersensitivity sites (rDHSs)')
    return


@upgrade_step('analysis_step', '9', '10')
def analysis_step_9_10(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5424
    output_file_types = value.get('output_file_types', None)
    input_file_types = value.get('input_file_types', None)

    if output_file_types and 'spike-in sequence' in output_file_types:
        output_file_types.remove('spike-in sequence')
        output_file_types.append('spike-ins')
    if input_file_types and 'spike-in sequence' in input_file_types:
        input_file_types.remove('spike-in sequence')
        input_file_types.append('spike-ins')
    return


@upgrade_step('analysis_step', '10', '11')
def analysis_step_10_11(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5480

    if 'stable peaks' in value.get('input_file_types', []):
        value['input_file_types'].remove('stable peaks')
        value['input_file_types'].append('pseudo-replicated peaks')
    if 'stable peaks' in value.get('output_file_types', []):
        value['output_file_types'].remove('stable peaks')
        value['output_file_types'].append('pseudo-replicated peaks')


@upgrade_step('analysis_step', '11', '12')
def analysis_step_11_12(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5551

    if 'smoothed methylation stage at CpG' in value.get('input_file_types', []):
        value['input_file_types'].remove('smoothed methylation stage at CpG')
        value['input_file_types'].append('smoothed methylation state at CpG')
    if 'smoothed methylation stage at CpG' in value.get('output_file_types', []):
        value['output_file_types'].remove('smoothed methylation stage at CpG')
        value['output_file_types'].append('smoothed methylation state at CpG')


@upgrade_step('analysis_step', '12', '13')
def analysis_step_12_13(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5573
    output_file_types = value.get('output_file_types', None)
    input_file_types = value.get('input_file_types', None)

    if output_file_types and 'consensus DNase hypersensitivity sites (cDHSs)' in output_file_types:
        output_file_types.remove('consensus DNase hypersensitivity sites (cDHSs)')
        output_file_types.append('consensus DNase hypersensitivity sites')
    if output_file_types and 'representative DNase hypersensitivity sites (rDHSs)' in output_file_types:
        output_file_types.remove('representative DNase hypersensitivity sites (rDHSs)')
        output_file_types.append('representative DNase hypersensitivity sites')
    if input_file_types and 'consensus DNase hypersensitivity sites (cDHSs)' in input_file_types:
        input_file_types.remove('consensus DNase hypersensitivity sites (cDHSs)')
        input_file_types.append('consensus DNase hypersensitivity sites')
    if input_file_types and 'representative DNase hypersensitivity sites (rDHSs)' in input_file_types:
        input_file_types.remove('representative DNase hypersensitivity sites (rDHSs)')
        input_file_types.append('representative DNase hypersensitivity sites')
    return


@upgrade_step('analysis_step', '13', '14')
def analysis_step_13_14(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5662
    if 'pseudo-replicated peaks' in value.get('input_file_types', []):
        value['input_file_types'].remove('pseudo-replicated peaks')
        value['input_file_types'].append('pseudoreplicated peaks')
    if 'pseudo-replicated peaks' in value.get('output_file_types', []):
        value['output_file_types'].remove('pseudo-replicated peaks')
        value['output_file_types'].append('pseudoreplicated peaks')


@upgrade_step('analysis_step', '14', '15')
def analysis_step_14_15(value, system):
    # https://encodedcc.atlassian.net/browse/ENCD-5657
    output_file_types = value.get('output_file_types', None)
    input_file_types = value.get('input_file_types', None)

    term_pairs = [
        ('blacklisted regions', 'exclusion list regions'), 
        ('mitochondria blacklisted regions', 'mitochondrial exclusion list regions'),
    ]
    
    for old_term, new_term in term_pairs:
        if output_file_types and old_term in output_file_types:
            output_file_types.remove(old_term)
            output_file_types.append(new_term)
        if input_file_types and old_term in input_file_types:
            input_file_types.remove(old_term)
            input_file_types.append(new_term)


@upgrade_step('analysis_step', '15', '16')
def analysis_step_15_16(value, system):
    # https://igvf.atlassian.net/browse/ENCM-97
    if 'topologically associated domain identification' in value.get('analysis_step_types', []):
        value['analysis_step_types'].remove('topologically associated domain identification')
        value['analysis_step_types'].append('contact domain identification')

    output_file_types = value.get('output_file_types', None)
    input_file_types = value.get('input_file_types', None)

    term_pairs = [
        ('topologically associated domains', 'contact domains'),
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

    for old_term, new_term in term_pairs:
        if output_file_types and old_term in output_file_types:
            output_file_types.remove(old_term)
            output_file_types.append(new_term)
        if input_file_types and old_term in input_file_types:
            input_file_types.remove(old_term)
            input_file_types.append(new_term)
