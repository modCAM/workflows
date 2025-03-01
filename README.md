## update-version.yml

The version should be updated whenever changes are made to 'main'. To update the version, this workflow should
- checkout the code,
- update the VERSION file,
- amend the last commit to include the bumped VERSION file, and
- tag that commit with the new version.

## build-and-test.yml

The CI workflow should run whenever changes are pushed to a pull request branch or to 'main'. For any changes pushed to 'main', the CI workflow should only run after a version update. This workflow should
- set up the build environment (use a container?),
- checkout the code,
- build the code,
- run linting checks, and
- run unit tests.

This is a test.