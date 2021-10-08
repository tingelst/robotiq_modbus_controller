from dataclasses import dataclass
from typing import List
import struct
import numpy as np


@dataclass
class GripperStatus:
    act: bool
    gto: bool
    sta: np.uint8
    obj: np.uint8


@dataclass
class FaultStatus:
    flt: np.uint8


@dataclass
class PositionRequestEcho:
    pr: np.uint8


@dataclass
class Position:
    po: np.uint8


@dataclass
class Current:
    cu: np.uint8


@dataclass
class Status:
    gripper_status: GripperStatus = GripperStatus(0, 0, 0, 0)
    fault_status: FaultStatus = FaultStatus(0)
    position_request_echo: PositionRequestEcho = PositionRequestEcho(0)
    position: Position = Position(0)
    current: Current = Current(0)

    @classmethod
    def from_registers(cls, registers: List[int]):
        assert len(registers) == 3
        gripper_status, _ = struct.unpack("BB", registers[0].to_bytes(2, "big"))
        fault_status, position_request_echo = struct.unpack(
            "BB", registers[1].to_bytes(2, "big")
        )
        position, current = struct.unpack("BB", registers[2].to_bytes(2, "big"))

        status = Status()
        status.gripper_status.obj = int(format(gripper_status, "08b")[0:2], 2)
        status.gripper_status.sta = int(format(gripper_status, "08b")[2:4], 2)
        status.gripper_status.gto = bool(format(gripper_status, "08b")[4])
        status.gripper_status.act = bool(format(gripper_status, "08b")[7])
        status.fault_status.flt = int(format(fault_status, "08b")[4:], 2)
        status.position_request_echo.pr = position_request_echo
        status.position.po = position
        status.current.cu = current

        return status
