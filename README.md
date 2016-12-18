


# 安装说明
Python版本: 3.5

pip3 install pycrypto # 用于AES加密

# 运行方法
python run_client.py

python run_server.py

（一次只能运行一个server，但可以运行N个client）

# 配置文件
server和client共用```config.json```
```
    {
      "crypto": {
        "base": ..,
        "modulus": ...
      },
      "client": {
        "server_ip": "127.0.0.1",
        "server_port": 8111
      },
      "server": {
        "bind_ip": "0.0.0.0",
        "bind_port": 8111
      }
    }
```ß