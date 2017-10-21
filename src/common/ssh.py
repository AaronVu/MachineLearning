# coding:utf-8
import paramiko


class SSHClient:

    def __init__(self, host, user, password, port=22):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.__instance = None

    def connect(self):
        self.__instance = paramiko.SSHClient()
        self.__instance.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__instance.connect(self.host, self.port, self.user, self.password)

    def disconnect(self):
        self.__instance.close()

    def exec(self, cmd):
        stdin, stdout, stderr = self.__instance.exec_command(cmd)
        err = stderr.readline()
        out = stdout.read()
        if err:
            return err
        else:
            return out

    def upload(self, localpath, remotepath):
        try:
            client = paramiko.Transport((self.ip,self.ip))
            client.connect(username=self.user, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(client)
            sftp.put(localpath, remotepath)
            client.close()
            print("OK.")
        except:
            print("Error!")

    def download(self, localpath, remotepath):
        try:
            client = paramiko.Transport((self.ip, self.ip))
            client.connect(username=self.user, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(client)
            sftp.get(remotepath, localpath)
            client.close()
            print("OK.")
        except:
            print ("Error!")

