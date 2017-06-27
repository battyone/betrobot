#!/bin/bash -xe

find data/providers -type f -name "provider-*.pkl" \
    -exec echo "==================================================" \; \
    -exec echo "{}" \; \
    -exec echo "" \; \
    -exec python3 betrobot/scripts/propose.py "{}" proposed \; \
    -exec echo "" \; \
    -exec echo "==================================================" \; \
    -exec echo "" \;
