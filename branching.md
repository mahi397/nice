# Key Branches:

`main`:
This branch contains the production-ready code.
No direct commits. Changes are merged into this branch only after they are thoroughly reviewed and tested.

`develop`:
This is the integration branch for ongoing development.
New features and fixes are merged into this branch.
All developers regularly pull updates from develop.


# Supporting Branches:

1. Feature Branches:

Used to develop specific features.
Branch off from develop and merge back into develop.
Naming convention: feature/<feature-name> (e.g., feature/user-auth, feature/payment-system).

2. Bugfix Branches:

For fixing bugs found in develop or main.
Branch off from develop (or main for critical fixes) and merge back into the source branch.
Naming convention: bugfix/<bug-name>.

3. Release Branches:

Used to prepare a release for deployment.
Branch off from develop and merge into both develop and main after testing.
Naming convention: release/<version> (e.g., release/v1.0).

4. Hotfix Branches:

For urgent fixes in main.
Branch off from main and merge into both main and develop.
Naming convention: hotfix/<issue-name>.


<img width="476" alt="image" src="https://github.com/user-attachments/assets/8c2fc757-e4dc-4b71-a1ce-3195cf1bc944">
