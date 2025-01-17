## Changelog for ucsc_browser_composite.json

### Minor changes since schema version 17

* Added *LRGASP* and *ENCYCLOPEDIAv6* to the *internal_tags* enums list
* Added *doi* property
* Added *analyses* property
* Added *RushAD* and *YaleImmuneCells* to the *internal_tags* enum
* Added *Deeply Profiled* to the *internal_tags* enum
* Added *Degron* to *internal_tags* enums list.

### Schema version 17

* Update the dbxref regex to remove IHEC; this is only allowed for Annotation and ReferenceEpigenome objects

### Schema version 16

* Update IHEC dbxref regex to remove version number

### Minor changes since schema version 15
* Added *MouseDevSeries* enum to *internal_tags*
* Removed *month_released* calculated property.

### Schema version 15

* *internal_tags* removes *cre_inputv10* and *cre_inputv11*, and adds *ENCYCLOPEDIAv5*, *ccre_inputv1*, and *ccre_inputv2*.

### Schema version 14

* Replace *started* enum in *status* with *in progress*.

### Schema version 13

* *proposed* removed from *status* enum (*dataset* mixin).

### Schema version 12

* *alternate_accessions* now must match accession format, "ENCSR..." or "TSTSR..."
