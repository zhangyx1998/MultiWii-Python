# ===================================================================
# Application Demo
# ===================================================================
# Author: Yuxuan Zhang, yuxuan@yuxuanzhang.net
# Published under MIT License
# ===================================================================
from time import sleep
from lib import MultiWii, MSP

fc = MultiWii("/dev/ttyACM0")

print(fc.invoke(MSP.RAW_IMU()))
print(fc.invoke(MSP.RC()))
print(fc.invoke(MSP.MOTOR()))
fc.invoke(MSP.SET_MOTOR(1450, 1550, 1450, 1550))
print(fc.invoke(MSP.MOTOR()))
sleep(1)
fc.invoke(MSP.SET_MOTOR(1500, 1500, 1500, 1500))
print(fc.invoke(MSP.MOTOR()))
