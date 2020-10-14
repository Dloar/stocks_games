#!/bin/bash
d=`date +%y-%m-%d_%H:%M:%S`
echo 'Running update at' $d
# Running daily update of the exchange rates.
echo `pwd`

export STOCKS_PATH=~/Documents/GitHub/stocks_games/python_dev
python3 ../python_dev/send_mail.py
echo 'ENDE'
