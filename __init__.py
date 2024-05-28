import ctypes
import time
from aqt import mw
from aqt.reviewer import Reviewer
from anki.hooks import wrap

# Define necessary structures
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

xinput = ctypes.windll.xinput1_1  # Load Xinput.dll

# Set up function argument types and return type
XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint

# Helper function to set vibration
def set_vibration(controller, left_motor, right_motor):
    vibration = XINPUT_VIBRATION(int(left_motor * 65535), int(right_motor * 65535))
    XInputSetState(controller, ctypes.byref(vibration))

# Function to make the controller vibrate
def vibrate_controller(duration=0.5, left_motor=0.5, right_motor=0.5):
    print("Starting vibration")
    set_vibration(0,left_motor, right_motor)
    time.sleep(duration)
    set_vibration(0, 0.0, 0.0)
    print("Vibration ended")

# Hook into the Anki review process
def on_reviewer_did_answer_card(reviewer: Reviewer, ease: int):
    if ease == 1:  # This corresponds to the "hard" button
        print("Hard button pressed")
        vibrate_controller()
    else:
        vibrate_controller(duration=0.2, left_motor=0.2, right_motor=0.2)

Reviewer._answerCard = wrap(Reviewer._answerCard, on_reviewer_did_answer_card, "after")
