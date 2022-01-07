# In general, keep the formating of the file unchanged. You can change the numeric values and texts between quaotes to adjust the options.
# The text after "#" are comments with instructions and recommendations and this text can be removed at will.

# Group assignment
#-----------------------------------------------------------------------------------------------------------------
# names of groups and their relative chance of assignment
GROUPS = {"control": 1,
          "low_probability": 1, # you can remove rows to include fewer options
          "small_size": 1} # you can add additional rows to include additional options


# Welcome screen
#-----------------------------------------------------------------------------------------------------------------
# the text shown on the initial screen
WELCOME_TEXT = """
Welcome to the study.
Please proceed by pressing Continue.
"""


# Charities
#-----------------------------------------------------------------------------------------------------------------
CHARITY = True # change to False if you do not want to ask participants to select a charity for which they play

CHARITIES = ["Charity 1",
             "Charity 2",
             "Charity 3", # you can remove rows to include fewer options
             "Charity 4"] # you can add additional rows to include additional options

# write instructions for selection of a charity below
INSTRUCTIONS_CHARITIES = """
Please choose one of the following charities, for which you could earn money in the following task.
"""


# Instructions
#-----------------------------------------------------------------------------------------------------------------
# texts of intstructions are loaded from files specified below
# it is also possible to show a picture (in a .gif format) with the instructions (an example how to do that is shown for the second screen below)
INSTRUCTIONS = ["instructions1.txt",
                ("instructions2.txt", "screen2.gif"),
                "instructions3.txt"
                ]


# Closing screen
#-----------------------------------------------------------------------------------------------------------------
# the text shown on the last screen
CLOSING_TEXT = """
Thank you for your participation!
"""


# Task
#-----------------------------------------------------------------------------------------------------------------
NUMBER_OF_OBJECTS = 5
CHARITY_ENDOWMENT = 2000
BRIBE_PROBABILITY = 0.225
SORTING_REWARD = 3
BRIBE_SIZES = [30, 60, 90, 120, 150, 180]
INCORRECT_SORTING_PENALTY = 200
TIME_BETWEEN_OBJECTS = 2.5 # in seconds
OBJECT_SPEED = 615 # pixels per second

# only relevant if there is punishment
#-------------------------------------
PUNISHMENT = True # change to False if you do not want to include punishment in the task
PUNISHMENT_PROBABILITY = 0.00
PUNISHMENT_SIZE = 0.00
PAUSE_AFTER_PUNISHMENT = 12 # in seconds
PUNISHMENT_TEXT = """Sorting by shape instead of color was recorded and you lost {size} points.
The probability that sorting against the rules is recorded is {probability} %.
The task will continue after a countdown.
""" # this text is shown after punishment, the {size} and {probability} can be used as in the current text to show the punishment size and probability


# Experimental manipulations
#-----------------------------------------------------------------------------------------------------------------
# you can manipulate any option between groups using the setting below
# in this example the groups differ in the punishment probability and size
USE_SETTINGS = True # change to False if you do not want to worry about this
settings = {
            "control": ["PUNISHMENT_PROBABILITY = 0",
                        "PUNISHMENT_SIZE = 0"],
            "low_probability": ["PUNISHMENT_PROBABILITY = 0.01",
                                "PUNISHMENT_SIZE = 200"],
            "small_size": ["PUNISHMENT_PROBABILITY = 0.10",
                           "PUNISHMENT_SIZE = 20"]
            }


# Options for testing
#-----------------------------------------------------------------------------------------------------------------
TESTING = True

# screen size for testing 
SCREENWIDTH = 1680 # in pixels
SCREENHEIGHT = 1050 # in pixels















# DO NOT CHANGE
#-----------------------------------------------------------------------------------------------------------------
from random import random
groupNames = []
groupSizes = []
currentSize = 0
for name, size in GROUPS.items():
    groupNames.append(name)
    currentSize += size
    groupSizes.append(currentSize)
groupSizes = [size/currentSize for size in groupSizes]
selection = random()
for i in range(len(groupSizes)):
    if selection <= groupSizes[i]:
        GROUP = groupNames[i]
        break

if USE_SETTINGS:
    if GROUP in settings:
        for setting in settings[GROUP]:
            exec(setting)