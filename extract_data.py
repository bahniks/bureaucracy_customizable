import os

studies = ["Charity",
           "Dishonesty"
           ]


columns = {"Charity": ("id", "charity"),
           "Dishonesty": ("id", "trial", "time_on_screen", "time_from_previous", "object_shape", "object_color", "bribe_size",
                          "response_shape", "response_color", "correct_shape", "correct_color", "was_punished",
                          "charity_total", "reward_total", "response_number", "color1", "color2", "color3",
                          "shape1", "shape2", "shape3", "charity_end", "reward_end", "probability_punishment",
                          "size_punishment", "group")
           }

for study in studies:
    with open("{} results.txt".format(study), mode = "w") as f:
        f.write("\t".join(columns[study]))

dirs = os.listdir()

for directory in dirs:
    if ".py" in directory or "results" in directory or "." in directory or "LICENSE" in directory:
        continue
    files = os.listdir(directory)
    for file in files:
        if ".py" in file or "results" in file or "file.txt" in file or ".txt" not in file:
            continue

        with open(os.path.join(directory, file)) as datafile:
            count = 1
            for line in datafile:
                study = line.strip()
                if study in studies:
                    with open("{} results.txt".format(study), mode = "a") as results:
                        for line in datafile:
                            content = line.strip()
                            if columns[study][0] == "id" and content: #
                                identificator = content.split()[0] #
                                content = content.replace(identificator, identificator + "_" + directory) #
                            if not content:
                                break
                            else:
                                results.write("\n" + content)
                        
                

    
        
