import socket
import re
import typing
import os

import msgcodes as mc

IP_REGEX = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
MIN_PORT = 1024
MAX_PORT = 65535
SIGN_SEPARATE = '/*'

class Client:
    __ip = ""
    __port = -1
    __s = None
    __download_folder = "downloads"

    def __init__(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # PUBLIC METHODS
    def connection_active(self):
        """ Veic darbības, kamēr savienojums ir aktīvs. """
        print("Klients ir pieslēdzies adresei {}:{}.".format(self.__ip, self.__port))
        connection_is_active = True
        while connection_is_active:
            code = self.__input_command()
            self.__send_command(code)
            connection_is_active = self.__work_w_server(code)

    def connection_close(self):
        """ Pārtrauc savienojumu. """
        self.__close()

    def connection_start(self):
        """ Uzsāk savienojumu ar serveri. """
        try:
            self.__s.connect((self.__ip, self.__port))
        except Exception as e:
            print(e)
        else:
            self.connection_active()

    def initialize_client(self):
        """ Veic darbības, lai sagatavotu klientu pieslēgumam. """
        self.__input_host_address()

    def nonblocking_mode(self):
        """ Iestata serveri uz non-blocking režīmu. """
        self.__s.setblocking(False)

    # PRIVATE METHODS
    def __close(self):
        """ Aizver savienojumu. """
        self.__s.close()
        print("Savienojums ir aizvērts.")

    def __file_exists(self, filename: bytes) -> bool:
        """ Pārbauda, vai dotais fails eksistē """
        if os.path.exists(filename):
            return True
        return False

    def __file_exists_reply(self, reply: bytes):
        """ Pārbauda servera atbildi par faila eksistenci """
        if reply == self.__string_to_bytes(mc.FILE_EXISTS):
            return True
        return False

    def __file_list(self):
        """ Saņem un attēlo sarakstu ar pieejamiem failiem. """
        files_str = self.__s.recv(1024)
        file_list = files_str.decode().split(SIGN_SEPARATE)
        print("Uz servera atrodās sekojošie faili:")
        for file in file_list:
            print(file)
        return False

    def __file_receive(self) -> bool:
        """ Klients lejupielādē no servera pieprasīto failu. """
        user_input = str(input("Ievadiet faila nosaukumu, ko lejupielādēt: "))
        b_user_input = self.__string_to_bytes(user_input)
        self.__s.sendall(b_user_input)
        reply = self.__s.recv(1024)
        if self.__file_exists_reply(reply):
            print("Saņem failu...")
            filename = os.path.join(self.__download_folder, user_input)
            # TODO darbība, ja fails jau eksistē
            with open(filename, 'wb') as file:
                while True:
                    data = self.__s.recv(1024)
                    if not data:
                        break
                    file.write(data)
            print("Fails saņemts.")
        else:
            print("Fails neeksistē.")
        return False

    def __file_send(self) -> bool:
        """ Klients augšupielādē uz serveri failu. """
        input_given = False
        filename = ""
        while(input_given == False):
            try:
                filename = str(input("Ievadiet augšupielādējamā faila nosaukumu: "))
                if self.__file_exists(filename):
                    input_given = True
                else:
                    raise ValueError("Fails nav atrasts. Pārbaudiet ievadi un mēģiniet vēlreiz.")
            except Exception as e:
                print(e)
        self.__s.sendall(self.__string_to_bytes("{}:{}".format(mc.FILE_SEND, filename))) # todo no faila ceļa noņemt mapes
        print("Sūta failu...")
        file = open(filename, 'rb')
        data = file.read(1024)
        while data:
            self.__s.send(data)
            data = file.read(1024)
        print("Fails ir nosūtīts.")
        return False

    def __input_command(self) -> str:
        """ Klients ievada darbību, ko viņš vēlās veikt """
        actions = {
            "list": mc.LIST,
            "upload": mc.UPLOAD,
            "download": mc.DOWNLOAD
        }
        input_given = False
        user_input = ""
        while(input_given == False):
            try:
                user_input = str(input("Ievadiet veicamo darbību - list, upload vai download: ")).lower()
                if user_input in actions:
                    input_given = True
                else:
                    raise ValueError("Pārbaudiet ievadi un mēģiniet vēlreiz.")
            except Exception as e:
                print(e)
        return actions[user_input]

    def __input_host_address(self) -> tuple:
        """ Klients ievada servera adresi un portu, kurai viņš grib pieslēgties. """
        input_given = False
        ip = ""
        port = -1
        while(input_given == False):
            try:
                user_input = str(input("Ievadiet servera IP adresi un portu (sagaidāmais formāts - 127.0.0.1:1024) - "))
                ip, port = user_input.split(':')
                if self.__is_ip_good(ip) and self.__is_port_good(int(port)):
                    input_given = True
                else:
                    raise ValueError("Pārbaudiet ievadi un mēģiniet vēlreiz.")
            except Exception as e:
                print(e)
        self.__ip = ip
        self.__port = int(port)

    def __is_ip_good(self, ip) -> bool:
        """ Pārbauda, vai IP adrese ir derīga """
        if(re.search(IP_REGEX, ip)):
            return True
        return False

    def __is_port_good(self, port) -> bool:
        """ Pārbauda, vai ports ir derīgs """
        if port >= MIN_PORT and port <= MAX_PORT:
            return True
        return False

    def __send_command(self, code) -> bytes:
        """ Klients nosūta serverim izvēlēto komandu. """
        self.__s.sendall(str.encode(code))

    def __string_to_bytes(self, str_text: str) -> bytes:
        """ Konvertē str objektu uz bytes """
        bytes_text = str.encode(str_text)
        return bytes_text

    def __work_w_server(self, code: str) -> bool:
        actions = {
            mc.LIST: self.__file_list,
            mc.DOWNLOAD: self.__file_receive,
            mc.UPLOAD: self.__file_send
        }
        connection_is_active = actions[code]() # TODO iegūtā bool vērtība norādīs, vai klients grib turpināt darbu ar programmu.
        return connection_is_active

client = Client()
client.initialize_client()
client.connection_start()
client.connection_close()