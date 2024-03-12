#!/bin/sh
# $1 train.py 路径
killall python3
python3 $1/AUTO/train.py &

sleep 5
tk=`curl -s http://localhost:5000/get_tk`
sed -i 's/tk =.*/tk = '\"$tk\"'/' $1/TickerConfig.py
python3 $1/run.py r &

while(true)
do
	tk=`curl -s http://localhost:5000/get_tk`
#	rd=`curl -s http://localhost:5000/get_uk`
#	re=`curl -s http://localhost:5000/get_je`
	change="false"
	if [ "$tk"x != "$tk_o"x ]; then
		sed -i 's/tk =.*/tk = '\"$tk\"'/' $1/TickerConfig.py
		change="true"
		echo "修改文件"
		tk_o="$tk"
	fi
#	if [ "$rd"x != "$rd_o"x ]; then
#		sed -i 's/uKey = .*/uKey = '\"$rd\"'/' $1/TickerConfig.py
#		change=true
#		rd_o="$rd"
#	fi
#	if [ "$re"x != "$re_o"x ]; then
#		sed -i 's/JSESSIONID =.*/JSESSIONID = '\"$re\"'/' $1/TickerConfig.py
#		change=true
#		re_o="$re"
#	fi

	if [ $change = "true" ]; then
		killall python3
		python3 $1/AUTO/train.py &
		echo "重新运行"
		python3 $1/run.py r &
	fi
	sleep 30
done
