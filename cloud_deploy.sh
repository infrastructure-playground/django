#!/usr/bin/env sh

yes YES | gcloud app deploy app.yml

if [$? == 141]
then
    exit 0
else
    echo "Experienced exit code $?"
    exit $?
fi