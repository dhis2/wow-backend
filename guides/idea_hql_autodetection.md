# Enable HQL Entity detection in IntelliJ
We use Hibernate as our ORM, using mapping files (`.hbm.xml`) to define the entities. IntelliJ provides the ability to detect valid Entities (and properties) when writing `HQL`. This guide will go through those steps to set this up.

## Previously, with no Entity detection
`HQL` looks like this in IntelliJ:  
(a) `Section` entity is not recognised as a valid Entity  
(b) `s.dataElementsss` is not detected to be invalid (misspelling)  
(c) There are no Entity property suggestions when using dot notation on the variable  

![](resources/images/intellij-no-entity-detection.png)  

## Enabling Entity detection
### 1. New file added
A new file (`ide-entity-mapping.xml`) has been added to the project, in location: `dhis-service-core/src/main/resources`.

### 2. Add a new Hibernate facet in IntelliJ
Navigate to the new file and you should be presented with a prompt to add a new facet. 
   ![](resources/images/intellij-add-facet-prompt.png)  

Click on the prompt and add choose `dhis-service-core`  
![](resources/images/intellij-choose-service-core.png)

### 3. Observe new behaviour
Build the `dhis-service-core` module (so jar is available) to enable detection, noting the new abilities:  
   (a) The `Section` entity is now detected by the IDE  
   (b) The `s.dataElementsss` property shows as invalid (misspelled)  
   (c) Valid properties are shown as if using Java   
      ![](resources/images/intellij-with-entity-detection.png)  

## Other info
This is just purely to provide a link from the mapping files for the IDE. We configure the persistence layer programmatically (also loading the mapping files), so this won't interfere with that process.  
We do plan on moving to annotation-based mapping in the future. If this stops working then we can look into a new configuration for this behaviour.  
The `jar` mapping was selected for ease of use. We have over a hundred mapping files (didn't want to list them individually). Any new mappings will be automatically included in the `jar`.
