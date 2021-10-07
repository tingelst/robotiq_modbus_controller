import struct
from dataclasses import dataclass
from typing import Union
import numpy as np


@dataclass
class ActionRequest:
    act: Union[bool, int] = False
    gto: Union[bool, int] = False
    atr: Union[bool, int] = False
    ard: Union[bool, int] = False

    def to_hex(self):
        bits = [0, 0, self.ard, self.atr, self.gto, 0, 0, self.act]
        return struct.pack(
            "B", sum(int(val) * (2 ** idx) for idx, val in enumerate(reversed(bits)))
        )


@dataclass
class GripperOptions:
    lbp: bool = False

    def to_hex(self):
        return struct.pack("B", int(self.lbp) * 2 ** 4)


@dataclass
class GripperOptions2:
    def to_hex(self):
        return struct.pack("B", 0)


@dataclass
class PositionRequest:
    pr: np.uint8 = 0

    def to_hex(self):
        return struct.pack("B", self.pr)


@dataclass
class Speed:
    sp: np.uint8 = 0

    def to_hex(self):
        return struct.pack("B", self.sp)


@dataclass
class Force:
    fr: np.uint8 = 0

    def to_hex(self):
        return struct.pack("B", self.fr)


@dataclass
class Request:
    action_request: ActionRequest = ActionRequest(False, False, False, False)
    gripper_options: GripperOptions = GripperOptions(False)
    position_request: PositionRequest = PositionRequest(0)
    speed: Speed = Speed(0)
    force: Force = Force(0)

    def to_hex(self):
        return (
            self.action_request.to_hex()
            + self.gripper_options.to_hex()
            + self.position_request.to_hex()
            + GripperOptions2().to_hex()
            + self.speed.to_hex()
            + self.force.to_hex()
        )


req = Request(action_request=ActionRequest(True, True, False, False))
print(req.to_hex())

action_request = ActionRequest(act=True, gto=1, atr=0, ard=0)
gripper_options = GripperOptions(lbp=False)
gripper_options2 = GripperOptions2()
position_request = PositionRequest(255)
speed = Speed(255)
force = Force(255)

action_request.to_hex()

req = (
    action_request.to_hex()
    + gripper_options.to_hex()
    + gripper_options2.to_hex()
    + position_request.to_hex()
    + speed.to_hex()
    + force.to_hex()
)

print(req)
