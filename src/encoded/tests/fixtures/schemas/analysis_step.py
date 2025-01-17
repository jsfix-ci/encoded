import pytest


@pytest.fixture
def base_analysis_step(testapp, software_version):
    item = {
        'name': 'lrna-pe-star-alignment-step-v-2-0',
        'title': 'Long RNA-seq STAR paired-ended alignment step v2.0',
        'analysis_step_types': ['alignments'],
        'input_file_types': ['reads'],
        'software_versions': [
            software_version['@id'],
        ]
    }
    return item


@pytest.fixture
def analysis_step(testapp):
    item = {
        'step_label': 'fastqc-step',
        'title': 'fastqc step',
        'major_version': 1,
        'input_file_types': ['reads'],
        'analysis_step_types': ['QA calculation'],

    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_1(base_analysis_step):

    item = base_analysis_step.copy()
    item.update({
        'schema_version': '2',
        'output_file_types': ['signal of multi-mapped reads']
    })
    return item


@pytest.fixture
def analysis_step_3(base_analysis_step):
    item = base_analysis_step.copy()
    item.update({
        'schema_version': '3',
        'analysis_step_types': ['alignment', 'alignment'],
        'input_file_types': ['reads', 'reads'],
        'output_file_types': ['transcriptome alignments', 'transcriptome alignments']
    })
    return item


@pytest.fixture
def analysis_step_5(base_analysis_step):
    item = base_analysis_step.copy()
    item.update({
        'schema_version': '5',
        'aliases': ["dnanexus:align-star-se-v-2"],
        'uuid': '8eda9dfa-b9f1-4d58-9e80-535a5e4aaab1',
        'status': 'in progress',
        'analysis_step_types': ['pooling', 'signal generation', 'file format conversion', 'quantification'],
        'input_file_types': ['alignments'],
        'output_file_types': ['methylation state at CHG', 'methylation state at CHH', 'raw signal', 'methylation state at CpG']
    })
    return item


@pytest.fixture
def analysis_step_6(base_analysis_step):
    item = base_analysis_step.copy()
    item.update({
        'schema_version': '6',
        'input_file_types': ['alignments', 'candidate regulatory elements'],
        'output_file_types': ['raw signal', 'candidate regulatory elements']
    })
    return item


@pytest.fixture
def analysis_step_7(base_analysis_step):
    item = base_analysis_step.copy()
    item.update({
        'input_file_types': [
            'peaks',
            'optimal idr thresholded peaks',
            'conservative idr thresholded peaks',
            'pseudoreplicated idr thresholded peaks'
        ],
        'output_file_types': [
            'peaks',
            'optimal idr thresholded peaks',
            'conservative idr thresholded peaks',
            'pseudoreplicated idr thresholded peaks'
        ],
    })
    return item


@pytest.fixture
def analysis_step_bam(testapp):
    item = {
        'step_label': 'bamqc-step',
        'title': 'bamqc step',
        'input_file_types': ['reads'],
        'analysis_step_types': ['QA calculation'],
        'major_version': 2
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_8(testapp):
    item = {
        'schema_version': '8',
        'step_label': 'rdhs-step',
        'title': 'rdhs step',
        'major_version': 1,
        'analysis_step_types': ['QA calculation'],
        'input_file_types': ['representative dnase hypersensitivity sites'],
        'output_file_types': ['representative dnase hypersensitivity sites']
    }
    return item


@pytest.fixture
def analysis_step_10(testapp):
    item = {
        'schema_version': '10',
        'step_label': 'rdhs-step',
        'title': 'rdhs step',
        'major_version': 1,
        'analysis_step_types': ['QA calculation'],
        'input_file_types': ['stable peaks'],
        'output_file_types': ['stable peaks']
    }
    return item


@pytest.fixture
def analysis_step_chip_encode4(testapp):
    item = {
        'step_label': 'chip-seq-star-align-step',
        'title': 'ChIP seq alignment step',
        'input_file_types': ['reads'],
        'analysis_step_types': ['QA calculation', 'alignment'],
        'major_version': 1
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_dnase_encode4(testapp):
    item = {
        'step_label': 'dnase-seq-star-align-step',
        'title': 'DNase seq alignment step',
        'input_file_types': ['reads'],
        'analysis_step_types': ['QA calculation', 'alignment'],
        'major_version': 1
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_rna_encode4(testapp):
    item = {
        'step_label': 'rna-pipeline-step',
        'title': 'RNA seq pipeline step',
        'input_file_types': ['reads'],
        'analysis_step_types': ['QA calculation', 'alignment'],
        'major_version': 1
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_atac_encode4_alignment(testapp):
    item = {
        'step_label': 'atac-seq-alignment-step',
        'title': 'ATAC seq alignment step',
        'input_file_types': ['reads'],
        'output_file_types': ['alignments', 'unfiltered alignments'],
        'analysis_step_types': ['read trimming', 'alignment', 'filtering', 'file format conversion'],
        'major_version': 1
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_atac_encode4_pseudoreplicate_concordance(testapp):
    item = {
        'step_label': 'atac-seq-unreplicated-overlap-step',
        'title': 'ATAC seq unreplicated overlap step',
        'input_file_types': ['alignments'],
        'output_file_types': ['pseudoreplicated peaks'],
        'analysis_step_types': ['peak calling', 'partition concordance'],
        'major_version': 1
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_atac_encode4_partition_concordance(testapp):
    item = {
        'step_label': 'atac-seq-partition-concordance-step',
        'title': 'ATAC seq partition concordance step',
        'input_file_types': ['alignments'],
        'output_file_types': ['pseudoreplicated peaks'],
        'analysis_step_types': ['peak calling', 'partition concordance'],
        'major_version': 1
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_9(testapp):
    item = {
        'schema_version': '9',
        'step_label': 'splice-junction-extraction-step',
        'title': 'spike-in step',
        'major_version': 1,
        'analysis_step_types': ['splice junction extraction'],
        'input_file_types': ['spike-in sequence'],
        'output_file_types': ['spike-in sequence']
    }
    return item


@pytest.fixture
def analysis_step_11(testapp):
    item = {
        'schema_version': '11',
        'step_label': 'wgbs-methylation-step',
        'title': 'wgbs methylation step',
        'major_version': 1,
        'analysis_step_types': ['methylation estimation'],
        'input_file_types': ['smoothed methylation stage at CpG'],
        'output_file_types': ['smoothed methylation stage at CpG']
    }
    return item


@pytest.fixture
def analysis_step_12(testapp):
    item = {
        'schema_version': '12',
        'step_label': 'rdhs-step',
        'title': 'rdhs step',
        'major_version': 1,
        'analysis_step_types': ['QA calculation'],
        'input_file_types': ['consensus DNase hypersensitivity sites (cDHSs)'],
        'output_file_types': ['representative DNase hypersensitivity sites (rDHSs)']
    }
    return item


@pytest.fixture
def analysis_step_13(testapp):
    item = {
        'schema_version': '13',
        'step_label': 'pseudoreplicated-step',
        'title': 'pseudoreplicated step',
        'major_version': 1,
        'analysis_step_types': ['peak calling'],
        'input_file_types': ['pseudo-replicated peaks'],
        'output_file_types': ['pseudo-replicated peaks']
    }
    return item


@pytest.fixture
def analysis_step_14(testapp):
    item = {
        'schema_version': '14',
        'step_label': 'atac-seq-step',
        'title': 'atac-seq step',
        'major_version': 1,
        'analysis_step_types': ['QA calculation'],
        'input_file_types': ['alignments', 'blacklisted regions'],
        'output_file_types': ['mitochondria blacklisted regions', 'pseudo-replicated peaks']
    }
    return item


@pytest.fixture
def analysis_step_chia_alignment(testapp):
    item = {
        'step_label': 'chia-pet-alignment-step',
        'title': 'ChIA-pet alignment step',
        'input_file_types': ['reads'],
        'output_file_types': ['alignments', 'unfiltered alignments'],
        'analysis_step_types': ['alignment', 'filtering', 'classification'],
        'major_version': 1
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_chia_peak_calling(testapp):
    item = {
        'step_label': 'chia-pet-peak-calling-step',
        'title': 'ChIA-pet peak calling step',
        'input_file_types': ['unfiltered alignments'],
        'output_file_types': ['peaks'],
        'analysis_step_types': ['peak calling'],
        'major_version': 1
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_chia_interaction_calling(testapp):
    item = {
        'step_label': 'chia-pet-interaction-calling-step',
        'title': 'ChIA-PET interaction calling step',
        'input_file_types': ['alignments'],
        'output_file_types': ['contact matrix'],
        'analysis_step_types': ['interaction calling', 'file format conversion'],
        'major_version': 1
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_hic_chromatin_interactions(testapp):
    item = {
        'step_label': 'hic-chromatin-interactions-step',
        'title': 'Hi-C contact matrix step',
        'input_file_types': ['alignments'],
        'output_file_types': ['contact matrix'],
        'analysis_step_types': ['interaction calling', 'file format conversion'],
        'major_version': 1
    }
    return testapp.post_json('/analysis_step', item).json['@graph'][0]


@pytest.fixture
def analysis_step_15(testapp):
    item = {
        'schema_version': '15',
        'step_label': 'test-hic-updated-file-step',
        'title': 'Test hic updated file step',
        'input_file_types': [
            'topologically associated domains',
            'chromatin interactions',
            'DNA accessibility raw signal',
            'long range chromatin interactions'
        ],
        'output_file_types': [
            'nested topologically associated domains',
            'allele-specific chromatin interactions',
            'variants chromatin interactions',
            'haplotype-specific chromatin interactions',
            'haplotype-specific DNA accessibility raw signal',
            'haplotype-specific DNA accessibility corrected signal'
        ],
        'analysis_step_types': ['topologically associated domain identification'],
        'major_version': 1
    }
    return item
