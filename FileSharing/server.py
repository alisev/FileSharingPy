# Pie tam servera programmai ir jāspēj vienlaicīgi apkalpot vairākus klientus (multi threading)
# starp klientiem ir janotiek kaut kādai mijiedarbibai
# (respektīvi, lai identisku funkcionalitāti nevarētu panākt piestartējot pilngi neatkarīgu serveri katram klientam). 

# atver komandlodziņu
# parāda lietotājam sava servera IP adresi
# lūdz norādīt paroli ?
# ip adresi (un paroli) lietotājs nosūta adresātam/-iem

# adresāts 'var saņemt failu, kamēr abi ir tiešsaistē un programma ir atvērta
# klienti var pārsūtīt failusvienam otram - augšupielādēt un lejupielādēt
# pēc augušupielādes lietotājam parāda saiti, ko var nodot citam klientam

import socket
import threading
import os
import typing

# Pirmais solis:
# Inicializē serveri
# Parāda lietotājam savu IP adresi
# Bind
# Listen
# Nosūta apstiprinājuma paziņojumu klientam
# Slēdz savienojumu

MIN_PORT = 1024
MAX_PORT = 65535

class Server:
    """ Klases mainīgie inicializēti ar sākuma vērtībām. """
    __ip = ""
    __port = -1
    __s = None

    def __init__(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # PUBLIC METHODS
    def connection_close(self):
        self.__close()

    def connection_start(self):
        self.__bind()
        self.__listen()

    def initialize_server(self):
        """ Veic darbības, kas sagatavo serveri palaišanai. """
        self.__select_port()
        self.__get_my_ip()
        self.show_my_ip()

    def send_confirmation(self):
        pass

    def show_my_ip(self):
        """ Izdrukā uz ekrāna datora IP adresi un portu. """
        print("Šī servera IP adrese ir: {}:{}".format(self.__ip, self.__port))

    def test_echo_receive(self):
        pass

    # PRIVATE METHODS
    def __bind(self):
        """ Piesaista IP adresi un portu 'Socket' objektam. """
        try:
            if self.__is_port_good(self.__port):
                self.__s.bind((self.__ip, self.__port))
            else:
                raise ValueError("Nevar piesaistīt adresi 'Socket' objektam, porta numuram ir jābūt starp {} un {}.".format(MIN_PORT, MAX_PORT))
        except Exception as e:
            print(e)

    def __close(self):
        self.__s.close()
        print("Savienojums ir aizvērts.")

    def __get_my_ip(self) -> str:
        """ Iestata mainīgā __ip vērtību uz datora IP adresi. """
        ip = socket.gethostbyname(socket.gethostname())
        self.__ip = ip

    def __is_port_good(self, port):
        """ Pārbauda, vai ports ir derīgs """
        if port >= MIN_PORT and port <= MAX_PORT:
            return True
        return False

    def __listen(self):
        """ Klausās ienākošos savienojumus """
        self.__s.listen()
        print("Gaida ienākošus savienojumus...")

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

server = Server()
server.initialize_server()
server.connection_start()
server.connection_close()