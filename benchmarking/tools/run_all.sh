#!/bin/bash

set -e

for f in $1/*.sh; do
  bash "$f"
done
