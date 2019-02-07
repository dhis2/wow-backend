# Testing guidelines

## Technology stack
* [JUnit 4](https://junit.org) 
* [TestContainers](https://www.testcontainers.org): library providing lightweight, throwaway instances of common databases or anything else that can run in a Docker container.

### Integration testing

#### Prerequisites:

1) Docker installed.
    - [Docker for mac](https://docs.docker.com/docker-for-mac/)
    - [Docker for linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/)


#### TestContainers
First time application context is loaded, test containers will start two docker containers: ryuk and postgres. Ryuk container is responsable for killing no longer used postgres containers. 
Every time when ApplicationContext is reloaded new postgres container will be started with fresh database. 

Postgres version: 10

#### Executing tests
```sh
$ mvn test -Pintegration
```

#### Creating integration test
- Annotate class with category IntegrationTest.class: 

  ``
    @org.junit.experimental.categories.Category( IntegrationTest.class )
  ``
  
- Extend IntegrationTestBase class
