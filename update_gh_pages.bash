#!/bin/bash

TMPDIR="/tmp/livespool-docs-site"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

do_stash_pop=true
# Stash any changes before continuining
if [ "$(git stash --include-untracked)" = "No local changes to save" ]; then
    do_stash_pop=false
fi

# Generate the html docs
mkdocs build

# Move them to /tmp so we can copy over to gh-pages
sudo rm -rf $TMPDIR
cp -r "site" $TMPDIR

# checkout gh-pages and copy over new docs
git checkout gh-pages
sudo rm -rf *
cp -r ${TMPDIR}/* .

# Commit/push new docs
git add .
git commit -am "Update documentation"
git push origin gh-pages

# Clean up any crud, return to branch and put back changes
git clean -fd
git checkout $CURRENT_BRANCH
if $do_stash_pop; then
    git stash pop
fi
