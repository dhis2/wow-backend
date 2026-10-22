# Run DHIS2 with embedded Tomcat
<!-- Author: Morten (Morty) <netroms@gmail.com> -->

Embedded mode runs DHIS2 directly from an executable WAR, without installing a separate servlet container. The `dhis-web-server` module starts Tomcat through `org.hisp.dhis.web.tomcat.Main`; the executable WAR uses the Spring Boot WAR launcher to invoke that class. It is not a Spring Boot application with Spring Boot command-line configuration.

Embedded Tomcat exists in the source from 2.42, but the 2.42/2.43 executable builds do not start as released: use 2.44 or later for the supported embedded mode described here, or external Tomcat for older versions.

For production setup, systemd, TLS and upgrades, see [Run DHIS2 with embedded Tomcat in the official documentation](https://docs.dhis2.org/en/manage/getting-started/run-dhis2-with-embedded-tomcat.html).

## Prerequisites

- Java 17 JDK and Maven for building from source.
- A running PostgreSQL database with PostGIS, configured for DHIS2.
- A writable `DHIS2_HOME` directory containing `dhis.conf` with the database connection settings. It is a directory, not the path to `dhis.conf` itself.

Run the following commands from the **dhis2-core repository root**.

## Quickstart

With `dhis.conf` prepared in `/opt/dhis2`:

```sh
export DHIS2_HOME=/opt/dhis2
./dhis-2/run-api.sh
```

The script builds the executable WAR and starts DHIS2 at [http://localhost:9090/](http://localhost:9090/). The API is at `http://localhost:9090/api/`.

| Flag | Purpose |
|---|---|
| `-d /path/to/home` | Set the DHIS2 home directory; otherwise use `DHIS2_HOME`, falling back to `/opt/dhis2`. |
| `-p 9091` | Select the HTTP port; the script defaults to **9090**. |
| `-s` | Skip the build and run the existing `dhis-2/dhis-web-server/target/dhis.war`. |

For example, restart an existing build on another port:

```sh
./dhis-2/run-api.sh -s -d /opt/dhis2 -p 9091
```

Stop with Ctrl-C. From 2.44, shutdown closes the Spring context, stops Tomcat and removes its temporary directory; SIGTERM uses the same shutdown hook.

## Build and run the executable WAR

```sh
mvn clean package -f dhis-2/pom.xml -pl dhis-web-server -am -P embedded -DskipTests
DHIS2_HOME=/opt/dhis2 java -jar dhis-2/dhis-web-server/target/dhis.war
```

Unlike `run-api.sh`, a direct `java -jar` launch defaults to **8080**, with no context-path prefix. Open [http://localhost:8080/](http://localhost:8080/).

The `embedded` profile packages the launcher and embedded container dependencies. Release WARs from [releases.dhis2.org](https://releases.dhis2.org/) are executable from DHIS2 2.44. To check a downloaded file saved as `dhis.war`:

```sh
unzip -p dhis.war META-INF/MANIFEST.MF | grep Main-Class
```

The main class is `org.springframework.boot.loader.launch.WarLauncher`. A WAR without a `Main-Class` cannot be started with `java -jar`.

### App bundling

Normal builds include web apps. For a faster backend-only development build, add `-Dskip.bundle.apps=true` to the Maven command above. The resulting WAR has no bundled apps; this does not remove apps already installed in your DHIS2 home. See [App bundling](../docs/app_bundling.md) for the build and startup installation process.

## Port, context path and JVM options

| Setting | JVM system property | Environment variable | Default |
|---|---|---|---|
| HTTP port | `-Dserver.port=9090` | `SERVER_PORT` | `8080` |
| Context path | `-Dserver.servlet.context.path=/dhis2` | `SERVER_SERVLET_CONTEXT_PATH` | Root, no prefix |
| Forwarded headers (2.44+) | `-Dserver.forward-headers-strategy=native` | `SERVER_FORWARD_HEADERS_STRATEGY` | `none` |
| Internal proxy addresses (2.44+) | `-Dserver.tomcat.remoteip.internal-proxies=<regex>` | `SERVER_TOMCAT_REMOTEIP_INTERNAL_PROXIES` | Tomcat's loopback and private-network list |

System properties take precedence over environment variables. `run-api.sh -p` supplies the port as a system property, so it also takes precedence over `SERVER_PORT`. Put JVM options **before** `-jar`, or in `JAVA_TOOL_OPTIONS`:

```sh
DHIS2_HOME=/opt/dhis2 java -Xms512m -Xmx1536m \
  -Dserver.port=9090 -Dserver.servlet.context.path=/dhis2 \
  -jar dhis-2/dhis-web-server/target/dhis.war
```

This serves `http://localhost:9090/dhis2/`; the API moves to `/dhis2/api/`. With a context path configured, `/` is not the application root.

Arguments after `-jar dhis.war` are ignored, including `--server.port=9090`. Embedded mode does not read `setenv.sh`, `CATALINA_OPTS` or `server.xml`. It binds all network interfaces, so firewall the application port rather than assuming it is local-only.

### Behind a reverse proxy

Use `native` when a trusted reverse proxy terminates HTTPS. It honours `X-Forwarded-For`, `X-Forwarded-Proto`, `X-Forwarded-Port` and `X-Forwarded-Host` from trusted proxies. Restrict direct access to the backend and override the internal-proxy regex if your proxy is outside Tomcat's default list.

Configure the proxy to use HTTP/1.1 upstream, preserve the public Host including its port, and supply forwarded headers. In `dhis.conf`, set `server.base.url` to the public URL and `server.https = on`; configure HSTS at the proxy. These settings do not create an embedded TLS listener.

Without the forward-headers strategy, the default OIDC callback can use `http` behind an HTTPS proxy. With `native` and correctly forwarded headers, it uses `https`. An explicit `oidc.provider.<id>.redirect_url` is also available; include your context path. See the official guide linked above for the full nginx configuration.

## Running from IntelliJ IDEA

Import `dhis-2/pom.xml` as a Maven project and build it using the command above first. Create an **Application** run configuration with these settings:

| Setting | Value |
|---|---|
| Main class | `org.hisp.dhis.web.tomcat.Main` |
| Use classpath of module | `dhis-web-server` |
| Include dependencies with provided scope | Enabled, under **Modify options** |
| JRE | Java 17 |
| Working directory | The repository's `dhis-2` directory |
| Environment variables | `DHIS2_HOME=/opt/dhis2`, or your own home directory |
| VM options | `-Xms512m -Xmx1536m -Dserver.port=9090 -Dlog4j.appender=console_color` |
| Program arguments | Leave empty; they do not configure embedded Tomcat. |

Add `-Dserver.servlet.context.path=/dhis2` to VM options if needed. Choose **Run** to start normally, or set breakpoints and choose **Debug** to debug the same main class. Rebuild changed classes before relaunching; standard JVM hot swap can apply supported changes while debugging.

For multiple nodes, duplicate the configuration and give each a different home directory and port. See [Local DHIS2 API cluster with Redis and nginx](cluster_with_redis.md).

## Logging

Console logging defaults to the plain `console` appender. Use `-Dlog4j.appender=console_color` for coloured development output. DHIS2 also writes `DHIS2_HOME/logs/dhis.log` and area-specific logs. A custom `-Dlog4j2.configurationFile=/path/to/log4j2.xml` replaces the default logging configuration. Under systemd, console output is captured by journald.

## Development Docker images

Start Docker and prepare the repository's development `.env` from `.env.example`. For its local demo database, retain the example's `DB_USERNAME` and `DB_PASSWORD` defaults, and set `DHIS2_IMAGE=dhis2/core-dev:local` so Compose selects the image you build rather than `latest`. From the dhis2-core repository root:

```sh
./dhis-2/build-dev.sh
docker compose up
```

Open `http://localhost:8080/`. This setup supplies its own database and mounted `dhis.conf`; it does not use the host's `DHIS2_HOME`.

The `dhis2/core-dev` images use embedded Tomcat from 2.43 onwards. The `dhis2/core` images still use external Tomcat, so their `CATALINA_OPTS` examples do not configure embedded mode. Use `JAVA_TOOL_OPTIONS` for JVM options in embedded containers. The repository's Compose setup is for development; see [docker-deployment](https://github.com/dhis2/docker-deployment) for production containers.

Tomcat is bundled into the embedded application, so upgrading DHIS2 also updates the bundled container. If you enable the OAuth2 authorization server, configure a persistent PKCS12 keystore using `oauth2.server.jwt.keystore.*` for stable signing keys. Otherwise each restart generates a new key and previously issued access tokens are rejected, though refresh tokens continue to work.
