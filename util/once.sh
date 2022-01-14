#!/usr/bin/env bash

if [ "$#" -ne 2 ]; then
    echo "Usage: once.sh html|latex dir"
    exit 1
fi

python -m mccole -C $2 -g $1.yml -L debug
echo "---- difference ----"
diff -r $2/tmp $2/$1
