# TODO notestēt gadījumu, kad vairāki klienti ir reizē pieslēgušies

import os
import socket
import threading
import typing

import msgcodes as mc

IP_SELF = "127.0.0.1"
MIN_PORT = 1024
MAX_PORT = 65535
SIGN_SEPARATE = '/*'

class Server:
    """ Globāli klases mainīgie inicializēti ar sākuma vērtībām. """
    __file_dir = "files"
    __ip = ""
    __port = -1
    __s = None
       
    def __init__(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # PUBLIC METHODS
    def connection_active(self):
        """ Veic darbības, kamēr savienojums ir aktīvs. """
        connection_is_active = True
        while connection_is_active:
            conn, addr = self.__accept_connection()
            threading.Thread(target = self.__handle_client, args = (conn, addr )).start()

    def connection_close(self):
        """ Pārtrauc savienojumu. """
        self.__close()

    def connection_start(self):
        """ Uzsāk savienojumu ar internetu, gaida, kad kāds pieslēgsies. """
        self.__bind()
        self.__listen()

    def initialize_server(self):
        """ Veic darbības, kas sagatavo serveri palaišanai. """
        self.__select_port()
        self.__get_my_ip()
        
    def nonblocking_mode(self):
        """ Iestata serveri uz non-blocking režīmu. """
        self.__s.setblocking(False)

    def show_my_ip(self):
        """ Izdrukā uz ekrāna datora IP adresi un portu. """
        print("Šī servera IP adrese ir: {}:{}".format(self.__ip, self.__port))

# PRIVATE METHODS
    def __accept_connection(self) -> tuple:
        """ Akceptē ienākošos savienojumus """
        conn, addr = self.__s.accept()
        print("Serverim ir pieslēdzies klients {}".format(addr))
        return conn, addr

    def __bind(self):
        """ Piesaista IP adresi un portu 'Socket' objektam. """
        try:
            if self.__is_port_good(self.__port):
                self.__s.bind((IP_SELF, self.__port))
            else:
                raise ValueError("Nevar piesaistīt adresi 'Socket' objektam, porta numuram ir jābūt starp {} un {}.".format(MIN_PORT, MAX_PORT))
        except Exception as e:
            print(e)

    def __close(self):
        """ Aizver savienojumu. """
        self.__s.close()
        print("Savienojums ir aizvērts.")

    def __close_connection_w_client(self, conn, addr):
        """ Aizver savienojumu ar klientu. """
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        print("Savienojums ar {} tika aizvērts.".format(addr))

    def __file_exists(self, filename: bytes) -> bool:
        """ Pārbauda, vai dotais fails eksistē """
        if os.path.exists(filename):
            return True
        return False

    def __file_list(self, conn):
        """ Serveris attēlo klientam sarakstu ar pieejamajiem failiem.
        Lai atdalītu failu nosaukumus, tiek izmantots '/*' kā apzīmējums. """
        file_list = os.listdir(self.__file_dir)
        str_filenames = SIGN_SEPARATE.join(file_list)
        msg = self.__string_to_bytes(str_filenames)
        conn.sendall(msg)
        # TODO lietotājs tālāk var izlemt, vai lejupielādēt kādu no failiem, vai beigt darbu.

    def __file_message(self, msg: bytes) -> bool: # TODO test
        split_msg = msg.decode().split(":")
        if split_msg[0] == mc.FILE_SEND and len(split_msg) == 2:
            return True
        return False

    def __file_receive(self, conn):
        """ Serveris saņem no klienta failu. """
        msg = conn.recv(1024)
        try:
            if self.__file_message(msg):
                filename = msg.decode().split(":")[1]
                file_path = os.path.join(self.__file_dir, filename)
                with open(file_path, 'wb') as file:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        file.write(data)
            else:
                raise ValueError("Tika saņemts {} FILE_SEND vietā".format(msg.decode())) # TODO bytes like object required not str
        except Exception as e:
            print(e)

    def __file_send(self, conn):
        """ Serveris nosūta klientam pieprasīto failu. """
        filename = conn.recv(1024)
        file_path = os.path.join(self.__file_dir, filename.decode())
        if self.__file_exists(file_path):
            conn.sendall(self.__string_to_bytes(mc.FILE_EXISTS))
            if self.__is_msg_nonempty(filename):
                file = open(file_path, 'rb')
                data = file.read(1024)
                while data:
                    conn.send(data)
                    data = file.read(1024)
        else:
            conn.sendall(self.__string_to_bytes(mc.FILE_NOT_EXIST))

    def __get_my_ip(self) -> str:
        """ Iestata mainīgā __ip vērtību uz datora IP adresi. """
        ip = socket.gethostbyname(socket.gethostname())
        self.__ip = ip

    def __handle_client(self, conn, addr):
        """ Apkalpo klientu """
        actions = {
            mc.LIST: self.__file_list,
            mc.DOWNLOAD: self.__file_send,
            mc.UPLOAD: self.__file_receive
            }
        command = conn.recv(1024)
        str_command = command.decode()
        actions[str_command](conn)
        self.__close_connection_w_client(conn, addr)

    def __is_msg_nonempty(self, message) -> bool:
        """ Pārbauda, vai simbolu virkne ir tukša """
        if message != "" or message != b"":
            return True
        return False

    def __is_port_good(self, port) -> bool:
        """ Pārbauda, vai ports ir derīgs """
        if port >= MIN_PORT and port <= MAX_PORT:
            return True
        return False

    def __listen(self):
        """ Klausās ienākošos savienojumus. """
        print("Gaida ienākošus savienojumus...")
        self.__s.listen()

    def __select_port(self) -> int:
        """ Iestata servera portu. """
        port_selected = False
        port = -1
        while(port_selected == False):
            try:
                port = int(input("Ievadiet portu, ko izmantos serveris: "))
                if self.__is_port_good(port):
                    port_selected = True
                else:
                    raise ValueError("Izvēlieties porta numuru starp {} un {}.".format(MIN_PORT, MAX_PORT))
            except Exception as e:
                print(e)
        self.__port = port

    def __string_to_bytes(self, str_text: str) -> bytes:
        """ Konvertē str objektu uz bytes """
        bytes_text = str.encode(str_text)
        return bytes_text

server = Server()

server.initialize_server()
server.show_my_ip()
server.connection_start()
server.connection_active()
server.connection_close()