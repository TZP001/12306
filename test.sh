python3 /mnt/g/python/img/train.py &
while(true)
do
	tk=`curl -s http://localhost:5000/get_tk`
	if [ "$tk"x != "$tk_o"x ]; then
		sed -i 's/tk =.*/tk = '\"$tk\"'/' /mnt/g/Twinzo/123066/TickerConfig.py
		killall python3
		python3 /mnt/g/python/img/train.py &
		python3 /mnt/g/Twinzo/123066/run.py r &
		tk_o="$tk"
	fi
	sleep 60
done
