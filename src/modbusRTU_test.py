# %%
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient

# import serial
# import modbus_tk
# import modbus_tk.defines as cst
# from modbus_tk import modbus_rtu

import numpy as np
import os

BATH_PATH = os.path.dirname(os.path.abspath(__file__))
ETC_PATH = os.path.join(BATH_PATH, "..", "etc")
DATA_PATH = os.path.join(BATH_PATH, "..", "data")


Baudrate, Parity, Bytesize, Stopbits = int(9600), str("N"), int(8), int(1)
# address = int(40001) # Extract Point Address from selected point dataset
# sid = 11
# offset = 40001

# client = ModbusSerialClient(method="rtu", port="/dev/ttyS0", baudrate=Baudrate, parity=Parity, bytesize=Bytesize, stopbits=Stopbits, timeout=0.2) 
# connection = client.connect()
# print(F"connection: {connection}")

# raws = client.read_holding_registers(address - offset, count=2, unit=sid, timeout=0.1) # 40001~49999 as read_holding_registers
# raws = np.asarray(raws.registers[0:2], dtype=np.uint16) if not raws.isError() else None
# print(F"raws : {raws}")

# client.close()

# %%
Baudrate, Parity, Bytesize, Stopbits = int(2400), str("E"), int(8), int(1)
address = int(40015) # Extract Point Address from selected point dataset
sid = 1
offset = 40001

client2 = ModbusSerialClient(method="RTU", port="COM3", baudrate=Baudrate, parity=Parity, bytesize=Bytesize, stopbits=Stopbits, timeout=0.2) 
connection2 = client2.connect()
print(F"connection: {connection2}")

raws = client2.read_holding_registers(address - offset, count=2, unit=sid, timeout=0.1) # 40001~49999 as read_holding_registers
print(F"raws_1 : {raws}")
raws = np.asarray(raws.registers[0:2], dtype=np.uint16) if not raws.isError() else None
print(F"raws_2 : {raws}")

client2.close()


# %%
Baudrate, Parity, Bytesize, Stopbits = int(2400), str("E"), int(8), int(1)
address = int(40017) # Extract Point Address from selected point dataset
sid = 2
offset = 40001

# client = ModbusSerialClient(method="rtu", port="/dev/ttyS0", baudrate=Baudrate, parity=Parity, bytesize=Bytesize, stopbits=Stopbits, timeout=0.2) 
# connection = client.connect()
# print(F"connection: {connection}")

raws = client2.read_holding_registers(address - offset, count=2, unit=sid, timeout=0.1) # 40001~49999 as read_holding_registers
print(F"raws_1 : {raws}")
raws = np.asarray(raws.registers[0:2], dtype=np.uint16) if not raws.isError() else None
print(F"raws_2 : {raws}")

client2.close()


# %%
# Baudrate, Parity, Bytesize, Stopbits = int(19200), str("N"), int(8), int(1)
# address = int(31047) # Extract Point Address from selected point dataset
# sid = 3
# offset = 30001

# client = ModbusSerialClient(method="rtu", port="/dev/ttyS0", baudrate=Baudrate, parity=Parity, bytesize=Bytesize, stopbits=Stopbits, timeout=0.2) 
# connection = client.connect()
# print(F"connection: {connection}")

# raws = client.read_input_registers(address - offset, count=2, unit=sid, timeout=0.1) # 40001~49999 as read_holding_registers
# print(F"raws_1 : {raws}")
# raws = np.asarray(raws.registers[0:2], dtype=np.uint16) if not raws.isError() else None
# print(F"raws_2 : {raws}")

# client.close()