import paramiko
import socket
from getpass import (getuser, getpass)

class switches():

    def __init__(self, ip, user, password):
        self.user=user
        self.password=password
        self.ip=ip
        self.remote = paramiko.SSHClient()
        #self.remote.set_missing_key_policy(paramiko.AutoAddPolicy())
        self.remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def pull_run(self):
        self.remote.connect(hostname=self.ip, port=22, username=self.user, password=self.password, timeout=10)
        self.stdin, self.stdout, self.stderr = self.remote.exec_command('sh run')


    def save_run(self):
        file = open(self.ip + ' sh_route.txt', 'a')
        file.write(''.join(self.stdout))
        file.close()

    def switch_close(self):
        self.remote.close()

    def ip_id(self):
        return self.ip

def main():

    user = input("Enter Username: ")
    password = getpass('Enter Password: ')
    ips=[]
    with open('IP-List.txt', 'r') as ip_list:
        ipaddr = ip_list.readlines()
        for line in ipaddr:
            ips.insert(0,switches(line,user,password))
    for i in range (0,len(ips)):
        try:
            ips[i].pull_run()
            ips[i].save_run()
            ips[i].switch_close()
            print("Connection to %s successful." % ips[i].ip_id())
        except socket.gaierror:
            print('Could not connect to %s \n' % ips[i].ip_id())
            # continue
        except paramiko.AuthenticationException:
            print('Could not authenticate to %s \n' % ips[i].ip_id())
            # continue
        except socket.error:
            print('Connection Timed out: %s \n' % ips[i].ip_id())
            # continue
        except paramiko.SSHException:
            print('Incompatible ssh peer: %s \n' % ips[i].ip_id())
            # continue
        except Exception:
            print("Unexpected error")

if __name__ == '__main__':
    main()
