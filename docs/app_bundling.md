# 2.43 App Bundling Process

## Overview

This document explains the new Java-based application bundling process introduced to improve the speed of DHIS2 builds. This new mechanism replaces the previous approach that relied on the `frontend-maven-plugin` to clone app repositories via Git during the build.

The primary goal is to fetch pre-packaged application ZIP archives directly, eliminating the overhead and potential failures associated with cloning Git repositories and managing Node.js dependencies for this part of the build.

## The Build Process: A Backend Developer's Perspective

As a Java developer, when you run a standard Maven build (e.g., `mvn clean install`), you will notice the new app bundling process during the `dhis-web-server` module's lifecycle.

### How It Works

1. **Maven Execution**: The process is triggered during the `prepare-package` phase of the `dhis-web-server` module. The `pom.xml` for this module uses the `exec-maven-plugin` to run a standalone Java application.

   ```xml
   <plugin>
     <groupId>org.codehaus.mojo</groupId>
     <artifactId>exec-maven-plugin</artifactId>
     <executions>
       <execution>
         <id>bundle-apps</id>
         <goals>
           <goal>java</goal>
         </goals>
         <phase>prepare-package</phase>
         <configuration>
           <mainClass>org.hisp.dhis.web.appbundler.AppBundler</mainClass>
           <!-- System properties are passed here -->
         </configuration>
       </execution>
     </executions>
   </plugin>
   ```

2. **AppBundler Tool**: The `org.hisp.dhis.web.appbundler.AppBundler` class is the core of this new process. You will see its log output in your console during the build. It performs the following steps:
   * **Reads App List**: It reads the list of applications to bundle from `dhis-web-server/apps-to-bundle.json`. This file contains a list of GitHub repository URLs.
   * **Downloads App Archives**: For each URL, it constructs a "codeload" URL to download the repository's source code as a ZIP archive directly from GitHub for a specific branch or tag.
   * **Efficient Caching with ETags**: The bundler is designed for efficiency. It stores the HTTP `ETag` of each downloaded ZIP file. On subsequent builds, it sends the stored ETag in an `If-None-Match` header. If the app hasn't changed on GitHub, the server responds with a `304 Not Modified`, and the download is skipped. This significantly speeds up consecutive builds.
   * **Output**: The downloaded app ZIP files are stored in the build directory, typically `dhis-web-server/target/dhis-web-apps/`. Alongside the ZIP files, it generates a manifest file named `apps-bundle.json`. This manifest contains metadata about all the bundled apps, including their name, original URL, branch, and the ETag from the download.

This entire process is self-contained within the JVM, making it faster, more reliable, and independent of external tools like Node.js.

## Server Startup and App Installation

The installation of the bundled apps happens automatically when the DHIS2 server starts up.

- The `BundledAppManager` service locates the `apps-bundle.json` manifest on the classpath.
- It iterates through the list of apps in the manifest. For each app, it compares the `etag` from the bundle manifest with the `etag` of the app that is currently installed in the DHIS2 instance (if any).
- If an app is not installed, or if the etags differ (indicating a new version), the `BundledAppManager` triggers a re-installation of the app from the corresponding ZIP file found in the classpath.

This ensures that the DHIS2 instance always runs the versions of the apps that were bundled during the last successful build. It ensures that all the apps, either pre-bundled, installed manually or installed via the app-hub are installed and stored the same way, all using the JCloudStorageService for handling the storage. This means that all apps now “live” in the DHIS2_HOME/files/app folder, if you are using local storage.


