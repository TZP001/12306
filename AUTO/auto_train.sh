#!/bin/sh
# $1 train.py 路径
python3 ../train.py &
while(true)
do
	tk=`curl -s http://localhost:5000/get_tk`
	rd=`curl -s http://localhost:5000/get_rd`
	re=`curl -s http://localhost:5000/get_re`
	if [ "$tk"x != "$tk_o"x ]; then
		sed -i 's/tk =.*/tk = '\"$tk\"'/' ../TickerConfig.py
		killall python3
		python3 ../train.py &
		python3 ../run.py r &
		tk_o="$tk"
	fi
	sleep 60
done
