import time
import struct
import sys
import socket
import pigpio
import threading

if sys.version > '3':
    buffer = memoryview

BUS = 1
ADXL345_I2C_ADDR = 0x53


class accelPI(threading.Thread):  # отслеживает ускорение по каждой оси и передает на диод
    def __init__(self, pin, value=200, iter=2000):
        self.pin = pin
        self.iter = iter
        self.value = value
        self.s = 0
        self.b = 0
        self.h = 0
        self.pi = 0
        self.x = 0
        self.y = 0
        self.z = 0
        threading.Thread.__init__(self)

    def run(self):
        self.pi = pigpio.pi('::1')
        self.h = self.pi.i2c_open(BUS, ADXL345_I2C_ADDR)
        if self.h >= 0:  # Connected OK?

            # Initialise ADXL345.
            self.pi.i2c_write_byte_data(self.h, 0x2d, 0)  # POWER_CTL reset.
            self.pi.i2c_write_byte_data(self.h, 0x2d, 8)  # POWER_CTL measure.
            self.pi.i2c_write_byte_data(self.h, 0x31, 0)  # DATA_FORMAT reset.
            self.pi.i2c_write_byte_data(self.h, 0x31, 11)  # DATA_FORMAT full res +/- 16g.
            while self.iter > 0:
                (self.s, self.b) = self.pi.i2c_read_i2c_block_data(self.h, 0x32, 6)
                if self.s >= 0:
                    (self.x, self.y, self.z) = struct.unpack('<3h', buffer(self.b))
                    # print("{} {} {}".format(self.x, self.y, self.z))
                    if 1 <= abs(self.x) <= 255:
                        self.value = abs(self.x)

                self.pi.set_PWM_dutycycle(self.pin, self.value)
                time.sleep(0.005)
                self.iter = self.iter - 1

        self.pi.i2c_close(self.h)
        self.pi.stop()


class accelRead(threading.Thread):  # читает показания акселерометра и передает на desktop
    def __init__(self, RUNTIME=10.0):
        threading.Thread.__init__(self)
        self.b = 0
        self.h = 0
        self.s = 0
        self.pi = 0
        self.messenger = 0
        self.RUNTIME = RUNTIME
        self.start_time = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.message = ''
        self.port = 6006

    def run(self):
        self.messenger = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.messenger.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.pi = pigpio.pi('::1')
        self.h = self.pi.i2c_open(BUS, ADXL345_I2C_ADDR)
        if self.h >= 0:  # Connected OK?

            # Initialise ADXL345.
            self.pi.i2c_write_byte_data(self.h, 0x2d, 0)  # POWER_CTL reset.
            self.pi.i2c_write_byte_data(self.h, 0x2d, 8)  # POWER_CTL measure.
            self.pi.i2c_write_byte_data(self.h, 0x31, 0)  # DATA_FORMAT reset.
            self.pi.i2c_write_byte_data(self.h, 0x31, 11)  # DATA_FORMAT full res +/- 16g.
            self.start_time = time.time()
            while (time.time() - self.start_time) < self.RUNTIME:
                (self.s, self.b) = self.pi.i2c_read_i2c_block_data(self.h, 0x32, 6)
                if self.s >= 0:
                    (self.x, self.y, self.z) = struct.unpack('<3h', buffer(self.b))
                    self.message = "{} {} {}".format(self.x, self.y, self.z)
                    self.messenger.sendto(bytes(self.message, encoding='utf-8'), ('192.168.0.4', self.port))
                time.sleep(1)
            self.pi.i2c_close(self.h)
            self.pi.stop()
            self.messenger.close()


class setColor(threading.Thread):  # устанавливает цвет диода из полученного значения
    def __init__(self, pin, value, iter=2000):
        self.pin = pin
        self.pi = pigpio.pi('::1')
        self.value = value
        self.iter = iter
        threading.Thread.__init__(self)

    def run(self):
        while self.iter > 0:
            self.pi.set_PWM_dutycycle(self.pin, self.value)
            self.iter = self.iter - 1
            time.sleep(0.005)


class listener(threading.Thread):
    def __init__(self, RUNTIME=30.0):
        self.messenger = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        threading.Thread.__init__(self)
        self.RUNTIME = RUNTIME
        self.start_time = 0
        self.result = ''
        self.p17 = 0
        self.p27 = 0
        self.p22 = 0
        self.data = []
        self.buffer = ''
        self.port = 6007

    def run(self):

        self.messenger.bind(('', self.port))
        self.messenger.settimeout(1)
        self.start_time = time.time()
        while (time.time() - self.start_time) < self.RUNTIME:
            try:
                self.result = str(self.messenger.recv(1024), encoding='utf-8')
            except:
                print('ждем команды')
            time.sleep(1)
            if self.result != '':
                break

        if self.result == 'ax':
            print('включаем акселерометр-диод')
            self.p17 = accelPI(17)
            self.p27 = accelPI(27)
            self.p22 = accelPI(22)
            self.p17.start()
            self.p27.start()
            self.p22.start()
        elif self.result == '':
            pass
        else:
            print('устанавливаем цвет')
            print(self.result)
            for self.i in self.result:
                if self.i == ' ':
                    self.data.append(int(self.buffer))
                    self.buffer = ''
                if self.i != ' ':
                    self.buffer = self.buffer + self.i

            self.p17 = setColor(17, self.data[0])
            self.p22 = setColor(27, self.data[1])
            self.p27 = setColor(22, self.data[2])
            self.p22.start()
            self.p27.start()
            self.p17.start()
        self.messenger.close()


a = accelRead()
a.start()
lis = listener()
lis.start()
