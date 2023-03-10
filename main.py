from lib.tools import *
import paramiko
import sys


def main():
    config = getXMLConfig(sys.argv[1])
    client = connectHost(config)
    local_path = compressZip(config['localpath'])
    remote_path = config['remotepath']
    try:
        sftp = paramiko.SFTPClient.from_transport(client.get_transport())
        sftp.put(local_path, remote_path, callback=call_back)
        logger.info(f"文件上传成功 {config['remotepath']}"+(" " * 50))
        stdin, stdout, stderr = client.exec_command(config['command'])
        while not stdout.channel.exit_status_ready():
            res = stdout.readline()[:-3]
            print("\r{}".format(res), end="")
            if stdout.channel.exit_status_ready():
                print("", end="\r")

    except paramiko.ssh_exception.SSHException:
        logger.error("强制断开连接")
        client.close()

    logger.info(f"命令执行成功 {config['command']}")
    client.close()
    pass


if __name__ == '__main__':
    main()
