import ctypes
import time
import json
import os
from aqt import mw
from aqt.reviewer import Reviewer
from anki.hooks import wrap

# Define necessary structures
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

def load_xinput():
    xinput_versions = ['xinput1_1.dll', 'xinput1_3.dll', 'xinput1_2.dll', 'xinput1_4.dll', 'xinput9_1_0.dll']
    for xinput_version in xinput_versions:
        try:
            xinput = ctypes.windll.LoadLibrary(xinput_version)
            print(f"Loaded {xinput_version}")
            return xinput
        except OSError:
            continue
    raise OSError("No suitable XInput library found.")

xinput = load_xinput() # Load Xinput.dll

# Set up function argument types and return type
XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint

# Helper function to set vibration
def set_vibration(controller, left_motor, right_motor):
    vibration = XINPUT_VIBRATION(int(left_motor * 65535), int(right_motor * 65535))
    result = XInputSetState(controller, ctypes.byref(vibration))
    print(f"Set vibration result: {result}")

# Function to make the controller vibrate
def vibrate_controller(duration=0.5, left_motor=0.5, right_motor=0.5):
    print(f"Starting vibration: duration={duration}, left_motor={left_motor}, right_motor={right_motor}")
    for controller in range(4):
        set_vibration(controller, left_motor, right_motor)
    time.sleep(duration)
    for controller in range(4):
        set_vibration(controller, 0.0, 0.0)
    print("Vibration ended")

# Load the configuration from config.json
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

config = load_config()

# Hook into the Anki review process
def on_reviewer_did_answer_card(reviewer: Reviewer, ease: int):
    print(f"Card answered with ease: {ease}")
    if ease == 1:  # This corresponds to the "again" button
        print("Again button pressed")
        settings = config["again"]
        vibrate_controller(settings["duration"], settings["intensity"], settings["intensity"])
    elif ease == 2: # This corresponds to the "hard" button
        print("Hard button pressed")
        settings = config["hard"]
        vibrate_controller(settings["duration"], settings["intensity"], settings["intensity"])
    elif ease == 3: # This corresponds to the "good" button
        print("Good button pressed")
        settings = config["good"]
        vibrate_controller(settings["duration"], settings["intensity"], settings["intensity"])
    elif ease == 4: # This corresponds to the "easy" button
        print("Easy button pressed")
        settings = config["easy"]
        vibrate_controller(settings["duration"], settings["intensity"], settings["intensity"])

Reviewer._answerCard = wrap(Reviewer._answerCard, on_reviewer_did_answer_card, "after")
