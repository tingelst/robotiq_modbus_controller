import numpy as np
from pymodbus.client.sync import ModbusSerialClient
from registers import Request


class ModbusRtuDriver:

    UNIT: int = 9

    def __init__(self, device) -> None:
        self._client = ModbusSerialClient(
            method="rtu",
            port=device,
            stopbits=1,
            bytesize=8,
            baudrate=115200,
            timeout=0.2,
        )

    def reset(self):
        request = Request()
        self._client.write_registers(1000, request.registers(), unit=self.UNIT)

    def activate(self):
        request = Request()
        request.action.act = True
        self._client.write_registers(1000, request.registers(), unit=self.UNIT)

    def move(self, *, pos: np.uint8, speed: np.uint8, force: np.uint8):
        request = Request()
        request.action.act = True
        request.action.gto = True
        request.position.pr = pos
        request.speed.sp = speed
        request.force.fr = force
        self._client.write_registers(1000, request.registers(), unit=self.UNIT)


if __name__ == "__main__":
    device = "/dev/ttyUSB2"
    driver = ModbusRtuDriver(device)

    driver.reset()
    driver.activate()
