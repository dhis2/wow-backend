# Data Value Set Import/Export

## Export
Exporting data value sets is quite straight forward.
The `DataValueSetStore` implementation takes care of assembling the lookup
SQL based on the `DataExportParams` provided. 

Each row of the database query `ResultSet` is fed to the `DataValueSetWriter`
using the `DataValueEntry` as adopter interface.
By choosing different implementations of the `DataValueSetWriter` the export
to different formats is implemented supporting XML, JSON, CSV.

Writing a set first writes the header via `writeHeader` followed by many calls 
to `writeValue` one for each matching row of the database query.
The header contains the common properties of the values, such as the 
data element or organisation unit.

## Import
Importing data via data value sets is more complicated process because:

* referenced metadata needs to be provided "cached"
* validation needs to be performed on the changes
* changes can create/update or delete values
* data value set sources work different in how they provide the data values
  and therefore how they need to be processed

Similar to the export there is a `DataValueSetReader` used as an adopter to
the different import formats XML, JSON, CSV that. Again the `DataValueEntry`
interface is used to represent each data value. 
This can either be an actual `DataValue` in case values are provided via mapped 
input from `DataValueSet#getDataValues` or format specific adapter 
implementation when values are provided from `DataValueSetReader#readNext`.

### Import-Steps

Steps within the overall import process:

1. reading header (metadata references common to all values)
2. prepare caches or header referenced metadata
3. create context (manages the import state, such as caches and "flags" and options)
4. validate data set level, abort is invalid  
5. loop data values import from header `DataValueSet#getDataValues`
6. loop data values import from `DataValueSetReader#readNext` 
7. prepare "summary"

An import reader (is supposed to) either use the `DataValueSet#getDataValues`
in case the values are mapped and then processed, or use 
`DataValueSetReader#readNext` in case the values are stream processed where
one value at a time is mapped and processed.

Each value in the loops undergoes the following steps:

1. create value context
2. prehead caches (of the context)
3. validate data value (change)
4. apply value change (create/update/delete/ignore)

Note that changes that effectively do not change the value of existing data 
values are also ignored.

### Validation
As the steps outline there are 2 phases of validation:

1. validation of the data set (the common metadata references)
2. validation of each data value (change)

Both types of validation are handled by the `DataValueSetImportValidator`.
Each data set validation method implements the `DataSetValidation` functional
interface, each data value validation method implements the 
`DataValueValidation` functional interface method.

The sequence of the validations is important. While most of the rules are
independent some rules make assumptions that other issues have already been
ruled out. Also, the validation error report responses are expected to 
bring up certain issues with higher priority which is why those rules come first.

When validation fails in data set validation this means the import is aborted.
No data value changes will be imported. On the other hand, if validation of a
data value fails the value change is simply ignored and an error added to the
report.

### Reports
The reports `ImportSummary` used for data value set imports have one important 
difference to reports used in metadata imports. 
In metadata each error adds an entry to a flat list of entries.
Reoccurring types of errors of the same type simply create more entries in the list.

For the data value set import each `ImportConflict` reflects a type of error.
Any value that has the same type of error is referenced in the same conflict
by its index in the data value input. This is so that the report does not
explode with huge lists of conflicts in case a large import shows same 
problem for all data values. Instead, this results in a single error
referencing all the values that have it by index. As a consequence of this
a `ImportConflict` cannot describe the unique key combination of the data
value(s) that have the same issue. It just can refer to common qualities.
These are the parameters used when creating an `ImportConflict`.
A conflict with different parameters (of the same type) is understood or managed
as a separate `ImportConflict`. How qualities are used to group issues to
single conflict objects follows no special logic other than what is useful
as feedback.

### Contexts
The different context objects `ImportContext`, `DataSetContext` and 
`DataValueContext` are really just a place to group the state of the import that 
otherwise would need to be passed around in many individual parameters.
The separation into the 3 classes is mainly due to the different points during
the import where all necessary inputs are known. 

First the overall `ImportContext` is created holding all the options and import 
"global" state, like the metadata caches. 

When the data value set header has been read the `DataSetContext` is created
to perform the set level validation.

While looping the imported data `DataValueContext` is created mainly to group
data needed during data validation and to apply the change.
