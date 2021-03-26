* 油猴脚本安装 [地址](https://github.com/Famine-Life/get12306cookie)
* 修改脚本（未完成）
```
// 修改发送的url
var text = JSON.stringify(data)
var obj = JSON.parse(text);
xmlhttp.open("GET", "http://127.0.0.1:5000/set_tk/" + obj.tk, true);
xmlhttp.open("GET", "http://127.0.0.1:5000/set_rd/" + obj.RAIL_DEVICEID, true);
xmlhttp.open("GET", "http://127.0.0.1:5000/set_re/" + obj.RAIL_EXPIRATION, true);
xmlhttp.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
console.log("JSON==================",obj.tk);
```
