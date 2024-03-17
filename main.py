import socket
import threading


def listen_for_messages():
    while True:
        data, address = sock.recvfrom(1024)
        print(f"Mesaj de la {address}, " + data.decode('utf-8'))


def send_messages(multicast_ip, port):
    print("Mesajul in canalul general trebuie sa inceapa cu m:<MESAJ>, iar pentru canal privat cu u:<MESAJ>@IP:PORT")
    while True:
        data = input("")
        try:
            if data.startswith("u:"):
                _, message_addr = data.split("u:", 1)
                message, addr = message_addr.split("@")
                ip, port_str = addr.split(":")
                port = int(port_str)
                sock.sendto(f"mesaj privat: {message}".encode('utf-8'), (ip, port))
            elif data.startswith("m:"):
                message_u = data[2:]
                sock.sendto(f"in canalul general: {message_u}".encode('utf-8'), (multicast_ip, port))
            else:
                print("Respecta formatul de mesaje")
        except Exception as e:
            print(f"Eroare la transmiterea datelor: {e}")


if __name__ == "__main__":
    multicast_ip = "224.0.0.1"
    port = 5008

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        #reutilizarea adresei pentru a asculta pe acelasi port
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', port))
        mreq = socket.inet_aton(multicast_ip) + socket.inet_aton("0.0.0.0")
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        threading.Thread(target=listen_for_messages).start()
        threading.Thread(target=send_messages, args=(multicast_ip, port)).start()
    except Exception as e:
        print(f"Nu s-a putut initializa socket-ul UDP: {e}")
