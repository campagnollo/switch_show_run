import paramiko
import time
import socket
from getpass import (getuser, getpass)

"""Function to start SSH process"""
def ssh_prime():
    remote = paramiko.SSHClient()
    remote.set_missing_key_policy(paramiko.AutoAddPolicy())
    return remote

"""Function to access a switch and pull 'show run' data"""
def call_switch(ip, Username, Password, remote_conn_pre):
    remote_conn_pre.connect(hostname=ip, port=22, username=Username, password=Password)
    time.sleep(2)
    print('Processing record Successfully Connected to %s' % ip)
    stdin, stdout, stderr = remote_conn_pre.exec_command('sh run')
    return stdout.readlines()

"""Function to save run data to a independent file"""
def run_save(ip, output):
    file = open(ip + ' sh_route.txt', 'a')
    file.write(''.join(output))
    file.close()

def main():

    Username = input('Enter Username: ')
    Password = getpass('Enter Password: ')

    """Open file of switch IPs and save to a list"""
    with open('IP-List.txt', 'r') as ip_list:
        ipaddr = ip_list.readlines()
        ipaddr = [line[:-1]for line in ipaddr]

    for ip in ipaddr:
        remote_conn_pre = ssh_prime()
        try:
            output=call_switch(ip, Username, Password, remote_conn_pre)
        except socket.gaierror:
            print('Could not connect to %s \n' % ip)
            # continue
        except paramiko.AuthenticationException:
            print('Could not authenticate to %s \n' % ip)
            # continue
        except socket.error:
            print('Connection Timed out: %s \n' % ip)
            # continue
        except paramiko.SSHException:
            print('Incompatible ssh peer: %s \n' % ip)
            # continue
        else:
            run_save(ip, output)
        finally: """closing SSH connection gracefully"""
            remote_conn_pre.close()


if __name__ == '__main__':
    main()