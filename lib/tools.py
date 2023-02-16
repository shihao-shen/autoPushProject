import shutil
import os
import time
import paramiko
import xml.etree.ElementTree as elementTree

from loguru import logger


def compressZip(path):
    file_name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    base_path = f"{os.path.abspath('.')}\\tmp\\{file_name}"
    zip_path = shutil.make_archive(base_path, "zip", path)
    logger.info(f"压缩 {path} ")
    return zip_path


def translate_byte(B):
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)
    GB = float(MB ** 2)
    TB = float(GB ** 2)
    if B < KB:
        return '{} {}'.format(B, 'bytes' if B > 1 else 'byte')
    elif KB < B < MB:
        return '{:.2f} KB'.format(B / KB)
    elif MB < B < GB:
        return '{:.2f} MB'.format(B / MB)
    elif GB < B < TB:
        return '{:.2f} GB'.format(B / GB)
    else:
        return '{:.2f} TB'.format(B / TB)


def process_bar(current, total, prefix='', auto_rm=True):
    bar = '=' * int(current / total * 50)
    bar = f' {prefix} |{bar.ljust(50)}| ({current}/{total}) {current / total:.1%} | '
    print(bar, end='\r', flush=True)
    if auto_rm and current == total:
        print(end=('\r' + ' ' * len(bar) + '\r'), flush=True)


def call_back(curr=100, total=100):
    bar_length = 100
    percents = '\033[32;1m%s\033[0m' % round(float(curr) * 100 / float(total), 2)
    filled = int(bar_length * curr / float(total))
    bar = '\033[32;1m%s\033[0m' % '=' * filled + '-' * (bar_length - filled)
    # print('translating: [{}] {}% already complete: {}, total: {}\r'.format(bar, percents, translate_byte(curr),
    #                                                                        translate_byte(total)), end='')

    if int(round(float(curr) * 100 / float(total), 2)) <= 99:
        print("\r上传进度： [{}] {}% {}".format(bar, percents, translate_byte(curr)), end='')
    else:
        print("", end='\r')


def connectHost(config):
    client = paramiko.SSHClient()
    try:
        if config['auth'] == "login":
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(config['hostname'], config['port'], config['username'], config['password'])
        elif config['auth'] == "key":
            pka = paramiko.RSAKey.from_private_key_file(config['rsa'])
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=config['hostname'], port=config['port'], username=config['username'], pkey=pka)
        logger.info(f"连接 {config['hostname']}")
    except paramiko.ssh_exception.AuthenticationException as err:
        logger.debug(f"连接出错：{err}")
        exit(1)
    return client


def getXMLConfig(key):
    tree = elementTree.parse('config.xml')
    root = tree.getroot().find(key)
    config = {
        "hostname": root.find("hostname").text,
        "username": root.find("username").text,
        "auth": root.find("auth").text,
        "rsa": root.find("rsa").text if root.find("rsa") is not None else "",
        "port": int(root.find("port").text),
        "password": root.find("password").text,
        "localpath": root.find("localpath").text,
        "remotepath": root.find("remotepath").text,
        "command": root.find("command").text,
    }
    logger.add(f"./log/{root.tag}.log")
    logger.info("加载配置文件")
    return config
