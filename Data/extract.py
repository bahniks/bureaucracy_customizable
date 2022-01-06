import os

studies = ["Charity",
           "Dishonesty",
           "Lottery",
           "Comparison",
           "Abolute",
           "Weak evidence",
           "Hexaco",
           "Dishonesty Questions",
           "Demographics",
           "Winnings",
           "Comments"
           ]


columns = {"Charity": ("id", "charity"),
           "Dishonesty": ("id", "order", "time_screen", "time_previous", "shape", "color", "bribe",
                          "response_shape", "response_color", "correct_shape", "correct_color", "was_punished",
                          "charity_total", "reward_total", "response_number", "color1", "color2", "color3",
                          "shape1", "shape2", "shape3", "charity_end", "reward_end", "probability_punishment",
                          "size_punishment"),
           "Lottery": ("id", "rolls", "reward"),
           "Comparison": ("id", "item", "anchor", "comparison", "time"),
           "Abolute": ("id", "item", "absolute", "time"),
           "Weak evidence": ("id", "trial", "item", "condition", "answer"),
           "Hexaco": ("id", "question", "agree"),
           "Dishonesty Questions": ("id", "purpose", "bribe_despicable", "bribe_unjust", "bribe_dishonest",
                                    "bribe_immoral", "bribe_comment", "charity_praiseworthy", "charity_just",
                                    "charity_honest", "charity_moral", "charity_comment"),
           "Demographics": ("id", "sex", "age", "language", "student", "field"),
           "Winnings": ("id", "total_reward", "sorting_reward", "lottery_reward", "charity_reward", "charity"),
           "Comments": ("comment")
           }

frames = ["Intro",
          "Charity",
          "DishonestyInstructions",
          "DishonestyInstructions2",
          "DishonestyInstructions3",
          "DishonestyInstructions4",
          "DishonestyInstructions5",
          "DishonestyInstructions6",
          "DishonestyInstructions7",
          "Dishonesty",
          "LotteryInstructions",
          "Lottery",
          "AnchoringInstructions1",
          "Comparison",
          "AnchoringInstructions2",
          "Absolute",
          "WeakEvidenceInstructions",
          "WeakEvidence",
          "HexacoInstructions",
          "Hexaco",
          "Debriefing",
          "Demographics",
          "Comments",
          "ending",
          "end"
          ]

for study in studies:
    with open("{} results.txt".format(study), mode = "w") as f:
        f.write("\t".join(columns[study]))

with open("Time results.txt", mode = "w") as times:
    times.write("\t".join(["id", "order", "frame", "time"]))

dirs = os.listdir()
#filecount = 0 #
for directory in dirs:
    if ".py" in directory or "results" in directory:
        continue
    files = os.listdir(directory)
    for file in files:
        if ".py" in file or "results" in file or "file.txt" in file or ".txt" not in file:
            continue

        with open(os.path.join(directory, file)) as datafile:
            #filecount += 1 #
            count = 1
            for line in datafile:
                study = line.strip()
                if line.startswith("time: "):
                    with open("Time results.txt", mode = "a") as times:
                        times.write("\n" + "\t".join([file, str(count), frames[count-1], line.split()[1]]))
                        count += 1
                        continue
                if study in studies:
                    with open("{} results.txt".format(study), mode = "a") as results:
                        for line in datafile:
                            content = line.strip()
                            if columns[study][0] == "id" and content: #
                                identificator = content.split()[0] #
                                content = content.replace(identificator, identificator + "_" + directory) #
                                #content = content.replace(identificator, identificator + "_" + str(filecount)) #
                            if not content:
                                break
                            else:
                                results.write("\n" + content)
                        
                

    
        
