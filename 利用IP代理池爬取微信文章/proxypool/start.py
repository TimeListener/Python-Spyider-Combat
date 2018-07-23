
from proxypool.checkout import CheckIp

if __name__=='__main__':
    check = CheckIp()
    vaild_list = check.return_vaild_ip()
    for i in range(0,len(vaild_list)):
        print('可用IP：',vaild_list[i])