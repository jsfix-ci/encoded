// Require all components to ensure javascript load ordering
require('./lib');
require('./view_controls.js');
require('./antibody');
require('./app');
require('./award');
require('./image');
require('./biosample');
require('./cart');
require('./collection');
require('./datacolors');
require('./dataset');
require('./dbxref');
require('./errors');
require('./experiment');
require('./genetic_modification');
require('./footer');
require('./globals');
require('./graph');
require('./doc');
require('./donor');
require('./encyclopedia');
require('./file');
require('./item');
require('./page');
require('./platform');
require('./facets');
require('./search');
require('./report');
require('./rnaget');
require('./matrix_audit');
require('./matrix_entex');
require('./matrix_brain');
require('./matrix_mouse_development');
require('./matrix_experiment');
require('./matrix_reference_epigenome');
require('./matrix_sescc_stem_cell');
require('./matrix_chip_seq');
require('./matrix_encore');
require('./target');
require('./publication');
require('./pipeline');
require('./software');
require('./testing');
require('./edit');
require('./inputs');
require('./blocks');
require('./user');
require('./schema');
require('./summary');
require('./region_search');
require('./gene');
require('./biosample_type');
require('./experiment_series');
require('./glossary');
require('./series_search');
require('./single_cell');
require('./top_hits');


module.exports = require('./app');
