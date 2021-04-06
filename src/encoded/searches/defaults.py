OPTIONAL_PARAMS = [
    'annotation',
    'cart',
    'datastore',
    'debug',
    'field',
    'filterresponse',
    'format',
    'frame',
    'from',
    'genome',
    'limit',
    'mode',
    'referrer',
    'region',
    'remove',
    'sort',
    'type',
]

FREE_TEXT_QUERIES = [
    'advancedQuery',
    'searchTerm',
]

RESERVED_KEYS = NOT_FILTERS = OPTIONAL_PARAMS + FREE_TEXT_QUERIES

DEFAULT_ITEM_TYPES = [
    'Analysis',
    'AntibodyLot',
    'Award',
    'Biosample',
    'BiosampleType',
    'Dataset',
    'Document',
    'Donor',
    'GeneticModification',
    'Page',
    'Pipeline',
    'Publication',
    'Software',
    'Gene',
    'Target',
    'File',
    'Lab',
]

TOP_HITS_ITEM_TYPES = [
    'AntibodyLot',
    'Award',
    'Biosample',
    'BiosampleType',
    'Annotation',
    'Experiment',
    'Document',
    'HumanDonor',
    'FlyDonor',
    'WormDonor',
    'MouseDonor',
    'GeneticModification',
    'Page',
    'Pipeline',
    'Publication',
    'Software',
    'Gene',
    'Target',
    'File',
    'Lab',
    'GeneSilencingSeries',
    'ReferenceEpigenome',
    'OrganismDevelopmentSeries',
    'TreatmentTimeSeries',
    'ReplicationTimingSeries',
    'MatchedSet',
    'TreatmentConcentrationSeries',
    'AggregateSeries',
    'FunctionalCharacterizationExperiment',
    'TransgenicEnhancerExperiment',
    'Reference',
    'PublicationData',
]
