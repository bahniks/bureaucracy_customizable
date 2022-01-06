#! python3
from tkinter import *
from tkinter import ttk
from collections import deque
from time import time, perf_counter

import random
import os

from common import ExperimentFrame, InstructionsFrame
from gui import GUI
from charity import Charity



group = random.sample([(0.01, 40), (0.01, 400), (0.01, "end"),
                       (0.05, 40), (0.05, 400), (0.05, "end"),
                       (0.25, 40), (0.25, 400), (0.25, "end"),
                       (0, "control")], 1)
group = group[0]
probability = group[0]
punishment = group[1]

if punishment == "end":
    size = "úloha bude ukončena a vám i charitě zůstane vaše stávající bodová odměna"
else:
    size = "ztratíte {} bodů ze své odměny".format(punishment)

punishmentInstructions = "V tomto případě je nicméně pravděpodobnost {} %, že porušení pravidla bude odhaleno a vy za daný obrázek body navíc neobdržíte a kromě toho {}.".format(int(probability*100), size) if punishment != "control" else ""

punishmentText = """Bylo zaznamenáno zatřídění podle tvaru místo podle barvy a bylo Vám strženo {} bodů.
Pravděpodobnost zaznamenání zatřídění v rozporu s pravidly je {} %.
Úloha bude znovu pokračovat po odečtu.
""".format(punishment, probability*100)

if punishment == "end":
    punishmentText = "Bylo zaznamenáno zatřídění podle tvaru místo podle barvy, což znamená, že úloha je ukončena. Vy i vybraná charita si ponecháváte dosud získané body."





        


class DishonestyInstructions(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = dishonestyintro, height = 20, font = 18, width = 100)

        self.width = self.root.screenwidth
        self.size = int(self.width / 18)
        self.colors = ["orange", "sky blue", "yellow"]
        self.shapes = ["triangle", "square", "circle"]
        
        self.down = Canvas(self, background = "white", highlightbackground = "white",
                           highlightcolor = "white", width = self.width, height = 280)
        self.down.grid(row = 3, column = 0, sticky = (E, W), columnspan = 3)

        self.createPots()

        
    def createPots(self):
        self.pots = []
        for i in range(3):
            color = self.colors[i]
            s = ((i*2 + 1) * int(self.width)) / 6
            x0, x1, x2 = s - self.size, s, s + self.size
            y0 = 10
            y1 = y0 + 2*self.size
            if self.shapes[i] == "triangle":
                idnum = self.down.create_polygon((x0, y1, x2, y1, x1, y0), fill = color,
                                                 outline = color)
            elif self.shapes[i] == "square":
                idnum = self.down.create_rectangle((x0, y0, x2, y1), fill = color, outline = color)
            elif self.shapes[i] == "circle":
                idnum = self.down.create_oval((x0, y0, x2, y1), fill = color, outline = color)
            self.down.create_text((x1, y1+40), text = str(i+1), font = "helvetica 35")

            

class Dishonesty(ExperimentFrame):
    def __init__(self, root, practice = False):
        super().__init__(root)

        #######################
        # adjustable parameters
        self.maxObjects = 200 # adjust for testing
        self.charityBeginning = 2000
        self.spacingTime = 2.5 
        self.pauseTime = 12 # pause after punishment
        self.speed = 615
        self.bribes = [i*10 for i in range(4, 19)]
        self.bribeProbability = 0.225
        self.sortReward = 3
        self.wrongPenalty = 200
        #######################

        self.width = self.root.screenwidth
        self.height = self.root.screenheight
        self.size = int(self.width / 18)

        self.file.write("Dishonesty\n")

        self["highlightbackground"] = "white"

        self.middle = Canvas(self, background = "white", highlightbackground = "white",
                             highlightcolor = "white", width = self.width)
        self.middle.grid(row = 1, column = 0, sticky = (E, W, S, W), columnspan = 2)

        self.down = Canvas(self, background = "white", highlightbackground = "white",
                           highlightcolor = "white", width = self.width, height = 280)
        self.down.grid(row = 3, column = 0, sticky = (E, W), columnspan = 2)

        self.charityVar = StringVar()
        self.rewardVar = StringVar()
        self.numberVar = StringVar()

        self.charityText = "Charitě: {}"
        self.rewardText = "Odměna: {}"
        self.numberText = "{}/" + str(self.maxObjects)

        self.charity = ttk.Label(self, textvariable = self.charityVar, font = "helvetica 30",
                                 background = "white")
        self.reward = ttk.Label(self, textvariable = self.rewardVar, font = "helvetica 30",
                                background = "white")
        self.number = ttk.Label(self, textvariable = self.numberVar, font = "helvetica 30",
                                background = "white")

        self.charity.grid(row = 0, column = 1, pady = 20, padx = 20)
        self.reward.grid(row = 2, column = 1, pady = 20, padx = 20)
        self.number.grid(row = 0, column = 0, pady = 20)
        
        self.objects = deque()
        self.shapes = ["triangle", "square", "circle"]
        random.shuffle(self.shapes)
        self.colors = ["orange", "sky blue", "yellow"]
        random.shuffle(self.colors)
        self.infos = {}
        self.rewardObjects = {}
        self.charityTotal = self.charityBeginning
        self.rewardTotal = 0
        self.responses = []
        self.responsesTotal = 0
        self.punishmentTextObject = None

        self.charityVar.set(self.charityText.format(self.charityTotal))
        self.rewardVar.set(self.rewardText.format(self.rewardTotal))
        self.numberVar.set(self.numberText.format(self.responsesTotal + 1))

        self.createPots()

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        
        self.root.bind("1", lambda e: self.response(1))
        self.root.bind("2", lambda e: self.response(2))
        self.root.bind("3", lambda e: self.response(3))

        self.paused = True
        self.pause = self.pauseTime - 3
        self.punished = 0
        self.time = perf_counter()


    def response(self, number):
        t = perf_counter()

        if not self.objects:
            return
               
        idnum = self.objects.popleft()
        self.rewardTotal += self.sortReward

        if idnum in self.rewardObjects:
            self.middle.delete(self.rewardObjects[idnum])
        self.middle.delete(idnum)
        shape, color, bribe, _ = self.infos[idnum]
        if shape == self.shapes[number-1]:
            self.rewardTotal += bribe
            shapeRight = 1
        else:
            shapeRight = 0
        if color != self.colors[number-1]:
            self.charityTotal -= self.wrongPenalty
            colorRight = 0
        else:
            colorRight = 1

        timeScreen = t - self.infos[idnum][3]
        timePrevious = t - self.time
        responseColor = self.colors[number-1]
        responseShape = self.shapes[number-1]

        if shapeRight and not colorRight and random.random() < probability and bribe:
            if punishment != "end" and punishment != "control":
                self.rewardTotal -= punishment
            self.rewardTotal -= bribe
            self.paused = True
            self.punished = 1
        else:
            self.punished = 0

        self.charityVar.set(self.charityText.format(self.charityTotal))
        self.rewardVar.set(self.rewardText.format(self.rewardTotal))

        self.responsesTotal += 1
        self.numberVar.set(self.numberText.format(self.responsesTotal + 1))

        self.responses.append([timeScreen, timePrevious, shape, color, bribe, responseShape,
                               responseColor, shapeRight, colorRight, self.punished, self.charityTotal,
                               self.rewardTotal, number] + self.colors + self.shapes)

        self.changePotsColors()
        self.time = perf_counter()


    def punishmentUpdate(self):
        if self.pause < self.pauseTime - 3 and not self.punishmentTextObject:
            self.punishmentTextObject = self.middle.create_text((self.width/2, 125), text = punishmentText, font = "helvetica 20", justify = "center")
        elif self.pause > self.pauseTime - 3 and punishment == "end" and self.punished:
            return True
        elif self.pauseTime - 2 > self.pause > self.pauseTime - 3:
            if not self.punishmentTextObject:
                self.punishmentTextObject = self.middle.create_text((self.width/2, 125), text = "3", font = "helvetica 35", justify = "center")
            else:
                self.middle.itemconfigure(self.punishmentTextObject, text = "3")
                self.middle.itemconfigure(self.punishmentTextObject, font = "helvetica 35")
        elif self.pauseTime - 1 > self.pause > self.pauseTime - 2:
            self.middle.itemconfigure(self.punishmentTextObject, text = "2")
        elif self.pauseTime > self.pause > self.pauseTime - 1:
            self.middle.itemconfigure(self.punishmentTextObject, text = "1")
        elif self.pause > self.pauseTime:
            if self.punishmentTextObject:
                self.middle.delete(self.punishmentTextObject)
                self.punishmentTextObject = None
            self.pause = 0
            self.paused = False
        return False    


    def run(self):
        self.root.config(cursor = "none")
        self.root.unbind("<Escape>")
        self.root.bind("<Shift-Escape>", self.root.closeFun)
        t0 = perf_counter()
        objects = 0
        timer = 0
        end = False
        while True:
            t1 = perf_counter()
            dif = t1 - t0
            if not self.paused:
                self.move(dif * self.speed)
                timer += dif
            else:
                self.pause += dif
                end = self.punishmentUpdate()
            self.root.update()
            if timer > self.spacingTime and objects < self.maxObjects:
                self.createObject()
                timer -= self.spacingTime
                objects += 1
            t0 = t1
            if (objects == self.maxObjects and not self.objects) or end:
                self.root.config(cursor = "arrow")
                break
        self.root.texts["reward"] = self.rewardTotal
        self.root.texts["charityReward"] = self.charityTotal
        self.root.bind("<Escape>", self.root.closeFun)
        self.root.unbind("<Shift-Escape>")
        self.nextFun()


    def createPots(self):
        self.pots = []
        for i in range(3):
            color = self.colors[i]
            s = ((i*2 + 1) * int(self.width)) / 6
            x0, x1, x2 = s - self.size, s, s + self.size
            y0 = 10
            y1 = y0 + 2*self.size
            if self.shapes[i] == "triangle":
                idnum = self.down.create_polygon((x0, y1, x2, y1, x1, y0), fill = color,
                                                 outline = color)
            elif self.shapes[i] == "square":
                idnum = self.down.create_rectangle((x0, y0, x2, y1), fill = color, outline = color)
            elif self.shapes[i] == "circle":
                idnum = self.down.create_oval((x0, y0, x2, y1), fill = color, outline = color)
            self.pots.append(idnum)
            self.down.create_text((x1, y1+40), text = str(i+1), font = "helvetica 35")


    def changePotsColors(self):
        random.shuffle(self.colors)
        for i in range(3):
            self.down.itemconfigure(self.pots[i], fill = self.colors[i], outline = self.colors[i])
            
        
    def createObject(self):
        shape = random.choice(self.shapes)
        color = random.choice(self.colors)
        congruent = self.shapes[self.colors.index(color)] == shape
        reward = 0 if random.random() > self.bribeProbability or congruent else random.choice(self.bribes)
        x0, x1, x2 = -self.size*2, 0-self.size, 0
        y0 = 10
        y1, y2 = y0 + self.size, y0 + 2*self.size
        if shape == "triangle":
            idnum = self.middle.create_polygon((x0, y2, x2, y2, x1, y0), fill = color,
                                               outline = color)
        elif shape == "square":
            idnum = self.middle.create_rectangle((x0, y0, x2, y2), fill = color, outline = color)
        elif shape == "circle":
            idnum = self.middle.create_oval((x0, y0, x2, y2), fill = color, outline = color)
        if reward:
            self.rewardObjects[idnum] = self.middle.create_text((x1, y1), text = str(reward),
                                                                font = "helvetica 30")
        self.objects.append(idnum)
        self.infos[idnum] = (shape, color, reward, perf_counter())


    def move(self, x):
        remove = ""
        for obj in self.objects:
            coordinates = self.middle.coords(obj)
            if len(coordinates) == 4:
                x1, y1, x2, y2 = coordinates
                self.middle.coords(obj, (x1+x, y1, x2+x, y2))
            else:
                x1, y1, x2, y2, x3, y3 = coordinates
                self.middle.coords(obj, (x1+x, y1, x2+x, y2, x3+x, y3))
            if x1 > self.width:
                remove = obj
            if obj in self.rewardObjects:
                robj = self.rewardObjects[obj]
                xr, yr = self.middle.coords(robj)
                self.middle.coords(robj, (xr+x, yr))
        if remove:
            t = perf_counter()
            self.objects.remove(remove)
            self.middle.delete(remove)
            if remove in self.rewardObjects:
                self.middle.delete(self.rewardObjects[remove])
            timeScreen = t - self.infos[remove][3]
            timePrevious = t - self.time
            shape, color, bribe, _ = self.infos[remove]
            responseColor = responseShape = "NA"
            colorRight = shapeRight = 0
            self.responsesTotal += 1
            self.numberVar.set(self.numberText.format(self.responsesTotal + 1))
            self.responses.append([timeScreen, timePrevious, shape, color, bribe, responseShape,
                                   responseColor, shapeRight, colorRight, 0, self.charityTotal,
                                   self.rewardTotal, "NA"] + self.colors + self.shapes)

            
    def write(self):
        for order, line in enumerate(self.responses, 1):
            begin = [self.id, order]
            end = [self.charityTotal, self.rewardTotal, probability, punishment]
            self.file.write("\t".join(map(str, begin + line + end)) + "\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Charity,
         DishonestyInstructions,
         DishonestyInstructions2,
         DishonestyInstructions3,
         DishonestyInstructions4,
         DishonestyInstructions5,
         DishonestyInstructions6,
         DishonestyInstructions7,
         Dishonesty])

