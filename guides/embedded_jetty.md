# DHIS2 API with Embedded Jetty 

The DHIS 2 backend API can be built as a JAR file and deployed with an embedded Jetty server for rapid development and testing.

## Quickstart

Build the JAR file and serve up the Jetty web server by running the provided script in the `dhis-2` directory:

```sh
./run-api.sh
```

This will make the API accessible at the following URL. Note that by browsing the API URLs in the browser, the browser will typically present a built-in authentication dialog.

```
http://localhost:9090/api/
```

## Compiling and starting an embedded Jetty container from the command line

The module called `dhis2-embedded-jetty` in the dhis2-core project is responsible for configuring and starting up an embedded Jetty container, and exposing the DHIS2 API on the default port which is `9090`.

Note that JDK 11 is required to run the API with the embedded Jetty server. Also note that no web apps will bee included in the build.

To skip the compile of the new `dhis2-embedded-jetty` module and get the same compile process as before you can do the following to exclude it from the build:

```sh
mvn clean install -Pdev -Pjdk11 -T 100C -pl -dhis-web-embedded-jetty
```

### Step 1: Compiling the DHIS2 core

From the root dhis2 directory, execute:

```sh
mvn clean install -Pdev -Pjdk11 -T 100C
```

### Step 2: Set DHIS2 home directory and run jar file

From the root dhis2 directory, execute:

```sh    
DHIS2_HOME=[your dhis2 home] \ 
java -jar ./dhis-web-embedded-jetty/target/dhis-web-embedded-jetty.jar
```

*TIP: You can also define the port and host/ip you want like this:*

```sh
java -Djetty.host=$HOST -Djetty.http.port=$PORT -jar ./dhis-web-embedded-jetty/target/dhis-web-embedded-jetty.jar
```

#### Alternative

The `run-api.sh` script will do exactly the same as above, but you will need to define your DHIS2_HOME first.

#### Step 1: Set DHIS2_HOME

From the root dhis2 directory, execute:

```sh
export DHIS2_HOME=[Your dhis2 home dir.]
```

#### Step 2: Run the bash script

From the root dhis2 directory, execute:

```sh
./run-api.sh
```
    
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


## Running embedded Jetty with front-end
From 2.40 the emedded Jetty server now also support serving the front-end.
Rigth now, as of January 2023 there exist a developement/preview version of Struts less front-end build into the embedded Jetty module.
In order to use this, you just need to follow the same instructions above in order to run the embedded Server with a front-end.
There are currently some caveats, that is intended to be resolved when all the front-end apps have migrated to the new Struts less backend.
Mainly the password reset, self-registration, two factor login is not supported in this development preview.
Normal form/username password login is supported and is now the default redirect when trying to access the server trough e.g http://localhost:9090/api etc.
There are also some apps that is currently unsupported and will not work at all, these are:
* Old data entry
* Old tracker capture

See PR: https://github.com/dhis2/dhis2-core/pull/12663

Follow progress on epic: https://dhis2.atlassian.net/browse/DHIS2-14092


