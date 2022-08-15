import socket
import struct


def ip_to_int(ip):
    return struct.unpack('!I', socket.inet_aton(ip))[0]


def int_to_ip(int_ip):
    return socket.inet_ntoa(struct.pack('!I', int_ip))
