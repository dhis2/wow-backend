# Code formatting (master)

## Maven Plugin

DHIS2 (master) is now using Spotless (https://github.com/diffplug/spotless) to automatically format the code base.
We used to use Speedy Spotless, but this project is now deprecated and archived.

### Step 1: Installing pre-commit hook

From the DHIS2 project root ([dhis2-core/dhis-2](https://github.com/dhis2/dhis2-core/blob/master/dhis-2)), create a file called `pre-commit.spotless` with this content:
```bash
#!/bin/sh
# From gist at https://gist.github.com/chadmaughan/5889802
# Version 2 (05/25/23)

echo '[git hook] executing mvn spotless:check before commit'

# stash any unstaged changes
git stash -q --keep-index

# Initialize the RESULT variable to 0
RESULT=0

# Run mvn spotless:check for each directory, capturing exit codes
for dir in ./dhis-2 ./dhis-2/dhis-test-e2e
do
  cd $dir; mvn spotless:check
  # If mvn command fails, update RESULT to 1
  if [ $? -ne 0 ]
  then
    RESULT=1
  fi
  # Go back to the root directory before the next iteration
  cd - > /dev/null
done

# unstash the unstashed changes
git stash pop -q

# return the 'mvn spotless:check' exit code
exit $RESULT
```

Then execute the commands below to move it to the .git/hooks folder and make it executable:
```bash
mv ./pre-commit.spotless ../.git/hooks/pre-commit
chmod +x ../.git/hooks/pre-commit
```

This will install the pre-commit hook that invoke Spotless Maven plugin command `spotless:check`. When you try to do a commit and the format check fails, the commit will abort before you can write the commit message and show which files failed.

**Note:** Make sure that git `core.hooksPath` is set to `.git/hooks` in order for Spotless to work.

    git config core.hooksPath .git/hooks

**Note:** If your commit hook fails to run in IntelliJ and gives this error message: `.git/hooks/pre-commit: line 11: mvn: command not found`, this means IntelliJ does not have the same PATH as you do in your terminal, and you need to tell it what your path is. You can do this by running this command on the command line, and copy it into the `../.git/hooks/pre-commit` file:

`'echo $PATH'` paste that content rigth above line 10 in the pre-commit, `'cd ./dhis-2; mvn spotless:check'`.

### Step 2: Commit your code

When committing your code, Spotless will check the format of the staged files, using the current DHIS2 Eclipse formatting rules:

[dhis2-core/dhis-2/DHISFormatter.xml](https://github.com/dhis2/dhis2-core/blob/master/dhis-2/DHISFormatter.xml)

A conditional formatting can be used to prevent the automatic formatter to format blocks of code:

```java
// @formatter:off
IN_USER_ORG_UNIT_HIERARCHY_CACHE = cacheProvider.newCacheBuilder( Boolean.class )
    .forRegion( "inUserOuHierarchy" )
    .expireAfterWrite( 3, TimeUnit.HOURS )
    .withInitialCapacity( 1000 )
    .forceInMemory()
    .withMaximumSize( SystemUtils.isTestRun(env.getActiveProfiles() ) ? 0 : 20000 ).build();
// @formatter:on
```

## Eclipse

### Step 1: Eclipse formatting definition location

The DHIS2 XML formatting definition is located in the DHIS2 project root: [dhis2-core/dhis-2/DHISFormatter.xml](https://github.com/dhis2/dhis2-core/blob/master/dhis-2/DHISFormatter.xml)

### Step 2: Add the formatting definition file to Eclipse

1. Open Eclipse preferences
2. In the search bar on the left, type “formatter”, and select the Java -> Code Style -> Formatter menu item.
3. Click “Import” and browse to the XML formatting definition file.
4. Ensure the "DHIS 2.0 Formatter" item is selected in the “Active profile” section.
5. Click "OK".

### Step 3: Configure auto-formatting when saving a file (optional)

1. In the Preferences menu (same as in Step 2), type “save actions”, and select Java -> Editor -> Save Actions.
2. Select “Perform the selected actions on save”.
3. Select “Format source code”.
4. Click the “Formatter” link and ensure the “DHIS 2.0 Formatter” formatter is selected as active.
5. Click OK.

## IntelliJ Idea

### Step 1: Download the formatting definition

Locate the Eclipse formatting definition, same as in Step 1 for Eclipse.

### Step 2: Install the Eclipse Code Formatter plugin

1. Open Intellij preferences.
2. In the search bar on the left, type "plugin", and select Marketplace.
3. In the search plugin bar, type "Eclipse Code Formatter" and select it
4. Click "Install" on the plugin page
5. Restart IntelliJ

### Step 3: Configure the Eclipse Code Formatter plugin

1. Open Intellij preferences.
2. In the search bar on the left, type "eclipse", and select Other Settings -> Eclipse Code Formatter.
3. Select "Use the Eclipse code formatter"
4. Select Selected Profile -> <Project Specific>
5. Select Supported file types -> Enable Java
6. Select Java Formatter Version -> Eclipse 4.9.0 2018-09 and Import ordering style for Eclipse 4.5.1+
7. Set the "Eclipse Java Formatter config file" to the location of the DHIS2 XML formatting definition file.
8. Set the "Java Formatting Profile" to "DHIS 2.0 Formatter".
9. Select "Optimize imports"
10. Copy import order from spotless plugin config in main pom.xml to the "Manual Import Order" field.

## Maintenance

To run the plugin from the commmand line and fix all the unformatted files, execute:

    mvn spotless:apply
