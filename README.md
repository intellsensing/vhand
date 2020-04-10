# vhand
Virtual Reality Environment (VRE) Python interface.

The virtual hand implementation is part of the [biopatrec](https://github.com/biopatrec/biopatrec) library. The documentation of the implementation can be found [here](https://github.com/biopatrec/biopatrec/wiki/VRE.md) and [here](https://github.com/biopatrec/biopatrec/wiki/VRE_Protocol.md).

Here's a minimal example to initalize a session with a right arm and move the index finger (it is assumed that the VRE application in VRE/bin/Release/Virtual Reality.exe is already running).

```python
import time
from vhand import VirtualHand

vh = VirtualHand()
vh.init_arm()

vh.move_limb(dof=4, direction=1, distance_n=5)
time.sleep(2)
vh.stop()
```
