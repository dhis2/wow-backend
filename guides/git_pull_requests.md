# GitHub Pull Request Guidelines

The following guidelines apply when raising pull requests.

## Guidelines

**1. Keep the PR as small as possible:** Do as little as possible for each PR and try to only include one feature per PR. The exception is strong dependencies between features. If you come across areas which need clean-up or refactor then create a new, separate PR for that.

**2. Follow the code style:** code that does not adhere to our [formatting conventions](./code_formatting.md) will not pass the formatting check.

**3. Tidy up the code:** Remove unused import statements, commented out code and unused code. Add license. Add proper Javadoc to methods and classes.

**4. Fix deprecation warnings:** If you upgrade libraries and it leads to deprecation warnings, please fix it and introduce the upgrade path as early as possible to avoid code debt.

**5. Write a clear commit message and description:** Write a good commit message and a description for the PR according to the guide [Git Commit Message Principles](https://chris.beams.io/posts/git-commit/). For more detail see the [commit message guide](https://github.com/dhis2/wow-backend/blob/master/guides/git_commit_messages.md).
  * Separate subject from body with a blank line
  * Limit the subject line to 50 characters
  * Capitalize the subject line
  * Do not end the subject line with a period
  * Use the imperative mood in the subject line
  * Wrap the body at 72 characters
  * Use the body to explain what and why vs. how

**6. Write and run tests:** Ensure new features have appropriate test coverage and are covered by at least some unit tests. Run all unit tests and ensure that they pass.

**7. Use draft mode for drafts:** If you are raising a PR which is not yet ready for merging, e.g. for getting review from others, then create a _draft_ PR. From _Create Pull Request_, click the down arrow and select _Create Draft Pull Request_.
