#!/usr/bin/python
import socket

s = socket.socket()

s.connect(('192.168.20.55', 3389))

s.send('quit')

print 'asdf'
