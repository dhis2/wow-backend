# Project Lombok DHIS2 guide

As of DHIS2 2.34 we now allow usage of [Project Lombok](https://projectlombok.org/) in our code, it does however come with some restrictions.

## IDE setup

To have Lombok function properly in IDEs like Intellij and Eclipse you will have to enable APT (annotation processing tool) and also install a plugin which helps with auto-complete etc, a nice guide for this can be found [here](https://www.baeldung.com/lombok-ide).

Maven already supports APT (through the lombok depdendency), so for CI servers etc no additional setup is needed.

Occasionally IntelliJ tends to get out of sync with lombok and shows errors related to generated code even if setup is correct and compilation works.
In such case use `File` => `Invalidate Caches / Restart...`.
