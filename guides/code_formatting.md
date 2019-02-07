### Code formatting

#### Eclipse

#### Step 1: Eclipse formatting definition location

The DHIS 2 XML formatting definition is located in the DHIS 2 project root: [dhis2-core/dhis-2/DHISFormatter.xml](https://github.com/dhis2/dhis2-core/blob/master/dhis-2/DHISFormatter.xml)

#### Step 2: Add the formatting definition file to Eclipse

1. Open Eclipse preferences
2. In the search bar on the left, type “formatter”, and select the Java -> Code Style -> Formatter menu item.
3. Click “Import” and browse to the XML formatting definition file.
4. Ensure the "DHIS 2.0 Formatter" item is selected in the “Active profile” section.
5. Click "OK".

#### Step 3: Add the formatting definition file to Eclipse (optional)

1. In the Preferences menu (same as in Step 2), type “save actions”, and select Java -> Editor -> Save Actions.
2. Select “Perform the selected actions on save”.
3. Select “Format source code”.
4. Click the “Formatter” link and ensure the “DHIS 2.0 Formatter” formatter is selected as active.
5. Click OK.


#### IntelliJ Idea

#### Step 1: Download the formatting definition

Locate the Eclipse formatting definition, same as in Step 1 for Eclipse.

#### Step 2: Install the Eclipse Code Formatter plugin

1. Open Intellij preferences.
2. In the search bar on the left, type "plugin", and select Marketplace.
3. In the search plugin bar, type "Eclipse Code Formatter" and select it
4. Click "Install" on the plugin page
5. Restart IntelliJ

#### Step 3: Configure the Eclipse Code Formatter plugin

1. Open Intellij preferences.
2. In the search bar on the left, type "eclipse", and select Other Settings -> Eclipse Code Formatter.
3. Select "Use the Eclipse code formatter"
4. Select Selected Profile -> <Project Specific>
5. Select Supported file types -> Enable Java
6. Select Java Formatter Version -> Eclipse 4.9.0 2018-09 and Import ordering style for Eclipse 4.5.1+
7. Set the "Eclipse Java Formatter config file" to the location of the DHIS2 XML formatting definition file.
8. Set the "Java Formatting Profile" to "DHIS 2.0 Formatter".
9. Select "Optimize imports"