# fqSou —— 一个很烂的shadowsocks管理系统
[http://fqsou.com](http://fqsou.com)

## 部署方式
Python Tornado项目
使用Supervisor部署

1. 安装pip
1. 安装tornado，supervisor
1. 安装supervisor
1. 创建Shadowsocks配置文件shadowsocks.json //`_comment`是注释给自己看的

		{
		    "server": "fqsou.com",
		    "port_password": {
		        "8388": "xxxxxxx",
		    },
		    "_comment": {
		        "8388": "myself",
		    },
		    "local_address": "127.0.0.1",
		    "local_port": 1080,
		    "timeout": 300,
		    "method": "aes-256-cfb",
		    "fast_open": false
		}

1. 修改supervisor配置文件
最后加入以下内容

		[program:fqSou]
		command=python fqSou.py
		directory=/opt/fqSou
		autostart=true
		autorestart=true
		exitcodes=0
		stopsignal=KILL
		redirect_stderr=true
		numprocs=1
		process_name=%(program_name)s_%(process_num)02d

输入通过8000端口即可访问，后面Nginx做个反向代理就随意了
管理员账号密码在config.properties文件中，下面是shadowsocks.json文件的路径，请按实际情况设置。

感谢[Shadowsocks](https://github.com/shadowsocks/shadowsocks "Shadowsocks")项目！
