# autoPushProject

这是一个将本地文件上传到远程服务器的一个程序，主要目的是为了将在本地生成的网站代码上传到服务器的网站根目录中。

虽然需求简单，但是需要日志，进度条，备份，ssh连接，sftp文件上传这些功能。

## ![Snipaste_2023-02-16_12-52-17](https://shihao-icu-1304033786.cos.ap-shanghai.myqcloud.com/shihao.icu/Snipaste_2023-02-16_12-52-17.png)

## 目录简介

```
├─lib
│  ├─__init__.py
│  ├─tools.py # 功能模块
├─log # 日志存放路径
├─tmp # 文件备份路径
├─main.py # 主程序
├─config.xml # 配置文件
```

## config 配置

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<host_config>
    <!-- centos这个名字并不固定，同时可以多个，但是名字不能相同 -->
    <centos>
        <!-- 主机IP地址 -->
        <hostname>192.168.79.128</hostname>
        <!-- 登录方式：login（用户名密码登录） 和 key（私钥登录） -->
        <auth>login</auth>
        <!--私钥地址，登录方式为key时需要，否则可以不写-->
        <rsa>C:\\Users\\shihao\\.ssh\\id_rsa</rsa>
        <!-- 端口 -->
        <port>22</port>
        <!-- 用户名称 -->
        <username>root</username>
        <!-- 用户密码，登录方式为login时需要，否则可以不写 -->
        <password>1232</password>
        <!-- 需要上传的本地目录-->
        <localpath>G:\\example\\dist</localpath>
        <!-- 上传到远程服务器的目录 -->
        <remotepath>/tmp/dist.zip</remotepath>
        <!-- 上传后进行远程命令执行 -->
        <command>rm -rf /root/html/*;cd /root/html/;mv /tmp/dist.zip ./;unzip dist.zip</command>
    </centos>
</host_config>
```

## 命令运行

创建虚拟环境（可选）

```shell
python -m venv venv
# 运行虚拟环境
./venv/Script/active.ps1
```

安装依赖

```shell
pip install -r requirements.txt
```

运行程序需要一个参数，就是配置文件中的`centos`标签，主程序会通过你提供的标签在配置文件中查找，并获取到你的配置信息

```python
python main.py centos 
```

下面是运行结果

![autoPushProject](https://shihao-icu-1304033786.cos.ap-shanghai.myqcloud.com/shihao.icu/autoPushProject.gif)

