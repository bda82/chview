#!/bin/bash

set -e

export LANG="en_US.UTF-8"

if [ "$1" = "run" ] || [ "$1" = "" ]; then
  command="cd /usr/src/desire/chview && \
    python3 chview.py"
else
  command="exec sh"
fi

eval "${command}"