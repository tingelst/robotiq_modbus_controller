# robotiq_modbus_controller

A Python library for controlling Robotiqs gripper over Modbus RTU and Modbus TCP

## Installation

```bash
pip3 install git+https://github.com/tingelst/robotiq_modbus_controller.git --upgrade
```

## Example

```python
from robotiq_modbus_controller.driver import RobotiqModbusRtuDriver


def main():
    device = "/dev/ttyUSB1"
    driver = RobotiqModbusRtuDriver(device)
    driver.connect()
    driver.reset()
    driver.activate()
    driver.move(pos=0, speed=1, force=1)


if __name__ == "__main__":
    main()
```