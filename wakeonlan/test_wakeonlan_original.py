#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://kapibara-sos.net/archives/853

import socket
import struct
import time
 
def send_magic_packet(addr):
    # create socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # parse address
        mac_ = addr.upper().replace("-", "").replace(":", "")
        if len(mac_) != 12:
            raise Exception("invalid MAC address format: {}".format(addr))
        buf_ = b'f' * 12 + (mac_ * 20).encode()
        # encode to magic packet payload
        magicp = b''
        for i in range(0, len(buf_), 2):
            magicp += struct.pack('B', int(buf_[i:i + 2], 16))
 
        # send magic packet
        print("sending magic packet for: {}".format(addr))
        for i in range(5):
            s.sendto(magicp, ('<broadcast>', 7))
            s.sendto(magicp, ('<broadcast>', 9))
            time.sleep(1)



if __name__ == "__main__":

    # mac_addr = []
    mac_addr = "B0:83:FE:B7:A2:1F" #kon..-w10
    send_magic_packet(mac_addr)
    mac_addr = "40:A8:F0:B1:2B:2C" #kon..-vm10
    send_magic_packet(mac_addr)




