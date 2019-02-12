# Git Pull Request Guidelines

The following guidelines apply when raising pull requests:

## Guidelines

**1. Keep the PR as small as possible:** Do as little as possible for each PR and try to only include one feature per PR. The exception is strong dependencies between features. If you come across areas which need clean-up or refactor then create a new, separate PR for that.

**2. Follow the code style:** There are many opinions on code style but we need to adhere to the same one, so pleas follow the code style and clean up formatting before raising the PR.

**3. Tidy up the code:** Remove unused import statements, commented out code and unused code. Add license. Add proper Javadoc to methods and classes.

**4. Fix deprecation warnings early:** If you upgrade libraries and it leads to deprecation warnings, please fix it and introduce the upgrade path as early as possible to avoid code debt.

**5. Write a clear commit message and description:** Write a good commit message and description for the PR according to the guide `Git Commit Message Principles`.
