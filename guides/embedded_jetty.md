# DHIS2 API with Embedded Jetty 

## Compiling and starting an embedded Jetty container from the command line

The module called "dhis2-embedded-jetty" in the dhis2-core project is responsible for configuring and starting up an embedded Jetty container, and exposing the DHIS2 API on the default port of 9080.

> **NOTE:** To skip the compile of the new "dhis2-embedded-jetty" module and basickly get the same compile time as before you can do the following to exlude it from the build:
    
    mvn clean install -Pdev -Pjdk11 -T 100C -pl -dhis-web-embedded-jetty

### Step 1: Compiling the DHIS2 core

From the root dhis2 directory, execute:

    mvn clean install -Pdev -Pjdk11 -T 100C

### Step 2: Set DHIS2 home directory and run jar file

From the root dhis2 directory, execute:
    
    DHIS2_HOME=[your dhis2 home] \ 
    java -jar ./dhis-web-embedded-jetty/target/dhis-web-embedded-jetty.jar
    
*TIP: You can also define the port and host/ip you want like this:*

    java -Djetty.host=$HOST -Djetty.http.port=$PORT -jar ./dhis-web-embedded-jetty/target/dhis-web-embedded-jetty.jar
    
#### Alternative:

The runApi.sh script will do exactly the same as above, but you will need to define your DHIS2_HOME first.

#### Step 1: Set DHIS2_HOME

From the root dhis2 directory, execute:

    export DHIS2_HOME=[Your dhis2 home dir.]
    
#### Step 2: Run runApi.sh script

From the root dhis2 directory, execute:

    ./runApi.sh

    
## Starting an embedded Jetty container from IntelliJ

You can also easily start the Jetty container directly from your IDE.

#### Step 1: Open JettyEmbeddedCoreWeb.java file
Open the JettyEmbeddedCoreWeb.java file in the "dhi2-web-embedded-jetty" module.

#### Step 2: Click the play button on the main method
![](resources/images/intellij-embedded-play.png)

#### Step 3: Edit run configuration
When clicking the play button, chose the last entry "Modify Run Configuration..."

#### Step 4: Add the DHIS2_HOME env var to the configuration
![](resources/images/intellij-embedded-config.png)

After setting the DHIS2_HOME variable, click "OK".

#### Step 5: Click play again and choose run or debug 
![](resources/images/intellij-embedded-run.png)
