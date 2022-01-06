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




TESTING = True

# screen size for testing 
SCREENWIDTH = 1680 # in pixels
SCREENHEIGHT = 1050 # in pixels



