#!/bin/bash
d=`date +%y-%m-%d_%H:%M:%S`
echo 'Running update at' $d
# Running daily update of the exchange rates.
echo `pwd`
python3 update_daily.sh
echo 'Run finished.'
