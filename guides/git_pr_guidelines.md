# Git Pull Request Guidelines

The following guidelines apply when raising pull requests:

## Guidelines

**1. Keep the PR as small as possible:** Do as little as possible for each PR and try to only include one feature per PR. The exception is strong dependencies between features. If you come across areas which need clean-up or refactor then create a new, separate PR for that.

**2. Follow the code style:** There are many opinions on code style but we need to adhere to the same one, so pleas follow the code style and clean up the formatting.

**3. Tidy up the code:** Remove unused import statements, commented out code and unused code. Add license. Add proper Javadoc to methods and classes.

**4. Fix deprecation warnings:** If you upgrade libraries and it leads to deprecation warnings, please fix it and introduce the upgrade path as early as possible to avoid code debt.

**5. Write a clear commit message and description:** Write a good commit message and description for the PR according to the guide `Git Commit Message Principles`.

**6. Write and run tests:** Ensure new features have appropriate test coverage and are covered by at least some unit tests. Run all unit tests and ensure that they pass.

**7. Use draft mode for drafts:** If you are raising a PR which is not yet ready for merging, e.g. for getting review and comments from others, then create a _draft_ PR. From _Create Pull Request_, click the down arrow and select _Create Draft Pull Request_.
