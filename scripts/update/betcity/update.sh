#!/bin/bash -xe


date -R
today=$(date "+%Y-%m-%d")

rm -rf tmp/update/betcity
mkdir -p tmp/update/betcity

./node_modules/.bin/xvfb-maybe nodejs scripts/update/betcity/stage1.js
python3 scripts/update/betcity/stage2.py

python3 scripts/update/incorporate.py

mv -f tmp/update/betcity/datesHtml/* data/betcityDatesHtml

rm -rf tmp/update/betcity
