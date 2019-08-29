import time
vr = VirtualHand()
vr.init_arm()
time.sleep(2)
vr.switch_camera(camera=3)
time.sleep(2)
vr.switch_camera(camera=0)
vr.move_limb(1,4,1,4,0)
