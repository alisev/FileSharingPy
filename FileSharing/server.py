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

class Server:
    def __init__(self):
        pass
    def bind():
        pass
    def connection_close():
        pass
    def connection_start():
        pass
    def listen():
        pass
    def send_confirmation():
        pass
    def show_my_ip():
        pass

server = Server()