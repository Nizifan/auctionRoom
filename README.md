# 功能
- [x] 启动时Diffie-Hellman 密钥交换安全传输
- [x] 用AES加密所有的传输内容
- [x] 查看聊天室内用户（上线/下线自动更新）
- [x] 多人聊天功能（服务器群发）
- [x] 包分为OpCode和Parameters，用binary序列化反序列化Parameters
- [x] PyQt5 GUI
- [x] 读写配置文件
- [x] 聊天室中添加“系统消息”（当有新用户进入/用户下线时）
- [x] 窗口放大缩小
- [x] 接收服务器的公告消息
- [x] 选择发送对象：发送给所有人/悄悄话发送给一人
- [x] 进入聊天室/客户端重启时从服务器获取之前的消息


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