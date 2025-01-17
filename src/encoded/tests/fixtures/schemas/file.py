import pytest


@pytest.fixture
def file_fastq_2(testapp, lab, award, base_experiment, base_replicate, platform1):
    item = {
        'dataset': base_experiment['@id'],
        'replicate': base_replicate['@id'],
        'file_format': 'fastq',
        'md5sum': '94be74b6e14515393547f4ebfa66d77a',
        'run_type': "paired-ended",
        'platform': platform1['@id'],
        'paired_end': '1',
        'output_type': 'reads',
        "read_length": 50,
        'file_size': 34,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_fastq_3(testapp, lab, award, base_experiment, replicate_1_1, platform1):
    item = {
        'dataset': base_experiment['@id'],
        'replicate': replicate_1_1['@id'],
        'file_format': 'fastq',
        'file_size': 34,
        'platform': platform1['@id'],
        'output_type': 'reads',
        "read_length": 50,
        'md5sum': '21be74b6e11515393507f4ebfa66d77a',
        'run_type': "paired-ended",
        'paired_end': '1',
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_fastq_4(testapp, lab, award, base_experiment, replicate_2_1, platform1):
    item = {
        'dataset': base_experiment['@id'],
        'replicate': replicate_2_1['@id'],
        'platform': platform1['@id'],
        'file_format': 'fastq',
        'file_size': 34,
        'md5sum': '11be74b6e11515393507f4ebfa66d77a',
        'run_type': "paired-ended",
        'paired_end': '1',
        'output_type': 'reads',
        "read_length": 50,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_fastq_5(testapp, lab, award, base_experiment, replicate_2_1, platform1):
    item = {
        'dataset': base_experiment['@id'],
        'platform': platform1['@id'],
        'replicate': replicate_2_1['@id'],
        'file_format': 'fastq',
        'md5sum': '91be79b6e11515993509f4ebfa66d77a',
        'run_type': "paired-ended",
        'paired_end': '1',
        "read_length": 50,
        'output_type': 'reads',
        'file_size': 34,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_fastq_6(testapp, lab, award, base_experiment, replicate_1_1, platform1):
    item = {
        'dataset': base_experiment['@id'],
        'replicate': replicate_1_1['@id'],
        'file_format': 'fastq',
        'file_size': 34,
        'platform': platform1['@id'],
        'output_type': 'reads',
        "read_length": 50,
        'md5sum': '21be74b6e11515393507f4ebfa66d77a',
        'run_type': "single-ended",
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_fastq_no_read_length(testapp, lab, award, experiment, replicate_1_1, platform3):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_1_1['@id'],
        'file_format': 'fastq',
        'file_size': 68,
        'platform': platform3['@id'],
        'output_type': 'reads',
        'md5sum': '21be74b6e11515393507f4ebfa66d77a',
        'lab': lab['@id'],
        'award': award['@id'],
        'aliases': ['encode:no read length alias'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]

@pytest.fixture
def file_bam_1_1(testapp, encode_lab, award, base_experiment, file_fastq_3):
    item = {
        'dataset': base_experiment['@id'],
        'derived_from': [file_fastq_3['@id']],
        'file_format': 'bam',
        'assembly': 'mm10',
        'file_size': 34,
        'md5sum': '91be44b6e11515394407f4ebfa66d77a',
        'output_type': 'alignments',
        'lab': encode_lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_bam_2_1(testapp, encode_lab, award, base_experiment, file_fastq_4):
    item = {
        'dataset': base_experiment['@id'],
        'derived_from': [file_fastq_4['@id']],
        'file_format': 'bam',
        'assembly': 'mm10',
        'file_size': 34,
        'md5sum': '91be71b6e11515377807f4ebfa66d77a',
        'output_type': 'alignments',
        'lab': encode_lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_fastq_control_chip(testapp, lab, award, experiment_chip_control, replicate_control_chip, platform1):
    item = {
        'dataset': experiment_chip_control['@id'],
        'replicate': replicate_control_chip['@id'],
        'file_format': 'fastq',
        'file_size': 34,
        'platform': platform1['@id'],
        'output_type': 'reads',
        "read_length": 50,
        'md5sum': '21ab74b6e21518393507f4ebfa66d77a',
        'run_type': "single-ended",
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_fastq_1_chip(testapp, lab, award, experiment_chip_H3K27me3, replicate_1_chip, platform1, file_fastq_control_chip):
    item = {
        'dataset': experiment_chip_H3K27me3['@id'],
        'replicate': replicate_1_chip['@id'],
        'file_format': 'fastq',
        'file_size': 34,
        'platform': platform1['@id'],
        'output_type': 'reads',
        "read_length": 50,
        'md5sum': '21be74b6e19115393507f4ebfa66d77a',
        'run_type': "single-ended",
        'lab': lab['@id'],
        'award': award['@id'],
        'controlled_by': [file_fastq_control_chip['@id']],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_fastq_2_chip(testapp, lab, award, experiment_chip_H3K27me3, replicate_2_chip, platform1):
    item = {
        'dataset': experiment_chip_H3K27me3['@id'],
        'replicate': replicate_2_chip['@id'],
        'file_format': 'fastq',
        'file_size': 34,
        'platform': platform1['@id'],
        'output_type': 'reads',
        "read_length": 50,
        'md5sum': '21ab74b6e11515393507f4ebfa66d77a',
        'run_type': "single-ended",
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]



@pytest.fixture
def file_bam_control_chip(testapp, encode_lab, award, experiment_chip_control, file_fastq_control_chip):
    item = {
        'dataset': experiment_chip_control['@id'],
        'derived_from': [file_fastq_control_chip['@id']],
        'file_format': 'bam',
        'assembly': 'GRCh38',
        'file_size': 34,
        'md5sum': '91be42b6e91515394407f4ebfa66d77a',
        'output_type': 'alignments',
        'lab': encode_lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_bam_1_chip(testapp, encode_lab, award, experiment_chip_H3K27me3, file_fastq_1_chip):
    item = {
        'dataset': experiment_chip_H3K27me3['@id'],
        'derived_from': [file_fastq_1_chip['@id']],
        'file_format': 'bam',
        'assembly': 'GRCh38',
        'file_size': 34,
        'md5sum': '91be42b6e11515394407f4ebfa66d77a',
        'output_type': 'alignments',
        'lab': encode_lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_bam_2_chip(testapp, encode_lab, award, experiment_chip_H3K27me3, file_fastq_2_chip):
    item = {
        'dataset': experiment_chip_H3K27me3['@id'],
        'derived_from': [file_fastq_2_chip['@id']],
        'file_format': 'bam',
        'assembly': 'GRCh38',
        'file_size': 34,
        'md5sum': '91be89b6e11515377807f4ebfa66d77a',
        'output_type': 'alignments',
        'lab': encode_lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_bed_narrowPeak_chip_background(testapp, experiment_chip_H3K27me3, file_bam_1_chip, award, lab):
    item = {
        'dataset': experiment_chip_H3K27me3['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'derived_from': [file_bam_1_chip['@id']],
        'file_format': 'bed',
        'file_format_type': 'narrowPeak',
        'file_size': 345,
        'assembly': 'GRCh38',
        'md5sum': 'e008ab102df36d93dd070ef0712b8ee7',
        'output_type': 'peaks and background as input for IDR',
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file_bed_narrowPeak_chip_peaks(testapp, experiment_chip_H3K27me3, file_bed_narrowPeak_chip_background, award, lab):
    item = {
        'dataset': experiment_chip_H3K27me3['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'file_format': 'bed',
        'derived_from':[file_bed_narrowPeak_chip_background['@id']],
        'file_format_type': 'narrowPeak',
        'file_size': 345,
        'assembly': 'GRCh38',
        'md5sum': 'e008ab204df36d93dd070ef0712b8ee7',
        'output_type': 'optimal IDR thresholded peaks',
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file_bed_narrowPeak_chip_peaks2(testapp, experiment_chip_H3K27me3, file_bed_narrowPeak_chip_background2, award, lab):
    item = {
        'dataset': experiment_chip_H3K27me3['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'file_format': 'bed',
        'derived_from':[file_bed_narrowPeak_chip_background2['@id']],
        'file_format_type': 'narrowPeak',
        'file_size': 345,
        'assembly': 'GRCh38',
        'md5sum': 'e008ab267ff36d93dd070ef0712b8ee7',
        'output_type': 'optimal IDR thresholded peaks',
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file_bed_narrowPeak_chip_background2(testapp, experiment_chip_H3K27me3, file_bam_1_chip, award, lab):
    item = {
        'dataset': experiment_chip_H3K27me3['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'derived_from': [file_bam_1_chip['@id']],
        'file_format': 'bed',
        'file_format_type': 'narrowPeak',
        'file_size': 345,
        'assembly': 'GRCh38',
        'md5sum': 'e008ab106ab36d93dd070ef0712b8ee7',
        'output_type': 'peaks and background as input for IDR',
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file_bed_methyl(base_experiment, award, encode_lab, testapp, analysis_step_run_bam):
    item = {
        'dataset': base_experiment['uuid'],
        "file_format": "bed",
        "file_format_type": "bedMethyl",
        "file_size": 66569,
        "assembly": "mm10",
        "md5sum": "91be74b6e11515223507f4ebf266d77a",
        "output_type": "methylation state at CpG",
        "award": award["uuid"],
        "lab": encode_lab["uuid"],
        "status": "released",
        "step_run": analysis_step_run_bam['uuid']
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file_tsv_1_2(base_experiment, award, encode_lab, testapp, analysis_step_run_bam):
    item = {
        'dataset': base_experiment['uuid'],
        'file_format': 'tsv',
        'file_size': 3654,
        'assembly': 'mm10',
        'genome_annotation': 'M4',
        'md5sum': '912e7ab6e11515393507f42bfa66d77a',
        'output_type': 'gene quantifications',
        'award': award['uuid'],
        'lab': encode_lab['uuid'],
        'status': 'released',
        'step_run': analysis_step_run_bam['uuid']
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file_tsv_1_1(base_experiment, award, encode_lab, testapp, analysis_step_run_bam):
    item = {
        'dataset': base_experiment['uuid'],
        'file_format': 'tsv',
        'file_size': 36524,
        'assembly': 'mm10',
        'genome_annotation': 'M4',
        'md5sum': '91be74b6e315153935a7f4ecfa66d77a',
        'output_type': 'gene quantifications',
        'award': award['uuid'],
        'lab': encode_lab['uuid'],
        'status': 'released',
        'step_run': analysis_step_run_bam['uuid']
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file1_2(file_exp, award, lab, file_rep1_2, platform1, testapp):
    item = {
        'dataset': file_exp['uuid'],
        'replicate': file_rep1_2['uuid'],
        'file_format': 'fastq',
        'platform': platform1['@id'],
        'md5sum': '91be74b6e11515393507f4ebfa66d58a',
        'output_type': 'raw data',
        'file_size': 34,
        'run_type': 'single-ended',
        'award': award['uuid'],
        'lab': lab['uuid'],
        'status': 'released'
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file2(file_exp2, award, lab, file_rep2, platform1, testapp):
    item = {
        'dataset': file_exp2['uuid'],
        'replicate': file_rep2['uuid'],
        'file_format': 'fastq',
        'md5sum': '91be74b6e11515393507f4ebfa66d58b',
        'output_type': 'raw data',
        'file_size': 34,
        'run_type': 'single-ended',
        'platform': platform1['uuid'],
        'award': award['uuid'],
        'lab': lab['uuid'],
        'status': 'released'
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file1(file_exp, award, lab, file_rep, file2, platform1, testapp):
    item = {
        'dataset': file_exp['uuid'],
        'replicate': file_rep['uuid'],
        'file_format': 'fastq',
        'md5sum': '91be74b6e11515393507f4ebfa66d58c',
        'output_type': 'reads',
        "read_length": 50,
        'file_size': 34,
        'run_type': 'single-ended',
        'platform': platform1['uuid'],
        'award': award['uuid'],
        'lab': lab['uuid'],
        'status': 'released',
        'controlled_by': [file2['uuid']]
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file3(file_exp, award, lab, file_rep, platform1, testapp):
    item = {
        'dataset': file_exp['uuid'],
        'replicate': file_rep['uuid'],
        'file_format': 'fastq',
        'file_size': 34,
        'md5sum': '91be74b6e11515393507f4ebfa56d78d',
        'output_type': 'reads',
        "read_length": 50,
        'platform': platform1['uuid'],
        'run_type': 'single-ended',
        'award': award['uuid'],
        'lab': lab['uuid'],
        'status': 'released'
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file4(file_exp2, award, lab, file_rep2, platform1, testapp):
    item = {
        'dataset': file_exp2['uuid'],
        'replicate': file_rep2['uuid'],
        'file_format': 'fastq',
        'md5sum': '91ae74b6e11515393507f4ebfa66d78a',
        'output_type': 'reads',
        'platform': platform1['uuid'],
        "read_length": 50,
        'file_size': 34,
        'run_type': 'single-ended',
        'award': award['uuid'],
        'lab': lab['uuid'],
        'status': 'released'
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file6(file_exp2, award, encode_lab, testapp, analysis_step_run_bam):
    item = {
        'dataset': file_exp2['uuid'],
        'file_format': 'bam',
        'file_size': 3,
        'md5sum': '91ce74b6e11515393507f4ebfa66d78a',
        'output_type': 'alignments',
        'award': award['uuid'],
        'file_size': 34,
        'assembly': 'hg19',
        'lab': encode_lab['uuid'],
        'status': 'released',
        'step_run': analysis_step_run_bam['uuid']
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file7(file_exp2, award, encode_lab, testapp, analysis_step_run_bam):
    item = {
        'dataset': file_exp2['uuid'],
        'file_format': 'tsv',
        'file_size': 3,
        'md5sum': '91be74b6e11515394507f4ebfa66d78a',
        'output_type': 'gene quantifications',
        'award': award['uuid'],
        'lab': encode_lab['uuid'],
        'status': 'released',
        'step_run': analysis_step_run_bam['uuid']
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file_fastq(testapp, lab, award, base_experiment, base_replicate, platform1):
    item = {
        'dataset': base_experiment['@id'],
        'replicate': base_replicate['@id'],
        'file_format': 'fastq',
        'md5sum': '91b574b6411514393507f4ebfa66d47a',
        'output_type': 'reads',
        'platform': platform1['@id'],
        "read_length": 50,
        'run_type': "single-ended",
        'file_size': 34,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_no_replicate(testapp, experiment, award, lab):
    item = {
        'dataset': experiment['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'file_format': 'bam',
        'file_size': 345,
        'assembly': 'hg19',
        'md5sum': 'e002cd204df36d93dd070ef0712b8eed',
        'output_type': 'alignments',
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_with_replicate(testapp, experiment, award, lab, replicate_url):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'file_format': 'bam',
        'file_size': 345,
        'assembly': 'hg19',
        'md5sum': 'e003cd204df36d93dd070ef0712b8eed',
        'output_type': 'alignments',
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_with_derived(testapp, experiment, award, lab, file_with_replicate):
    item = {
        'dataset': experiment['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'file_format': 'bam',
        'assembly': 'hg19',
        'file_size': 345,
        'md5sum': 'e004cd204df36d93dd070ef0712b8eed',
        'output_type': 'alignments',
        'status': 'in progress',  # avoid s3 upload codepath
        'derived_from': [file_with_replicate['@id']]
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_no_assembly(testapp, experiment, award, lab, replicate_url):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'file_format': 'bam',
        'file_size': 345,
        'md5sum': '82847a2a5beb8095282c68c00f48e347',
        'output_type': 'alignments',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def file_no_error(testapp, experiment, award, lab, replicate_url, platform1):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'platform': platform1['@id'],
        'award': award['@id'],
        'file_format': 'fastq',
        'run_type': 'paired-ended',
        'paired_end': '1',
        'output_type': 'reads',
        "read_length": 50,
        'md5sum': '136e501c4bacf4aab87debab20d76648',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def file_content_error(testapp, experiment, award, lab, replicate_url, platform1):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'platform': platform1['@id'],
        'award': award['@id'],
        'file_format': 'fastq',
        'run_type': 'single-ended',
        'output_type': 'reads',
        "read_length": 36,
        'md5sum': '99378c852c5be68251cbb125ffcf045a',
        'status': 'content error'
    }
    return item


@pytest.fixture
def file_no_platform(testapp, experiment, award, lab, replicate_url):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'award': award['@id'],
        'file_format': 'fastq',
        'run_type': 'single-ended',
        'output_type': 'reads',
        "read_length": 36,
        'md5sum': '99378c852c5be68251cbb125ffcf045a',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def file_no_paired_end(testapp, experiment, award, lab, replicate_url, platform1):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'award': award['@id'],
        'platform': platform1['@id'],
        'file_format': 'fastq',
        'run_type': 'paired-ended',
        'output_type': 'reads',
        "read_length": 50,
        'md5sum': '136e501c4bacf4aab87debab20d76648',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def file_with_bad_date_created(testapp, experiment, award, lab, replicate_url, platform1):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'date_created': '2017-10-23',
        'platform': platform1['@id'],
        'award': award['@id'],
        'file_format': 'fastq',
        'run_type': 'paired-ended',
        'paired_end': '1',
        'output_type': 'reads',
        "read_length": 50,
        'md5sum': '136e501c4bacf4aab87debab20d76648',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def file_with_bad_revoke_detail(testapp, experiment, award, lab, replicate_url, platform1):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'platform': platform1['@id'],
        'award': award['@id'],
        'file_format': 'fastq',
        'run_type': 'paired-ended',
        'paired_end': '1',
        'output_type': 'reads',
        "read_length": 50,
        'md5sum': '136e501c4bacf4aab87debab20d76648',
        'status': 'in progress',
        'revoke_detail': 'some reason to be revoked'
    }
    return item


@pytest.fixture
def file_processed_output_raw_format(testapp, experiment, award, lab, replicate_url, platform1):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'platform': platform1['@id'],
        'award': award['@id'],
        'file_format': 'fastq',
        'run_type': 'single-ended',
        'output_type': 'peaks',
        'read_length': 36,
        'md5sum': '99378c852c5be68251cbb125ffcf045a',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def file_raw_output_processed_format(testapp, experiment, award, lab, replicate_url):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'award': award['@id'],
        'file_format': 'bam',
        'output_type': 'reads',
        'read_length': 36,
        'assembly': 'hg19',
        'md5sum': '99378c852c5be68251cbb125ffcf045a',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def file_restriction_map(testapp, experiment, award, lab):
    item = {
        'dataset': experiment['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'file_format': 'txt',
        'file_size': 3456,
        'assembly': 'hg19',
        'md5sum': 'e002cd204df36d93dd070ef0712b8e12',
        'output_type': 'restriction enzyme site locations',
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return item


@pytest.fixture
def file_no_genome_annotation(testapp, experiment, award, lab, replicate_url):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'assembly': 'GRCh38',
        'file_format': 'database',
        'file_size': 342,
        'md5sum': '82847a2a5beb8095282c68c00f48e347',
        'output_type': 'transcriptome index',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def file_database_output_type(testapp, experiment, award, lab, replicate_url):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'assembly': 'GRCh38',
        'file_format': 'database',
        'file_size': 342,
        'genome_annotation': 'V24',
        'md5sum': '82847a2a5beb8095282c68c00f48e348',
        'output_type': 'alignments',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def file_good_bam(testapp, experiment, award, lab, replicate_url, platform1):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'platform': platform1['@id'],
        'award': award['@id'],
        'assembly': 'GRCh38',
        'file_format': 'bam',
        'output_type': 'alignments',
        'md5sum': '136e501c4bacf4fab87debab20d76648',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def file_no_runtype_readlength(testapp, experiment, award, lab, replicate_url, platform1):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'platform': platform1['@id'],
        'award': award['@id'],
        'file_format': 'fastq',
        'output_type': 'reads',
        'md5sum': '99378c852c5be68251cbb125ffcf045a',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def uploading_file(testapp, award, experiment, lab, replicate_url, dummy_request):
    item = {
        'award': award['@id'],
        'dataset': experiment['@id'],
        'lab': lab['@id'],
        'replicate': replicate_url['@id'],
        'file_format': 'tsv',
        'file_size': 2534535,
        'md5sum': '00000000000000000000000000000000',
        'output_type': 'raw data',
        'status': 'uploading',
    }
    return item


@pytest.fixture
def uploading_file_0(testapp, award, experiment, lab, replicate, dummy_request):
    item = {
        'award': award['@id'],
        'dataset': experiment['@id'],
        'lab': lab['@id'],
        'file_format': 'tsv',
        'file_size': 2534535,
        'md5sum': '00000000000000000000000000000000',
        'output_type': 'raw data',
        'status': 'uploading',
    }
    return item


@pytest.fixture
def hg19_file(testapp, base_reference_epigenome, award, lab):
    item = {
        'dataset': base_reference_epigenome['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'file_format': 'bigBed',
        'file_format_type': 'narrowPeak',
        'file_size': 345,
        'assembly': 'hg19',
        'md5sum': 'e002cd204df36d93dd070ef0712b8eed',
        'output_type': 'replicated peaks',
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def GRCh38_file(testapp, base_experiment_submitted, award, lab):
    item = {
        'dataset': base_experiment_submitted['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'file_format': 'bigBed',
        'file_format_type': 'narrowPeak',
        'file_size': 345,
        'assembly': 'GRCh38',
        'md5sum': 'e002cd204df36d93dd070ef0712b8ee7',
        'output_type': 'replicated peaks',
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def bigbed(testapp, lab, award, experiment, analysis_step_run):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'bigBed',
        'file_format_type': 'bedMethyl',
        'md5sum': 'd41d8cd98f00b204e9800998ecf8427e',
        'output_type': 'methylation state at CpG',
        'assembly': 'hg19',
        'file_size': 13224,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'step_run': analysis_step_run['@id'],
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_base(experiment):
    return {
        'accession': 'ENCFF000TST',
        'dataset': experiment['uuid'],
        'file_format': 'fasta',
        'file_size': 243434,
        'md5sum': 'd41d8cd98f00b204e9800998ecf8427e',
        'output_type': 'raw data',
    }


@pytest.fixture
def file_1(file_base):
    item = file_base.copy()
    item.update({
        'schema_version': '1',
        'status': 'CURRENT',
        'award': '1a4d6443-8e29-4b4a-99dd-f93e72d42418'
    })
    return item


@pytest.fixture
def file_17(file_base):
    item = file_base.copy()
    item.update({
        'assembly': 'hg19',
        'output_type': 'subreads',
        'schema_version': '17'
    })
    return item


@pytest.fixture
def file_2(file_base):
    item = file_base.copy()
    item.update({
        'schema_version': '2',
        'status': 'current',
        'download_path': 'bob.bigBed'
    })
    return item


@pytest.fixture
def file_3(file_base):
    item = file_base.copy()
    item.update({
        'schema_version': '3',
        'status': 'current',
        'download_path': 'bob.bigBed'
    })
    return item


@pytest.fixture
def file_4(file_base):
    item = file_base.copy()
    item.update({
        'schema_version': '4',
        'file_format': 'bed_bedMethyl',
        'download_path': 'bob.bigBed',
        'output_type': 'Base_Overlap_Signal'
    })
    return item


@pytest.fixture
def file_5(file_base):
    item = file_base.copy()
    item.update({
        'schema_version': '5',
        'file_format': 'bigWig',
        'output_type': 'signal of multi-mapped reads'
    })
    return item


@pytest.fixture
def file_7(file_base):
    item = file_base.copy()
    item.update({
        'schema_version': '7'
    })
    return item


@pytest.fixture
def file_8a(file_base):
    item = file_base.copy()
    item.update({
        'file_format': 'fastq',
        'assembly': 'hg19',
        'schema_version': '8'
    })
    return item


@pytest.fixture
def file_9(file_base):
    item = file_base.copy()
    item.update({
        'date_created': '2017-04-28'
    })
    return item


@pytest.fixture
def file_10(file_base):
    item = file_base.copy()
    item.update({
        'schema_version': '10'
    })
    return item


@pytest.fixture
def file_12(file_base):
    item = file_base.copy()
    item.update({
        'platform': 'ced61406-dcc6-43c4-bddd-4c977cc676e8',
        'schema_version': '12',
        'file_format': 'fastq',
        'run_type': 'single-ended',
        'read_length': 55,
        'file_size': 243434,
        'md5sum': 'd41d8cd98f00b204e9800998ecf8423e',
        'output_type': 'reads'
    })
    return item


@pytest.fixture
def old_file(experiment):
    return {
        'accession': 'ENCFF000OLD',
        'dataset': experiment['uuid'],
        'file_format': 'fasta',
        'md5sum': 'e41d9ce97b00b204e9811998ecf8427b',
        'output_type': 'raw data',
        'uuid': '627ef1f4-3426-44f4-afc3-d723eccd20bf'
    }


@pytest.fixture
def file_8b(file_base, old_file):
    item = file_base.copy()
    item.update({
        'schema_version': '8',
        'supercedes': list(old_file['uuid'])
    })
    return item


@pytest.fixture
def file_13(file_base):
    item = file_base.copy()
    item.update({
        'output_type': 'candidate regulatory elements'
    })
    return item


@pytest.fixture
def file_14_optimal(file_base):
    item = file_base.copy()
    item.update({
        'output_type': 'optimal idr thresholded peaks'
    })
    return item


@pytest.fixture
def file_14_conservative(file_base):
    item = file_base.copy()
    item.update({
        'output_type': 'conservative idr thresholded peaks'
    })
    return item


@pytest.fixture
def file_14_pseudoreplicated(file_base):
    item = file_base.copy()
    item.update({
        'output_type': 'pseudoreplicated idr thresholded peaks'
    })
    return item


@pytest.fixture
def file_15(file_base):
    item = file_base.copy()
    item.update({
        'platform': 'e2be5728-5744-4da4-8881-cb9526d0389e',
        'schema_version': '15',
        'file_format': 'fastq',
        'run_type': 'single-ended',
        'read_length': 55,
        'file_size': 243434,
        'md5sum': 'd41d8cd98f00b204e9800998ecf8423e',
        'output_type': 'reads'
    })
    return item


@pytest.fixture
def file_16(file_base):
    item = file_base.copy()
    item.update({
        'platform': '6c275b37-018d-4bf8-85f6-6e3b830524a9',
        'schema_version': '16'
    })
    return item


@pytest.fixture
def file(testapp, lab, award, experiment):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'fasta',
        'md5sum': 'd41d8cd98f00b204e9800998ecf8427e',
        'output_type': 'raw data',
        'lab': lab['@id'],
        'file_size': 34,
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def fastq_file(testapp, lab, award, experiment, replicate, platform1):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'fastq',
        'md5sum': '91be74b6e11515393507f4ebfa66d78b',
        'replicate': replicate['@id'],
        'output_type': 'reads',
        "read_length": 36,
        'file_size': 34,
        'platform': platform1['@id'],
        'run_type': 'single-ended',
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def bam_file(testapp, lab, award, experiment):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'bam',
        'file_size': 34,
        'md5sum': '91be74b6e11515393507f4ebfa66d78c',
        'output_type': 'alignments',
        'assembly': 'hg19',
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def bigWig_file(testapp, lab, award, experiment):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'bigWig',
        'md5sum': '91be74b6e11515393507f4ebfa66d78d',
        'output_type': 'signal of unique reads',
        'assembly': 'mm10',
        'file_size': 34,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_ucsc_browser_composite(testapp, lab, award, ucsc_browser_composite):
    item = {
        'dataset': ucsc_browser_composite['@id'],
        'file_format': 'fasta',
        'md5sum': '91be74b6e11515393507f4ebfa66d77a',
        'output_type': 'raw data',
        'file_size': 34,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_bam(testapp, lab, award, base_experiment, base_replicate):
    item = {
        'dataset': base_experiment['@id'],
        'replicate': base_replicate['@id'],
        'file_format': 'bam',
        'md5sum': 'd41d8cd98f00b204e9800998ecf8427e',
        'output_type': 'alignments',
        'assembly': 'mm10',
        'lab': lab['@id'],
        'file_size': 34,
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_with_external_sheet(file, root):
    file_item = root.get_by_uuid(file['uuid'])
    properties = file_item.upgrade_properties()
    file_item.update(
        properties,
        sheets={
            'external': {
                'service': 's3',
                'key': 'xyz.bed',
                'bucket': 'test_file_bucket',
            }
        }
    )
    return file

@pytest.fixture
def public_file_with_public_external_sheet(file, root):
    file_item = root.get_by_uuid(file['uuid'])
    properties = file_item.upgrade_properties()
    properties['status'] = 'released'
    file_item.update(
        properties,
        sheets={
            'external': {
                'service': 's3',
                'key': 'xyz.bed',
                'bucket': 'pds_public_bucket_test',
            }
        }
    )
    return file

@pytest.fixture
def file_with_no_external_sheet(file, root):
    file_item = root.get_by_uuid(file['uuid'])
    properties = file_item.upgrade_properties()
    file_item.update(
        properties,
        sheets={
            'external': {}
        }
    )
    return file


@pytest.fixture
def file_subreads(testapp, experiment, award, lab, replicate_url, platform3):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 5768,
        'platform': platform3['@id'],
        'award': award['@id'],
        'file_format': 'bam',
        'md5sum': '0adb8693a743723d8a7882b5e9261b98',
        'output_type': 'subreads',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def fastq(fastq_no_replicate, replicate_url):
    item = fastq_no_replicate.copy()
    item['replicate'] = replicate_url['@id']
    return item

@pytest.fixture
def filtered_fastq(fastq_no_replicate, replicate_url):
    item = fastq_no_replicate.copy()
    item['output_type'] = 'filtered reads'
    return item

@pytest.fixture
def fastq_pair_1(fastq):
    item = fastq.copy()
    item['paired_end'] = '1'
    return item

@pytest.fixture
def mapped_run_type_on_fastq(award, experiment, lab, platform1):
    return {
        'award': award['@id'],
        'dataset': experiment['@id'],
        'lab': lab['@id'],
        'file_format': 'fastq',
        'file_size': 2535345,
        'platform': platform1['@id'],
        'run_type': 'paired-ended',
        'mapped_run_type': 'single-ended',
        'md5sum': '01234567890123456789abcdefabcdef',
        'output_type': 'raw data',
        'status': 'in progress',
    }


@pytest.fixture
def mapped_run_type_on_bam(award, experiment, lab):
    return {
        'award': award['@id'],
        'dataset': experiment['@id'],
        'lab': lab['@id'],
        'file_format': 'bam',
        'assembly': 'mm10',
        'file_size': 2534535,
        'mapped_run_type': 'single-ended',
        'md5sum': 'abcdef01234567890123456789abcdef',
        'output_type': 'alignments',
        'status': 'in progress',
    }


@pytest.fixture
def fastq_pair_1_paired_with(fastq_pair_1, file_fastq):
    item = fastq_pair_1.copy()
    item['paired_with'] = file_fastq['@id']
    return item


@pytest.fixture
def fastq_pair_2(fastq):
    item = fastq.copy()
    item['paired_end'] = '2'
    item['md5sum'] = '2123456789abcdef0123456789abcdef'
    return item


@pytest.fixture
def fastq_pair_2_paired_with(fastq_pair_2, fastq_pair_1):
    item = fastq_pair_2.copy()
    item['paired_with'] = 'md5:' + fastq_pair_1['md5sum']
    return item


@pytest.fixture
def external_accession(fastq_pair_1):
    item = fastq_pair_1.copy()
    item['external_accession'] = 'EXTERNAL'
    return item


@pytest.fixture
def file_18(testapp, lab, award, experiment):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'bigBed',
        'file_format_type': 'bed3+',
        'md5sum': 'eeb9325f54a0ec4991c4a3df0ed35f20',
        'output_type': 'representative dnase hypersensitivity sites',
        'assembly': 'hg19',
        'file_size': 8888,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'schema_version': '18'
    }
    return item


@pytest.fixture
def file_no_runtype(testapp, experiment, award, lab, replicate_url, platform1):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'platform': platform1['@id'],
        'award': award['@id'],
        'file_format': 'fastq',
        'output_type': 'reads',
        'md5sum': '99378c852c5be68251cbb125ffcf045a',
        'status': 'in progress',
        'read_length': 76
    }
    return item


@pytest.fixture
def file_19(testapp, experiment, award, lab, replicate_url, platform1):
    item = {
        'schema_version': '19',
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'platform': platform1['@id'],
        'award': award['@id'],
        'file_format': 'fastq',
        'output_type': 'reads',
        'md5sum': '99378c852c5be68251cbb125ffcf045a',
        'status': 'in progress',
        'read_length': 76
    }
    return item


@pytest.fixture
def file_hotspots_prefix(testapp, lab, award, experiment):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'tsv',
        'md5sum': 'eeb9325f54a0ec4991c4a3df0ed35f20',
        'output_type': 'hotspots',
        'hotspots_prefix': 'GRCh38',
        'file_size': 8888,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',
    }
    return item

@pytest.fixture
def file_hotspots1_reference(testapp, lab, award, experiment):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'tsv',
        'md5sum': 'ae26b3d8e556703291282149e3ae894f',
        'output_type': 'hotspots1 reference',
        'file_size': 8888,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',
    }
    return item


@pytest.fixture
def file_dnase_enrichment(testapp, experiment_dnase, award, lab):
    return {
        'dataset': experiment_dnase['uuid'],
        'lab': lab['@id'],
        'file_size': 13459832,
        'award': award['@id'],
        'assembly': 'GRCh38',
        'file_format': 'bed',
        'file_format_type': 'bed3+',
        'output_type': 'enrichment',
        'md5sum': '99378c852c5be68251cbb125ffcf045a',
        'status': 'in progress'
    }


@pytest.fixture
def file_chip_enrichment(testapp, experiment_chip_CTCF, award, lab):
    return {
        'dataset': experiment_chip_CTCF['uuid'],
        'lab': lab['@id'],
        'file_size': 151823,
        'award': award['@id'],
        'assembly': 'mm10',
        'file_format': 'bed',
        'file_format_type': 'bed3+',
        'output_type': 'enrichment',
        'md5sum': 'a2d0dde9ea1cbc8ec24d74c413a897f1',
        'status': 'in progress'
    }


@pytest.fixture
def file_fastq_1_atac(testapp, lab, award, ATAC_experiment, replicate_ATAC_seq, platform1):
    item = {
        'dataset': ATAC_experiment['@id'],
        'replicate': replicate_ATAC_seq['@id'],
        'file_format': 'fastq',
        'file_size': 34,
        'platform': platform1['@id'],
        'output_type': 'reads',
        "read_length": 50,
        'md5sum': '32cd74b6e19115393507f4ebfa66d77a',
        'run_type': "single-ended",
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_fastq_2_atac(testapp, lab, award, ATAC_experiment_replicated, replicate_ATAC_seq_2, platform1):
    item = {
        'dataset': ATAC_experiment_replicated['@id'],
        'replicate': replicate_ATAC_seq_2['@id'],
        'file_format': 'fastq',
        'file_size': 34,
        'platform': platform1['@id'],
        'output_type': 'reads',
        "read_length": 50,
        'md5sum': '21ab74b6e22625393507f4ebfa66d77a',
        'run_type': "single-ended",
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def ATAC_bam(testapp, encode_lab, award, ATAC_experiment, replicate_ATAC_seq,
            analysis_step_run_atac_encode4_alignment, file_fastq_1_atac):
    item = {
        'dataset': ATAC_experiment['@id'],
        'replicate': replicate_ATAC_seq['@id'],
        'file_format': 'bam',
        'md5sum': 'e52e9cd98f00b204e9800998ecf8427e',
        'output_type': 'alignments',
        'derived_from': [file_fastq_1_atac['@id']],
        'assembly': 'GRCh38',
        'lab': encode_lab['@id'],
        'file_size': 34,
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'step_run': analysis_step_run_atac_encode4_alignment['@id'],
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_bed_IDR_thresholded_peaks_atac(testapp, ATAC_experiment, ATAC_bam, award, encode_lab):
    item = {
        'dataset': ATAC_experiment['@id'],
        'lab': encode_lab['@id'],
        'award': award['@id'],
        'derived_from': [ATAC_bam['@id']],
        'file_format': 'bed',
        'file_format_type': 'idr_peak',
        'file_size': 345,
        'assembly': 'GRCh38',
        'md5sum': 'f119ab102df36d93dd070ef0712b8ee7',
        'output_type': 'IDR thresholded peaks',
        'status': 'in progress',  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_21_22(file_subreads):
    item = file_subreads.copy()
    item.update({'notes': 'Prior entry.'})
    item.pop('replicate')
    return item


@pytest.fixture
def file_23(file_base):
    item = file_base.copy()
    item['output_type'] = 'stable peaks'
    return item


@pytest.fixture
def fastq_index(testapp, lab, award, experiment, base_replicate_two, platform1, single_fastq_indexed):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'fastq',
        'md5sum': '11bd74b6e11515393507f4ebfa66d78c',
        'replicate': base_replicate_two['@id'],
        'output_type': 'index reads',
        'read_length': 36,
        'file_size': 34,
        'platform': platform1['@id'],
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',
        'index_of': [single_fastq_indexed['@id']]
        }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def single_fastq_indexed(testapp, lab, award, experiment, base_replicate, platform1):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'fastq',
        'md5sum': '91be74b6e11515393507f4ebfa66d78b',
        'replicate': base_replicate['@id'],
        'output_type': 'reads',
        'read_length': 36,
        'file_size': 34,
        'platform': platform1['@id'],
        'run_type': 'single-ended',
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress'
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def second_fastq_indexed(testapp, lab, award, experiment, base_replicate_two, platform1):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'fastq',
        'md5sum': '82cd66b6f21515393507f4ebfa66d78b',
        'replicate': base_replicate_two['@id'],
        'output_type': 'reads',
        'read_length': 36,
        'file_size': 68,
        'platform': platform1['@id'],
        'run_type': 'paired-ended',
        'paired_end': '1',
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress'
    }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def correct_paired_fastq_indexed(testapp, lab, award, experiment, base_replicate_two, platform1, second_fastq_indexed):
    item = {
            'dataset': experiment['@id'],
            'file_format': 'fastq',
            'md5sum': '23cd66b6f21515393507f4ebfa55e77c',
            'replicate': base_replicate_two['@id'],
            'output_type': 'reads',
            'read_length': 36,
            'file_size': 72,
            'platform': platform1['@id'],
            'run_type': 'paired-ended',
            'paired_with': second_fastq_indexed['@id'],
            'paired_end': '2',
            'lab': lab['@id'],
            'award': award['@id'],
            'status': 'in progress'
        }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def incorrect_paired_fastq_indexed(testapp, lab, award, experiment, base_replicate_two, platform1, single_fastq_indexed):
    item = {
            'dataset': experiment['@id'],
            'file_format': 'fastq',
            'md5sum': '82cd66b6f21515393507f4ebfa55e77c',
            'replicate': base_replicate_two['@id'],
            'output_type': 'reads',
            'read_length': 36,
            'file_size': 72,
            'platform': platform1['@id'],
            'run_type': 'paired-ended',
            'paired_with': single_fastq_indexed['@id'],
            'paired_end': '2',
            'lab': lab['@id'],
            'award': award['@id'],
            'status': 'in progress'
        }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def pacbio_fastq_indexed(testapp, lab, award, experiment, base_replicate_two, platform3):
    item = {
            'dataset': experiment['@id'],
            'file_format': 'fastq',
            'md5sum': '04cd66b6f21515393507f4ebfa55e77c',
            'replicate': base_replicate_two['@id'],
            'output_type': 'reads',
            'file_size': 720,
            'platform': platform3['uuid'],
            'lab': lab['@id'],
            'award': award['@id'],
            'status': 'in progress'
        }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def oxford_nanopore_fastq_indexed(testapp, lab, award, experiment, base_replicate, platform4):
    item = {
            'dataset': experiment['@id'],
            'file_format': 'fastq',
            'md5sum': '15dd66b6f21515393507f4ebfa55e77c',
            'replicate': base_replicate['@id'],
            'output_type': 'reads',
            'file_size': 800,
            'platform': platform4['uuid'],
            'lab': lab['@id'],
            'award': award['@id'],
            'status': 'in progress'
        }
    return testapp.post_json('/file', item, status=201).json['@graph'][0]


@pytest.fixture
def file_22(testapp, lab, award, experiment):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'fasta',
        'md5sum': 'bc37b3d8e556703291282149e3ae894f',
        'output_type': 'spike-in sequence',
        'file_size': 8888,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',
    }
    return item


@pytest.fixture
def file_bed_pseudo_replicated_peaks_atac(
    testapp,
    ATAC_experiment,
    ATAC_bam,
    award,
    encode_lab,
    analysis_step_run_atac_encode4_pseudoreplicate_concordance
):
    item = {
        'dataset': ATAC_experiment['@id'],
        'lab': encode_lab['@id'],
        'award': award['@id'],
        'derived_from': [ATAC_bam['@id']],
        'file_format': 'bed',
        'file_format_type': 'narrowPeak',
        'file_size': 345,
        'assembly': 'GRCh38',
        'md5sum': '27f0221b6d6d4052320dbce3fc434668',
        'output_type': 'pseudoreplicated peaks',
        'status': 'in progress',  # avoid s3 upload codepath
        'step_run': analysis_step_run_atac_encode4_pseudoreplicate_concordance['@id'],
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def ATAC_bam2(testapp, encode_lab, award, ATAC_experiment_replicated,
              replicate_ATAC_seq_2, analysis_step_run_atac_encode4_alignment,
              file_fastq_2_atac):
    item = {
        'dataset': ATAC_experiment_replicated['@id'],
        'replicate': replicate_ATAC_seq_2['@id'],
        'file_format': 'bam',
        'md5sum': 'f63e9cd98f00b204e9800998ecf8427e',
        'output_type': 'alignments',
        'derived_from': [file_fastq_2_atac['@id']],
        'assembly': 'GRCh38',
        'lab': encode_lab['@id'],
        'file_size': 34,
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'step_run': analysis_step_run_atac_encode4_alignment['@id'],
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_bed_replicated_peaks_atac(testapp, ATAC_experiment_replicated, ATAC_bam2,
                                   ATAC_bam, award, encode_lab,
                                   analysis_step_run_atac_encode4_partition_concordance):
    item = {
        'dataset': ATAC_experiment_replicated['@id'],
        'lab': encode_lab['@id'],
        'award': award['@id'],
        'derived_from': [ATAC_bam2['@id'], ATAC_bam['@id']],
        'file_format': 'bed',
        'file_format_type': 'narrowPeak',
        'file_size': 345,
        'assembly': 'GRCh38',
        'md5sum': 'a220ab102df36d93dd070ef0712b8ee7',
        'output_type': 'pseudoreplicated peaks',
        'status': 'in progress',  # avoid s3 upload codepath
        'step_run': analysis_step_run_atac_encode4_partition_concordance['@id']
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_bed_IDR_peaks_atac(testapp, ATAC_experiment_replicated, ATAC_bam2,
                            ATAC_bam, award, encode_lab,
                            analysis_step_run_atac_encode4_partition_concordance):
    item = {
        'dataset': ATAC_experiment_replicated['@id'],
        'lab': encode_lab['@id'],
        'award': award['@id'],
        'derived_from': [ATAC_bam2['@id'], ATAC_bam['@id']],
        'file_format': 'bed',
        'file_format_type': 'narrowPeak',
        'file_size': 345,
        'assembly': 'GRCh38',
        'md5sum': 'b331ba102df36d93dd070ef0712b8ee7',
        'output_type': 'IDR thresholded peaks',
        'status': 'in progress',  # avoid s3 upload codepath
        'step_run': analysis_step_run_atac_encode4_partition_concordance['@id']
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def ATAC_bam3(testapp, encode_lab, award, ATAC_experiment_replicated,
              replicate_ATAC_seq_3, analysis_step_run_atac_encode4_alignment,
              file_fastq_2_atac):
    item = {
        'dataset': ATAC_experiment_replicated['@id'],
        'replicate': replicate_ATAC_seq_3['@id'],
        'file_format': 'bam',
        'md5sum': 'a74f0cd98f00b204e9800998ecf8427e',
        'output_type': 'alignments',
        'derived_from': [file_fastq_2_atac['@id']],
        'assembly': 'GRCh38',
        'lab': encode_lab['@id'],
        'file_size': 34,
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'step_run': analysis_step_run_atac_encode4_alignment['@id'],
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_bed_IDR_peaks_2_atac(testapp, ATAC_experiment_replicated, ATAC_bam3,
                              award, encode_lab, ATAC_bam2,
                              analysis_step_run_atac_encode4_partition_concordance):
    item = {
        'dataset': ATAC_experiment_replicated['@id'],
        'lab': encode_lab['@id'],
        'award': award['@id'],
        'derived_from': [ATAC_bam3['@id'], ATAC_bam2['@id']],
        'file_format': 'bed',
        'file_format_type': 'narrowPeak',
        'file_size': 345,
        'assembly': 'GRCh38',
        'md5sum': 'c442cb102df36d93dd070ef0712b8ee7',
        'output_type': 'IDR thresholded peaks',
        'status': 'in progress',  # avoid s3 upload codepath
        'step_run': analysis_step_run_atac_encode4_partition_concordance['@id']
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_24(base_experiment, award, encode_lab, testapp, analysis_step_run_bam):
    item = {
        'dataset': base_experiment['uuid'],
        "file_format": "bed",
        "file_format_type": "bedMethyl",
        "file_size": 24000,
        "assembly": "mm10",
        "md5sum": "91be74b6e11515223507f4ebf266d88a",
        "output_type": "smoothed methylation stage at CpG",
        "award": award["uuid"],
        "lab": encode_lab["uuid"],
        "status": "released",
        "step_run": analysis_step_run_bam['uuid']
    }
    return item


@pytest.fixture
def file_25(testapp, lab, award, experiment):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'bigBed',
        'file_format_type': 'bed3+',
        'md5sum': 'eeb9325f54a0ec4991c4a3df0ed35f20',
        'output_type': 'representative DNase hypersensitivity sites (rDHSs)',
        'assembly': 'hg19',
        'file_size': 8888,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'schema_version': '25'
    }
    return item


@pytest.fixture
def file_26(file_base):
    item = file_base.copy()
    item['output_type'] = 'pseudo-replicated peaks'
    return item


@pytest.fixture
def file_27(testapp, lab, award, experiment):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'bigBed',
        'file_format_type': 'bed3+',
        'md5sum': 'eeb1325f54a0ec4911c4a3df0ed32f20',
        'output_type': 'blacklisted regions',
        'assembly': 'hg19',
        'file_size': 888328,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'schema_version': '27'
    }
    return item


@pytest.fixture
def file_nanopore_signal(testapp, experiment, award, lab, replicate_url, platform4):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 5768,
        'platform': platform4['@id'],
        'award': award['@id'],
        'file_format': 'tar',
        'md5sum': '0adb8693a743723d8a7882b5e9261b98',
        'output_type': 'nanopore signal',
        'status': 'in progress'
    }
    return item


@pytest.fixture
def file_fastq_1_chia(testapp, lab, encode4_award, ChIA_PET_experiment, replicate_ChIA_PET, platform1):
    item = {
        'dataset': ChIA_PET_experiment['@id'],
        'replicate': replicate_ChIA_PET['@id'],
        'file_format': 'fastq',
        'file_size': 5890125,
        'platform': platform1['@id'],
        'output_type': 'reads',
        "read_length": 75,
        'md5sum': '04cc8b52ffc78dc62df7cadd44adfedd',
        'run_type': "single-ended",
        'lab': lab['@id'],
        'award': encode4_award['@id'],
        'status': 'in progress'  # avoid s3 upload codepath
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def chia_bam(testapp, encode_lab, encode4_award, ChIA_PET_experiment, replicate_ChIA_PET, file_fastq_1_chia, analysis_step_run_chia_alignment):
    item = {
        'dataset': ChIA_PET_experiment['@id'],
        'replicate': replicate_ChIA_PET['@id'],
        'file_format': 'bam',
        'md5sum': 'eaaa33052a2a15317c0acc65a783e505',
        'output_type': 'alignments',
        'derived_from': [file_fastq_1_chia['@id']],
        'assembly': 'GRCh38',
        'lab': encode_lab['@id'],
        'file_size': 341908904,
        'award': encode4_award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'step_run': analysis_step_run_chia_alignment['@id']
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def chia_peaks(testapp, ChIA_PET_experiment, chia_bam, encode4_award, encode_lab, analysis_step_run_chia_peak_calling):
    item = {
        'dataset': ChIA_PET_experiment['@id'],
        'lab': encode_lab['@id'],
        'award': encode4_award['@id'],
        'derived_from': [chia_bam['@id']],
        'file_format': 'bed',
        'file_format_type': 'broadPeak',
        'file_size': 45892,
        'assembly': 'GRCh38',
        'md5sum': 'b8c4ccb7078163067d49ab612f55b128',
        'output_type': 'peaks',
        'status': 'in progress',  # avoid s3 upload codepath
        'step_run': analysis_step_run_chia_peak_calling['@id']
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def chia_chromatin_int(testapp, ChIA_PET_experiment, chia_bam, encode4_award, encode_lab, analysis_step_run_chia_interaction_calling):
    item = {
        'dataset': ChIA_PET_experiment['@id'],
        'lab': encode_lab['@id'],
        'award': encode4_award['@id'],
        'derived_from': [chia_bam['@id']],
        'file_format': 'hic',
        'file_size': 3908501,
        'assembly': 'GRCh38',
        'md5sum': '78f05b7a9fa61088c90b29e578a3cb43',
        'output_type': 'contact matrix',
        'status': 'in progress',  # avoid s3 upload codepath
        'step_run': analysis_step_run_chia_interaction_calling['@id']
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_ccre(testapp, lab, award, annotation_ccre):
    item = {
        'dataset': annotation_ccre['@id'],
        'file_format': 'bed',
        'file_format_type': 'bed9+',
        'output_type': 'candidate Cis-Regulatory Elements',
        'assembly': 'GRCh38',
        'file_size': 8888,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'md5sum': '7f8a39c323c56c2e56eccff0e95f3488',
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_ccre_2(testapp, lab, award, annotation_dhs, file_rDHS):
    item = {
        'dataset': annotation_dhs['@id'],
        'file_format': 'bed',
        'file_format_type': 'bed9+',
        'output_type': 'candidate Cis-Regulatory Elements',
        'assembly': 'GRCh38',
        'file_size': 8888,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'md5sum': 'fe5ec9c5d77cf6e3c95eb643591fdd8d',
        'derived_from': [file_rDHS['@id']],
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_ccre_3(testapp, lab, award, annotation_dhs, file_cDHS):
    item = {
        'dataset': annotation_dhs['@id'],
        'file_format': 'bed',
        'file_format_type': 'bed9+',
        'output_type': 'candidate Cis-Regulatory Elements',
        'assembly': 'GRCh38',
        'file_size': 8888,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'md5sum': '1beb8693a743723d8a7882b5e9261b98',
        'derived_from': [file_cDHS['@id']],
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_rDHS(testapp, lab, award, annotation_dhs):
    item = {
        'dataset': annotation_dhs['@id'],
        'file_format': 'bigBed',
        'file_format_type': 'bed3+',
        'output_type': 'representative DNase hypersensitivity sites',
        'assembly': 'GRCh38',
        'file_size': 8888,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'md5sum': '2cfb8693a743723d8a7882b5e9261b98',
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_cDHS(testapp, lab, award, annotation_dhs):
    item = {
        'dataset': annotation_dhs['@id'],
        'file_format': 'bigBed',
        'file_format_type': 'bed3+',
        'output_type': 'consensus DNase hypersensitivity sites',
        'assembly': 'GRCh38',
        'file_size': 2222,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'md5sum': '078eb6dc4e96d2d5a922f246b4088cf6',
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_28(file_base):
    item = file_base.copy()
    item.update({
        'platform': '25acccbd-cb36-463b-ac96-adbac11227e6',
        'schema_version': '28'
    })
    return item


@pytest.fixture
def file_no_readlength(testapp, experiment, award, lab, replicate_url, platform1):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 345,
        'platform': platform1['@id'],
        'award': award['@id'],
        'file_format': 'fastq',
        'output_type': 'reads',
        'md5sum': '99378c852c5be68251cbb125ffcf045a',
        'status': 'in progress',
        'run_type': 'single-ended'
    }
    return item


@pytest.fixture
def file_sequence_barcodes(testapp, lab, award, experiment):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'tsv',
        'output_type': 'sequence barcodes',
        'file_size': 2222,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'md5sum': '514ddb776705756a52f8b46cec90f3d7',
    }
    return item


@pytest.fixture
def file_subreads_posted(testapp, experiment, award, lab, replicate_url, platform3):
    item = {
        'dataset': experiment['@id'],
        'replicate': replicate_url['@id'],
        'lab': lab['@id'],
        'file_size': 5768,
        'platform': platform3['@id'],
        'award': award['@id'],
        'file_format': 'bam',
        'md5sum': '4dc593c21fa5ef4088b384c0f3c49aac',
        'output_type': 'subreads',
        'status': 'in progress'
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def fragments_file_csv(testapp, experiment, award, lab):
    item = {
        "assembly": "GRCh38",
        "award": award['@id'],
        'dataset': experiment['@id'],
        "date_created": "2021-08-11T21:32:51.463118+00:00",
        "file_format": "csv",
        "file_size": 1522674567,
        'lab': lab['@id'],
        "md5sum": "f140dcda5101928714b1ca967c6e4ea2",
        "output_type": "fragments",
        "status": "in progress"
    }
    return item


@pytest.fixture
def archr_project_file(testapp, experiment, award, lab):
    item = {
        "assembly": "GRCh38",
        "award": award['@id'],
        'dataset': experiment['@id'],
        "file_format": "tar",
        "file_size": 16000555,
        'lab': lab['@id'],
        "md5sum": "b1ebd74b6e11928714b1ca96517c6bd4",
        "output_type": "archr project",
        "status": "in progress"
    }
    return item


@pytest.fixture
def hic_chromatin_int(testapp, intact_hic_experiment, encode4_award, encode_lab, analysis_step_run_hic_chromatin_interactions):
    item = {
        'dataset': intact_hic_experiment['@id'],
        'lab': encode_lab['@id'],
        'award': encode4_award['@id'],
        'file_format': 'hic',
        'file_size': 14653403584,
        'assembly': 'GRCh38',
        'md5sum': '78f05b7a9fa61088c90b29e578a3cb4a',
        'output_type': 'contact matrix',
        'filter_type': 'mapping quality',
        'filter_value': 1,
        'status': 'in progress',  # avoid s3 upload codepath
        'step_run': analysis_step_run_hic_chromatin_interactions['@id']
    }
    return testapp.post_json('/file', item).json['@graph'][0]


@pytest.fixture
def file_29(testapp, lab, award, experiment):
    item = {
        'dataset': experiment['@id'],
        'file_format': 'bigBed',
        'file_format_type': 'bed3+',
        'md5sum': 'd9729feb74992cc3482b350163a1a010',
        'output_type': 'chromatin interactions',
        'assembly': 'hg19',
        'file_size': 888328,
        'lab': lab['@id'],
        'award': award['@id'],
        'status': 'in progress',  # avoid s3 upload codepath
        'schema_version': '29'
    }
    return item
