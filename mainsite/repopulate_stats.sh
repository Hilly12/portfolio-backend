#!/bin/bash
cd "$(dirname "$0")"
echo $(date -u) >> log.txt
source ../env/bin/activate
python scripts/fetch_stats.py
python manage.py runscript repopulate_stats
deactivate
cd /
