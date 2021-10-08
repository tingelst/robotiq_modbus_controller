import struct
from dataclasses import dataclass
from typing import Union
import numpy as np


@dataclass
class Action:
    act: bool = False
    gto: bool = False
    atr: bool = False
    ard: bool = False

    def to_byte(self):
        bits = [0, 0, self.ard, self.atr, self.gto, 0, 0, self.act]
        return sum(int(val) * (2 ** idx) for idx, val in enumerate(reversed(bits)))


@dataclass
class Options:
    lbp: bool = False

    def to_byte(self):
        return int(self.lbp) * 2 ** 4


@dataclass
class Position:
    pr: np.uint8 = 0

    def to_byte(self):
        return self.pr


@dataclass
class Speed:
    sp: np.uint8 = 0

    def to_byte(self):
        return self.sp


@dataclass
class Force:
    fr: np.uint8 = 0

    def to_byte(self):
        return self.fr


@dataclass
class Request:
    action: Action = Action(False, False, False, False)
    options: Options = Options(False)
    position: Position = Position(0)
    speed: Speed = Speed(0)
    force: Force = Force(0)

    def registers(self):
        return [
            (self.action.to_byte() << 8) + self.options.to_byte(),
            self.position.to_byte(),
            (self.speed.to_byte() << 8) + self.force.to_byte(),
        ]
