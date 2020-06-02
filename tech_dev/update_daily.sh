#!/bin/bash
d=`date +%y-%m-%d_%H:%M:%S`
echo 'Running update at' $d
# Running daily update of the exchange rates.
cd $STOCKS_PATH
echo `pwd`

