#!/bin/sh
# $1 train.py 路径
python3 ../train.py &
while(true)
do
	tk=`curl -s http://localhost:5000/get_tk`
	rd=`curl -s http://localhost:5000/get_rd`
	re=`curl -s http://localhost:5000/get_re`
	change=false
	if [ "$tk"x != "$tk_o"x ]; then
		sed -i 's/tk =.*/tk = '\"$tk\"'/' ../TickerConfig.py
		change=true
		tk_o="$tk"
	fi
	if [ "$rd"x != "$rd_o"x ]; then
		sed -i 's/RAIL_DEVICEID = .*/RAIL_DEVICEID = '\"$rd\"'/' ../TickerConfig.py
		change=true
		rd_o="$rd"
	fi
	if [ "$re"x != "$re_o"x ]; then
		sed -i 's/RAIL_EXPIRATION =.*/RAIL_EXPIRATION = '\"$re\"'/' ../TickerConfig.py
		change=true
		re_o="$re"
	fi
	if [ $change = true ]; then
		killall python3
		python3 ../train.py &
		python3 ../run.py r &
	fi
	sleep 60
done
