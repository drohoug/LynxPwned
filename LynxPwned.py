import argparse
import socket
import threading
import pyfiglet
from datetime import datetime
from termcolor import colored
 
t1 = datetime.now()


def banner():
    print(100 * "_")
    print(pyfiglet.figlet_format("L Y N X", font="ticksslant", justify="center"))
    print("   LynxPwned - Port Scanner | Created by Pedro 'drohoug' Henrique")
    print(100 * "_")



def check_host(host):
    try:
        target = socket.gethostbyname(host)
    except socket.gaierror:
        print(colored("[!] Invalid hostname or IP address.", "red"))
        exit()
    return target


def check_ports(ports):
    max_port = 65535
    if any(port > max_port for port in ports):
        print(colored(f"[!] Invalid port number (maximum is {max_port}).", "red"))
        exit()


def port_scan(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        result = s.connect_ex((host, port))
        if result == 0:
            print(colored(f"[*] {host}:{port}  Open ", "green"))


def main():
    colored(f'{banner()}', "green")
    parser = argparse.ArgumentParser(description="Simple Port Scanner in python")
    parser.add_argument("host", type=str, help="Target host to scan")
    parser.add_argument("-p", "--ports", type=int, nargs="+",
                        default=[
                            0, 3, 7, 20, 21, 22, 23, 25, 53, 69, 80, 88, 102, 110, 135, 137, 139, 143, 161, 381,
                            383, 389, 443, 464, 465, 587, 593, 636, 691, 902, 990, 993, 995, 1025, 1194, 1337,
                            1433, 1521, 1589, 1725, 2049, 2077, 2082, 2083, 2086, 2096, 2483, 2484, 2967, 3074,
                            3306, 3724, 4664, 5432, 5632, 5900, 6665, 6669, 6881, 6999,
                            6970, 8086, 8087, 8222, 9100, 10000, 12345, 27374, 18006, 8080
                                ],
                        help="Target ports to scan (separated by spaces).")
    parser.add_argument("-t", "--threads", type=int, default=5,
                        help="Number of threads to use. Default is 5.")
    args = parser.parse_args()
    host = args.host
    ports = args.ports

    ip = check_host(host)
    check_ports(ports)

    threads_list = []
    for port in ports:
        t = threading.Thread(target=port_scan, args=(ip, port))
        threads_list.append(t)
        t.start()
    for t in threads_list:
        t.join()


if __name__ == "__main__":
    main()


# End time
t2 = datetime.now()
total = str(t2 - t1)
print(colored(f"Scanning Completed in: {total}", "cyan"))
