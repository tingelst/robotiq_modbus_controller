import numpy as np
from pymodbus.client.sync import ModbusSerialClient
from request import Request
from status import Status


class ModbusRtuDriver:

    UNIT: int = 9
    INPUT_REGISTER: int = 1000
    OUTPUT_REGISTER: int = 2000
    NUM_REGISTERS: int = 3

    def __init__(self, device) -> None:
        self._client = ModbusSerialClient(
            method="rtu",
            port=device,
            stopbits=1,
            bytesize=8,
            baudrate=115200,
            timeout=0.2,
        )

    def connect(self):
        return self._client.connect()

    def disconnect(self):
        self._client.close()

    def reset(self):
        request: Request = Request()
        self._client.write_registers(
            self.INPUT_REGISTER, request.registers(), unit=self.UNIT
        )

    def activate(self):
        request: Request = Request()
        request.action_request.act = True
        self._client.write_registers(
            self.INPUT_REGISTER, request.registers(), unit=self.UNIT
        )

    def move(self, *, pos: np.uint8, speed: np.uint8, force: np.uint8):
        request: Request = Request()
        request.action_request.act = True
        request.action_request.gto = True
        request.position_request.pr = pos
        request.speed.sp = speed
        request.force.fr = force
        self._client.write_registers(
            self.INPUT_REGISTER, request.registers(), unit=self.UNIT
        )

    def status(self) -> Status:
        response = self._client.read_holding_registers(
            self.OUTPUT_REGISTER, self.NUM_REGISTERS, unit=self.UNIT
        )
        return Status.from_registers(response.registers)


if __name__ == "__main__":

    import time

    device = "/dev/ttyUSB2"
    driver = ModbusRtuDriver(device)

    driver.move(pos=0, speed=255, force=1)

    time.sleep(5)
    driver.move(pos=200, speed=1, force=1)
    while True:

        print(driver.status().position.po)
        time.sleep(0.03)
