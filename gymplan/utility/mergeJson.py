import json
import os
import filePaths

"""
the reason this exists is for getExerciseAnim.py
so its easier to look through the json.
 this most likely wont be sed for the actual routine
"""

def logToFile(file,msg) -> None:
    with open(f"{filePaths.fpLogDir()}\\{file}",'a') as logFile:
        logFile.writelines(msg)


def getFilePaths(directory) -> list:
    filePaths = []
    for item in os.listdir(directory):
        if os.path.isdir(f"{directory}\\{item}"):
            filePaths.extend(getFilePaths(f"{directory}\\{item}"))
        else:
            filePaths.append(f'{directory}\\{item}')
    return filePaths

def merge(directory,exclude: list = None) -> dict:
    rDict = {}
    repeatKeys = {}
    for file in getFilePaths(directory):
        if exclude is not None and file in exclude: 
            logToFile('utilLog1.txt', f'Excluding {file}')
            continue
        with open(file) as jsonFile:
            try: 
                fileData = json.load(jsonFile) 
            except json.decoder.JSONDecodeError:
                 logToFile('utilLog1.txt',f'{file} is blank.')
                 continue
            logToFile('utilLog1.txt',f'\n\n{file} opened\nContents:\n\n{fileData}\n\n')
            for key, val in fileData.items():
                 if key in rDict:
                    repeatKeys[key] = 1 + repeatKeys[key] if key in repeatKeys else 1
                    rDict[f"{key}{repeatKeys[key]}"] = val

                 else:
                    rDict[key] = val
    return rDict

def extract_exercises(data):
    exercises_list = {}
    for key, value in data.items():
        for category in value.values(): 
            for exercise, details in category.items():
                exercises_list[exercise] = details  
    return exercises_list

print(extract_exercises(merge(filePaths.fpExerJson(),[r'C:\Users\mike.mat\Desktop\GymRoutineMaker\exerciseJson\videos\videos.json'])))

    