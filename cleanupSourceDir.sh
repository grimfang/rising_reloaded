#!/bin/sh
echo "removing pyc files"
find . -name '*.pyc' -delete
echo "removing pyo files"
find . -name '*.pyo' -delete
echo "removing ~ (backup) files"
find . -name '*.*~' -delete