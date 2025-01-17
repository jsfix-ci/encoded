## Changelog for pipeline.json

### Minor changes since schema version 14
* Added *proliferation CRISPR screen*, *FACS CRISPR screen*, and *FlowFISH CRISPR screen* to *assay_term_names* enum

### Schema version 14

* Added *LC/MS label-free quantitative proteomics*, *LC-MS/MS isobaric label quantitative proteomics*, and *Ribo-seq* to *assay_term_names* enum. *assay_term_names* enum *Capture Hi-C* was changed to *capture Hi-C*

### Schema version 13

* Added *perturbation followed by scRNA-seq* and *perturbation followed by snATAC-seq* to *assay_term_names* enum; *single-cell ATAC-seq* was removed from the *assay_term_names* enum and remapped to *single-nucleus ATAC-seq*

### Schema version 12

* Added *GRO-cap*, *GRO-seq*, and *long read single-cell RNA-seq* to *assay_term_name* enum;  *single-nucleus RNA-seq* and *genotyping by high throughput sequencing assay* were removed and remapped to *single-cell RNA sequencing assay* and *whole genome sequencing assay* respectively

### Minor changes since schema version 11
* Added *CUT&RUN* to *assay_term_names* enum
* Added *SPRITE-IP* to *assay_term_names* enum
* Added *CUT&Tag* to *assay_term_name* enum
* Added *Capture Hi-C* and *single-nucleus RNA-seq* to *assay_term_names* enum

### Schema version 11

* *assay_term_names* enum *single cell isolation followed by RNA-seq* was changed to *single-cell RNA sequencing assay*

### Minor changes since schema version 10
* *reference_filesets* property was added to link related reference file sets to each pipeline

### Schema version 10

* *assay_term_names* enum *single-nuclei ATAC-seq* was changed to *single-nucleus ATAC-seq*

### Minor changes since schema version 9

* *pipeline_version* was set to have a minimum of 1.

### Schema version 9

* Add *revoked* to possible statuses and change *active* to *released*.

### Schema version 8

* *assay_term_name* property was replaced by *assay_term_names*, a list of assay names consistent with the pipeline type
* *pipeline_version* property was added to represent pipeline version

### Schema version 7

* *alternate_accessions* now must match accession format, "ENCPL..." or "TSTPL..."

### Schema version 6

* *aliases* now must be properly namespaced according lab.name:alphanumeric characters with no leading or trailing spaces
* unsafe characters such as " # @ % ^ & | ~ ; ` [ ] { } and consecutive whitespaces will no longer be allowed in the alias

### Schema version 5

* *assay_term_id* is no longer allowed to be submitted, it will be automatically calculated based on the *term_name*, if present

### Schema version 4

* Array properties *analysis_steps*, *aliases*, *documents* and *references* must contain unique elements

### Schema version 3

* *version* field was removed
* *end_points* was removed
* *name* was removed

### Schema version 2

* *lab* field added
* *award* field added
