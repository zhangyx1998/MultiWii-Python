# MultiWii-Python

Author: _[Yuxuan Zhang](mailto:yuxuan@yuxuanzhang.net)_.

> A python implementation of serial MultiWii protocol.
>
> Crafted to be both easy to use and straightforward to extend.


## Usage

Initialization:

```python
from lib import MultiWii, MSP
fc = MultiWii("/dev/ttyACMx")
```

There are two types of commands, they are all invoked by `fc.invoke()`:

1. Read Command: it sends a command without any data to the controller and
expects a specific answer from the controller.

    ```python
    # Example
    result = fc.invoke(MSP.RC())
    # result is a dict object
    # e.g. {'ROLL': 1498, 'PITCH': 1500, 'YAW': 1500, 'THROTTLE': 1898, 'AUX1': 2000, 'AUX2: 2000, ... }
    ```

2. Write command 

    ```python
    # Example 1: set values by keyword arguments
    fc.invoke(MSP.SET_RAW_RC(
        ROLL=1200,
        PITCH=1300,
        YAW=1400,
        THROTTLE=1500,
    ))
    ```

    ```python
    # Example 2: set values by positional arguments
    fc.invoke(MSP.SET_RAW_RC(
        1200, # ROLL
        1300, # PITCH
        1400, # YAW
        1500, # THROTTLE
        *([0] * 12) # AUX1 - AUX12
    ))
    ```

    ```python
    # Example 3: mixed usage of positional args and kwargs are allowed
    fc.invoke(MSP.SET_RAW_RC(
        1200, # ROLL
        1300, # PITCH
        1400, # YAW
        1500, # THROTTLE
        AUX1=123,
        AUX2=456
    ))
    ```

    Unspecified arguments are filled by 0.

## Abstraction under the hood

The protocol specifications live under `lib/MSP.py`.
Each command is inherited from either `class ReadCMD` or `class WriteCMD`.

Extension of both classes requires only the defination of two static variables,
the command's `code` (int) and the command's `struct` (OrderedList).

For example, the commands to read/write RC channels look like this:

```python
class RC(ReadCMD):
    """
    ROLL/PITCH/YAW/THROTTLE/AUX1-AUX12
    Range [1000;2000]
    """
    code = 105
    struct = OrderedDict(
        ROLL=U16,
        PITCH=U16,
        YAW=U16,
        THROTTLE=U16,
        **U16.ARRAY(12, start=1, prefix="AUX")
    )

class SET_RAW_RC(WriteCMD):
    """
    This request is used to inject RC channel via MSP.
    Each chan overrides legacy RX as long as it is refreshed at least every second. See UART radio projects for more details.
    """
    code = 200
    struct = OrderedDict(
        ROLL=U16,
        PITCH=U16,
        YAW=U16,
        THROTTLE=U16,
        **U16.ARRAY(12, start=1, prefix="AUX")
    )
```

All further work beyond these are handled by their parent classes.
(See [lib/MultiWii.py](lib/MultiWii.py) for binary protocol related stuff and [lib/Command.py](lib/Command.py) for serialization/deserialization related stuff.)

You can easily extend the protocol if you want to implement more commands.
