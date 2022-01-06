#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))

from gui import GUI

from dishonesty import Dishonesty
from common import InstructionsFrame, ScreenshotInstructions
from charity import Charity
from constants import CHARITY, WELCOME_TEXT, CLOSING_TEXT, INSTRUCTIONS

Intro = (InstructionsFrame, {"text": WELCOME_TEXT})
ending = (InstructionsFrame, {"text": CLOSING_TEXT})

instructionFrames = []
for i in INSTRUCTIONS:
    if type(i) != tuple:
        instructionFrames.append((InstructionsFrame, {"file": os.path.join(os.getcwd(), "Stuff", i)}))
    else:
        instructionFrames.append((ScreenshotInstructions, {"file": os.path.join(os.getcwd(), "Stuff", i[0]), 
                                                           "picture": os.path.join(os.getcwd(), "Stuff", i[1])}))
    

frames = [Intro, Charity] + instructionFrames + [Dishonesty, ending]

if not CHARITY:
    frames.remove(Charity)

GUI(frames)
