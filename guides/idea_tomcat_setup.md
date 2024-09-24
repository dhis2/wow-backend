# IntelliJ IDEA Project Setup Guide

This guide assumes you have already installed Tomcat on your machine. 
Additionally, the Maven and Tomcat and Java EE plugins are required, but they come bundled with IntelliJ IDEA and are enabled by default. Unless you have manually disabled them, your environment should be ready.


To ensure a smooth setup, follow these steps to configure your project in IntelliJ IDEA:

1. Build with Maven. Run the following commands from the command line:
    - `mvn clean install -f dhis-2/pom.xml -DskipTests=true`

    if you are using version 2.41 or older, run this command too:
    - `mvn clean install -f dhis-2/dhis-web/pom.xml -DskipTests=true`

2. Import Project to IntelliJ:
    - Continue by importing the project from your local sources into IntelliJ.

3. Add as Maven Project:
    - Right-click on the project's pom.xml and select "Add as Maven Project".

4. If you are on 2.41 or older, configure the Maven Project:
    - In the plugin list on the right side, click on Maven.
    - Add the web portal project to the list of Maven projects.
    - Make sure it's part of the list of modules in `/File/Project Stucture/Modules`. If it's not, add it to the list.

5. Configure Local Tomcat:
    - Open the configurations menu and add a new local Tomcat configuration.
    - In the _Deployment_ tab:
        1. From 2.42 on, add the artifact named _dhis-web-server:war exploded_. 
        2. Up until 2.41, add the artifact named _dhis-web-portal:war exploded_. 
        This will automatically select this artifact for build before launch. 
![](resources/images/deploy.png)

6. Configure Tomcat Settings:
    - Navigate to the _Server_ tab.
    - Choose an available port in your local URL.
    - In both options _on update action_ and _on frame deactivation_, select _update classes and resources_ if you need to enable hot swap functionality.
![](resources/images/tomcat-setting.png)

7. Set Environment Variable:
    - In the _Startup/Connection_ tab, add a new environment variable called ***DHIS2_HOME***. Repeat this action for the Debug profile too.
    - Set the value to your configuration file.

8. Configure Logging (optional):
    - Go to the _Logs_ tab and click on Save console output to file.
    - Choose a file, preferably the Catalina file of your local Tomcat, to store logs.