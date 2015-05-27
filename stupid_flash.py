#!/usr/bin/env python

from serial import *
from threading import Thread
import time
import re

def flashing(ser):
	time.sleep(1)
	print "=> setenv ipaddr 192.168.1.3 && setenv serverip 192.168.1.23 && saveenv"
	ser.write("setenv ipaddr 192.168.1.3 && setenv serverip 192.168.1.23 && saveenv")
	ser.write('\n')
	time.sleep(1)
	print "=> tftp 0x80060000 openwrt-ar71xx-generic-cus531-nand-rootfs-squashfs.bin"
	ser.write("tftp 0x80060000 openwrt-ar71xx-generic-cus531-nand-rootfs-squashfs.bin")
	ser.write('\n')
	time.sleep(15)
	print "=> nand erase 0x200000 0x1400000 && nand write $fileaddr 0x200000 $filesize"
	ser.write("nand erase 0x200000 0x1400000 && nand write $fileaddr 0x200000 $filesize")
	ser.write('\n')
	time.sleep(10)
	print "=> tftp 0x80060000 openwrt-ar71xx-generic-cus531-nand-kernel.bin"
	ser.write("tftp 0x80060000 openwrt-ar71xx-generic-cus531-nand-kernel.bin")
	ser.write('\n')
	time.sleep(5)
	print "=> nand erase 0x0 0x200000 && nand write $fileaddr 0x0 $filesize"
	ser.write("nand erase 0x0 0x200000 && nand write $fileaddr 0x0 $filesize")
	ser.write('\n')
	time.sleep(5)

def receiving(ser):
	start = re.compile("Hit any key to stop autoboot")
	p = re.compile("OK")
	buffer = ''
	while True:
		buffer = ser.readline()
		if p.match(buffer):
			print "==> %s " % buffer

		if start.match(buffer):
			ser.write('a')
			Thread(target=flashing, args=(ser,)).start()
		'''
		if stop.match(buffer):
			print "[FLASH] upgrade ok"
			break
		'''

		
if __name__ ==  '__main__':
	ser = Serial(
		port="/dev/ttyUSB0",
		baudrate=115200,
		bytesize=EIGHTBITS,
		parity=PARITY_NONE,
		stopbits=STOPBITS_ONE,
		timeout=0.1,
		xonxoff=0,
		rtscts=0,
		interCharTimeout=None
	)

	print "[FLASH] start"
	Thread(target=receiving, args=(ser,)).start()

