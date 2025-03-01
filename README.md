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

## create-release.yml

A release should be created on 'main' after the CI tests pass.

## check-version.yml

Developers should not touch the VERSION file! It is automatically updated by a workflow when a branch is merged into 'main'.

This workflow checks for changes made to the VERSION file. It should block changes made by the developer, but it should let changes pass if they were merged in from 'main'.

## Workflows

Developer pushes to pull request branch --> build-and-test.yml

Developer pushes to 'main' --> update-version.yml --> build-and-test.yml --> create-release.yml

## Merge conflicts

Committing new versions in update-version.yml may lead to conflicting commits if we try to merge two pull requests at the same time. [Concurrency groups](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#concurrency) won't work: 

> When a concurrent job or workflow is queued, if another job or workflow using the same concurrency group in the repository is in progress, the queued job or workflow will be pending. Any existing pending job or workflow in the same concurrency group, if it exists, will be canceled and the new queued job or workflow will take its place.

I should investigate merge queues.
