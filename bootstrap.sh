#! /bin/bash

export PYTHONPATH="$PYTHONPATH:$(pwd)"
export PBT_PLUGINS_PATH="$PBT_PLUGINS_PATH:plugins"

bin/pbt "$@"
