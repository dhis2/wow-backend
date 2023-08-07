# Code formatting

DHIS2 follows the [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html).
This guide is enforced via [Spotless](https://github.com/diffplug/spotless) in our CI pipeline. 

## Apply formatting

The following section describes multiple options for you to format your code according to the style
guide.

### Option 1: Format via your IDE

#### IntelliJ Idea

##### Step 1: Download the Google formatter plugin

Download the Google Java format plugin and follow the setup instructions
https://github.com/google/google-java-format

##### Step 2: Configure auto-format on save (optional)

1. Open IntelliJ preferences
2. Enable `Reformat code` in Tools -> Actions on Save

#### Eclipse

##### Step 1: Download the Google formatter plugin

Download the Google Java format plugin and follow the setup instructions
https://github.com/google/google-java-format

### Option 2: Format manually

To format the entire project run

```sh
mvn spotless:apply -f ./dhis-2/pom.xml
mvn spotless:apply -f ./dhis-2/dhis-web/pom.xml
mvn spotless:apply -f ./dhis-2/dhis-test-e2e/pom.xml
```

Note: Maven module `dhis-web` will be removed. As building `dhis-web` is time consuming it is not a
submodule of `dhis-2/pom.xml`. This allows only building the API. Maven module `dhis-test-e2e` is
not a submodule of `dhis-2/pom.xml` as its testing DHIS2 via its HTTP APIs without sharing any code.

### Option 3: Format via pre-commit hook

We could create a Git pre-commit hook to format staged changes before creating a commit. What the
correct behavior is quickly becomes complicated when you have staged and unstaged changes to the
same file, maybe even the same piece of code. Spotless might get such a feature in the future, see
https://github.com/diffplug/spotless/issues/623

## Disable formatting

The Google Java formatter cannot be disabled by design.

## Check formatting

### Option 1: Check manually

To check the entire project is formatted correctly run

```sh
mvn spotless:check -f ./dhis-2/pom.xml
mvn spotless:check -f ./dhis-2/dhis-web/pom.xml
mvn spotless:check -f ./dhis-2/dhis-test-e2e/pom.xml
```

### Option 2: Check via pre-commit hook

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

