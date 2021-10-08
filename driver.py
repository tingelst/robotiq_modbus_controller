from typing import Union, List
import numpy as np
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.client.sync import ModbusTcpClient
from request import Request
from status import Status


class ModbusDriver:
    INPUT_REGISTER: int = 0
    OUTPUT_REGISTER: int = 0
    NUM_REGISTERS: int = 3

    def __init__(self, client: Union[ModbusSerialClient, ModbusTcpClient]) -> None:
        self._client: Union[ModbusSerialClient, ModbusTcpClient] = client

    def connect(self):
        return self._client.connect()

    def disconnect(self):
        self._client.close()

    def reset(self):
        request: Request = Request()
        self._write_registers(request.registers())

    def activate(self):
        request: Request = Request()
        request.action_request.act = True
        self._write_registers(request.registers())

    def move(self, *, pos: np.uint8, speed: np.uint8, force: np.uint8):
        request: Request = Request()
        request.action_request.act = True
        request.action_request.gto = True
        request.position_request.pr = pos
        request.speed.sp = speed
        request.force.fr = force
        self._write_registers(request.registers())

    def status(self) -> Status:
        response = self._read_registers()
        return Status.from_registers(response)

    def _read_registers(self):
        registers = self._client.read_input_registers(
            self.OUTPUT_REGISTER, self.NUM_REGISTERS
        ).registers
        return registers

    def _write_registers(self, registers: List[int]):
        self._client.write_registers(self.INPUT_REGISTER, registers)


class ModbusTcpDriver(ModbusDriver):
    def __init__(self, host: str) -> None:
        client = ModbusTcpClient(host)
        super().__init__(client)


class ModbusRtuDriver(ModbusDriver):

    UNIT: int = 9
    INPUT_REGISTER: int = 1000
    OUTPUT_REGISTER: int = 2000
    NUM_REGISTERS: int = 3

    def __init__(self, device) -> None:
        client = ModbusSerialClient(
            method="rtu",
            port=device,
            stopbits=1,
            bytesize=8,
            baudrate=115200,
            timeout=0.2,
        )
        super().__init__(client)

    def _read_registers(self):
        registers = self._client.read_input_registers(
            self.OUTPUT_REGISTER, self.NUM_REGISTERS, unit=self.UNIT
        ).registers
        return registers

    def _write_registers(self, registers: List[int]):
        self._client.write_registers(
            self.INPUT_REGISTER, registers, unit=self.UNIT
        )


if __name__ == "__main__":

    import time

    # device = "/dev/ttyUSB1"
    # driver = ModbusRtuDriver(device)

    driver = ModbusTcpDriver("192.168.250.12")

    driver.connect()

    driver.reset()
    driver.activate()

    def moveit(pos):
        driver.move(pos=pos, speed=1, force=1)
        for i in range(100):
            # print(driver.status().position.po)
            print(driver.status().fault_status.flt)
            time.sleep(0.1)
