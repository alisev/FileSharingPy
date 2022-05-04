# Pirmais solis:
# pieslēdzas Ip adresei
# norāda paroli, ja nepieciešams
# pieslēdzas
# sagaida apstirpinājumu
# slēdz savienojumu

import socket
import re
import typing

import threading
import os


MIN_PORT = 1024
MAX_PORT = 65535
IP_REGEX = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

class Client:
    __ip = ""
    __port = -1
    __s = None

    def __init__(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.initialize_client()
        self.connection_start()
        self.connection_close()

    # PUBLIC METHODS
    def connection_active(self):
        """ Veic darbības, kamēr savienojums ir aktīvs. """
        print("Klients ir pieslēdzies adresei {}:{}.".format(self.__ip, self.__host))
        self.test_echo_send()

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

    # METODES TESTĒŠANAI
    def test_echo_send(self):
        """ Atbalss tests. """
        self.__s.sendall(b"Hello, world!")
        data = self.__s.recv(1024)
        print(data)

    # PRIVATE METHODS
    def __close(self):
        """ Aizver savienojumu. """
        self.__s.close()
        print("Savienojums ir aizvērts.")

    def __input_host_address(self):
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

    def __is_ip_good(self, ip):
        """ Pārbauda, vai IP adrese ir derīga """
        if(re.search(IP_REGEX, ip)):
            return True
        return False

    def __is_port_good(self, port):
        """ Pārbauda, vai ports ir derīgs """
        if port >= MIN_PORT and port <= MAX_PORT:
            return True
        return False

client = Client()