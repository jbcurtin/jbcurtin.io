#!/usr/bin/env bash

set -x
set -e

status=$(git status --porcelain=v1|wc -l|awk '{print $1}')
if [ "$status" -gt "0" ]; then
    echo 'Commit files before publishing'
    exit 1
fi

zola build
rm -rf ./docs || true
mv public docs
cat >> ./docs/CNAME <<EOF
jbcurtin.io
EOF
git add docs
git commit -m 'Zola Publish' -a
git push github draft
