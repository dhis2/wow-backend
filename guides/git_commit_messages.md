# Git Commit Message Principles

The following guidelines for Git commit messages are put in place to make it easy to follow the developments in the various Git branches. We would like to have a concise and consistent commit history so that it becomes an effective tool for communication between developers .For inspiration have a look at the [Spring Boot](https://github.com/spring-projects/spring-boot/commits/master) project.


## Principles

1. **Limit the subject line to 70 characters:** Ensure that the subject is informative, short and concise and fits within the GitHub commit history for easy browsing.

2. **Start the message with a prefix:** Start with a prefix in lower-case followed by colon. Try to use one of the following prefixes: `feat: `, `fix:`, `chore:`, `ci:`, `docs:`, `refactor:`, `perf:`, `test:`.

3. **Refer to Jira issue:** Include a reference to a Jira issue as often as possible in the commit message. Specify the issue ID in brackets, e.g. like this: [DHIS2-6299].

3. **Capitalize the subject line:** Write proper English and being all subject lines with a capital letter. For example use  "Introduced performance boost option", not "introduced performance boost option".

4. **Do not end the subject line with a period**: Trailing punctuation is unnecessary in subject lines and space is precious when limiting the subject line length.

5. **Use the imperative mood in the subject line:** Imperative means as if giving a command. Start the subject lines with a verb. Examples: "Update spacecraft launch module", "Refactor JSONB user type". Good verbs to start the subject with are: Add, Fix, Start, Refactor, Reformat, Optimize, Introduce, Document.

6. **Use the body to explain what and why:** Use git commit message bodies to communicate what you are doing and why. This is very helpful to other developers to stay up to date on developments in master.

7. **Avoid generic messages**: Avoid using generic commit messages like "Minor fix" and "Clean-up", rather explain what you are doing and why you are doing it.

### Prefix overview

The table below shows availabe prefixes and their purpose.

Prefix | Purpose
--- | ---
feat: | New feature
fix: | Bug fix
chore: | Clean-up and maintenance
ci: | Change related to continuous integration
docs: | Documentation such as Javadoc
refactor: | Code refactor
perf: | Performance improvement
test: | Unit or integration test

### Example commit messages

Some example commit messages are listed below.

    feat: Add new endpoint for static images [DHIS2-7656]

    fix: Expire user sessions at password change [DHIS2-7355]

    chore: Clean up code for attribute value service
