#!/bin/bash
cd "$(dirname "$0")"
echo $(date -u) >> log.txt
source ../env/bin/activate
python manage.py runscript repopulate_stats
deactivate
cd /
