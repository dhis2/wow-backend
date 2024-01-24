# IntelliJ IDEA Project Setup Guide

Follow these detailed steps to set up your project in IntelliJ IDEA seamlessly:

1. Import Project from GitHub:
    - Begin by importing the project from GitHub into IntelliJ.

2. Build with Maven. Run the following commands from the command line:
    - `mvn clean install -f dhis-2/pom.xml`
    - `mvn clean install -f dhis-2/dhis-web/pom.xml`

3. Add as Maven Project:
    - Right-click on the project's pom.xml and select "Add as Maven Project".

4. Configure Maven Projects:
    - In the plugin list on the right side, click on Maven.
    - Add the web project to the list of Maven projects.

5. Configure Local Tomcat:
    - Open the configurations menu and add a new local Tomcat configuration.
    - In the deployment tab, add the artifact named _dhis-web-portal:war exploded_.
![](resources/images/deploy.png)

6. Configure Tomcat Settings:
    - Navigate to the server tab.
    - Choose an available port in your local URL.
    - In both options _on update action_ and _on frame deactivation_, select _update classes and resources_ to enable hot swap functionality (Remember these settings will only take effect if IntelliJ is run in ***DEBUG*** mode and any change which involve modification in signature of the class will ***NOT*** trigger Hotswap.).
![](resources/images/tomcat-setting.png)

7. Configure Logging:
    - Go to the logs tab and click on Save console output to file.
    - Choose a file, preferably the Catalina file of your local Tomcat, to store logs.

8. Set Environment Variable:
    - In the _startup/connection_ tab, add a new environment variable called ***DHIS2_HOME***. Repeat this action for the Debug profile too.
    - Set the value to your configuration file.