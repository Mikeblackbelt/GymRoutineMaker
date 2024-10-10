import json
import os

"""
the reason this exists is for getExerciseAnim.py
so its easier to look through the json.
 this most likely wont be sed for the actual routine
"""

def getFilePaths(directory) -> list:
    filePaths = []
    for item in os.listdir(directory):
        if os.path.isdir(f"{directory}\\{item}"):
            filePaths.extend(getFilePaths(f"{directory}\\{item}"))
        else:
            filePaths.append(f'{directory}\\{item}')
    return filePaths

def merge(directory) -> dict:
    rDict = {}
    repeatKeys = {}
    for file in getFilePaths(directory):
        with open(file) as jsonFile:
            fileData = json.load(jsonFile)
            for key, val in fileData.items():
                 if key in rDict:
                    repeatKeys[key] = 1 + repeatKeys[key] if key in repeatKeys else 1
                    rDict[f"{key}{repeatKeys[key]}"] = val

                 else:
                    rDict[key] = val
                  

    return rDict

print(merge(r"C:\Users\mike.mat\Desktop\GymRoutineMaker\exerciseJson"))
    