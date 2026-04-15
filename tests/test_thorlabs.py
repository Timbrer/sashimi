import time

from sashimi.hardware.cameras.thorlabs import ThorlabsCamera
from sashimi.hardware.cameras.interface import TriggerMode

# CS2100M-USB sensor is 1080(V) x 1920(H)
cam = ThorlabsCamera(
    camera_id=0,
    max_sensor_resolution=(1080, 1920),
)

cam.binning = 1
cam.roi = (0, 0, 1080, 1920)   # sashimi runtime convention: (vpos, hpos, vsize, hsize)
cam.exposure_time = 20         # ms
cam.trigger_mode = TriggerMode.FREE

cam.start_acquisition()

t0 = time.time()
n_frames = 0

try:
    while time.time() - t0 < 3.0:
        frames = cam.get_frames()
        for frame in frames:
            n_frames += 1
            print(
                f"frame {n_frames}: shape={frame.shape}, "
                f"dtype={frame.dtype}, min={frame.min()}, max={frame.max()}"
            )
        time.sleep(0.01)
finally:
    cam.shutdown()

print(f"done, total frames = {n_frames}")