import serial
import time

import serial.serialutil


class InspireHandAPI:
    ser: serial.Serial
    port: int
    baudrate: int
    id: int

    regdict = {
        'ID' : 1000,
        'baudrate' : 1001,
        'clearErr' : 1004,
        'forceClb' : 1009,
        'angleSet' : 1486,
        'forceSet' : 1498,
        'speedSet' : 1522,
        'angleAct' : 1546,
        'forceAct' : 1582,
        'errCode' : 1606,
        'statusCode' : 1612,
        'temp' : 1618,
        'actionSeq' : 2320,
        'actionRun' : 2322
    }

    def _openSerial(self, port, baudrate):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = 1
        self.ser.write_timeout = 1
        
        self.ser.open()
        print('Serial port opened successfully!')

    
    def __init__(self, port, baudrate, id):
        self.port = port
        self.baudrate = baudrate
        self.id = id
    
        self._openSerial(port, baudrate)
        

    def _writeRegister(self, id, add, num, val):
        byteList = [0xEB, 0x90]

        # id
        byteList.append(id)
        # len
        byteList.append(num + 3)
        # cmd
        byteList.append(0x12)
        # add
        byteList.append(add & 0xFF)
        byteList.append((add >> 8) & 0xFF)

        for i in range(num):
            byteList.append(val[i])
        
        checksum = 0x00
        for i in range(2, len(byteList)):
            checksum += byteList[i]
        checksum &= 0xFF
        byteList.append(checksum)

        self.ser.write(bytes(byteList))

        time.sleep(0.01)
        self.ser.read_all()

    
    def _readRegister(self, id, add, num, mute=False):
        bytes = [0xEB, 0x90]
        bytes.append(id) # id
        bytes.append(0x04) # len
        bytes.append(0x11) # cmd
        bytes.append(add & 0xFF)
        bytes.append((add >> 8) & 0xFF) # add
        bytes.append(num)
        checksum = 0x00
        for i in range(2, len(bytes)):
            checksum += bytes[i]
        checksum &= 0xFF
        bytes.append(checksum)

        print('Sent bytes: ', end='')
        for byte in bytes:
            print(f'{byte:02X};', end='')
        print()

        self.ser.write(bytes)
        time.sleep(0.01)
        recv = self.ser.read_all()
        if len(recv) == 0:
            return []
        num = (recv[3] & 0xFF) - 3
        val = []
        for i in range(num):
            val.append(recv[7 + i])
        if not mute:
            print('Read register values: ', end='')
            for i in range(num):
                print(val[i], end=' ')
            print()
        return val

    def write6(self, id, str, val):
        if str == 'angleSet' or str == 'forceSet' or str == 'speedSet':
            val_reg = []
            for i in range(6):
                val_reg.append(val[i] & 0xFF)
                val_reg.append((val[i] >> 8) & 0xFF)
            self._writeRegister(id, self.regdict[str], 12, val_reg)
        else:
            print("Function call error, correct usage: str should be 'angleSet'/'forceSet'/'speedSet', val should be a list of length 6 with values 0~1000, -1 can be used as a placeholder")

    def read6(self, id, str):
        val_act = []

        if str == 'angleSet' or str == 'forceSet' or str == 'speedSet' or str == 'angleAct' or str == 'forceAct':
            val = self._readRegister(id, self.regdict[str], 12, True)
            if len(val) < 12:
                print('No data read')
                return
            for i in range(6):
                val_act.append((val[2*i] & 0xFF) + (val[1 + 2*i] << 8))
            print('Read values: ', end='')
            for i in range(6):
                print(val_act[i], end=' ')
            print()
        elif str == 'errCode' or str == 'statusCode' or str == 'temp':
            val_act = self._readRegister(id, self.regdict[str], 6, True)
            if len(val_act) < 6:
                print('No data read')
                return
            print('Read values: ', end='')
            for i in range(6):
                print(val_act[i], end=' ')
            print()
        else:
            print("Function call error, correct usage: str should be 'angleSet'/'forceSet'/'speedSet'/'angleAct'/'forceAct'/'errCode'/'statusCode'/'temp'")

        return val_act


def main():
    print('Opening serial port!')
    # Change to your own serial port and baud rate, default baud rate is 115200
    hand = InspireHandAPI('/dev/ttyUSB0', 115200)
    print('Setting hand movement speed parameters, -1 means do not set this speed!')

    hand.write6(1, 'speedSet', [100, 100, 100, 100, 100, 100])
    time.sleep(2)
    print('Setting hand grip force parameters!')
    hand.write6(1, 'forceSet', [500, 500, 500, 500, 500, 500])
    time.sleep(1)
    print('Setting hand movement angle parameters to 0, -1 means do not set this angle!')
    hand.write6(1, 'angleSet', [0, 0, 0, 0, 400, -1])
    time.sleep(3)
    hand.read6(1, 'angleAct')
    time.sleep(1)
    print('Setting hand movement angle parameters to 1000, -1 means do not set this angle!')
    hand.write6(1, 'angleSet', [1000, 1000, 1000, 1000, 400, -1])
    time.sleep(3)
    hand.read6(1, 'angleAct')
    time.sleep(1)
    hand.read6(1, 'errCode')
    time.sleep(1)
    print('Setting hand action sequence: 8!')
    hand._writeRegister(1, hand.regdict['actionSeq'], 1, [8])
    time.sleep(1)
    print('Running current hand action sequence!')
    hand._writeRegister(1, hand.regdict['actionRun'], 1, [1])
    # writeRegister(ser, 1, regdict['forceClb'], 1, [1])
    # time.sleep(10) # Since force calibration takes a long time, do not skip this sleep and try to re-communicate with the hand, it may cause the plugin to crash


if __name__ == '__main__':
    main()