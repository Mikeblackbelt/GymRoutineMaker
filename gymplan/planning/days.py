import json
import sys
import os
import random
import math

sys.path.append(os.path.abspath(r'C:\Users\mike.mat\Desktop\GymRoutineMaker'))

import gymplan.utility.filePaths as fp
import gymplan.utility.mergeJson as mj

def getMGroupExercises(section:str,group:str,subgroup: str) -> dict:
    with open(f'{fp.fpExerJson()}\\{section}\\{group}\\{subgroup}.json','r') as file:
        exercises = json.load(file)
    return exercises["Exercises"]

defaultDirectVolumeRatios = {
    'chest': 0.10,
    'lats': 0.08, 
    'midback': 0.08,
    'frontdelts': 0.04, 
    'sidedelts': 0.09, 
    'reardelts': 0.04, 
    'biceps': 0.08, 
    'triceps': 0.07, 
    'calves': 0.06, 
    'quads': 0.10, 
    'hamstrings': 0.09, 
    'glutes': 0.06, 
    'abs': 0.05,
    'obliques': 0.03,
    'forearms': 0.04
}

class DayType():
    def __init__(self, muscles: list[list[str,str,str]]): 
        self.muscles = muscles 
        mj.logToFile('planlogs.txt',f'\n{self} initated\n')

    def getCompIsol(self, muscle: list[list[str,str,str]], equipment: list[str]):
        equipment = [x.lower() for x in equipment]
        returnCompounds = []
        returnIsos = []

        exercises = getMGroupExercises(muscle[0], muscle[1], muscle[2])
        for item in exercises['Compound']:
            if all(equipmentItem.lower() in equipment for equipmentItem in exercises['Compound'][item]['Equipment']):
                returnCompounds.append(item)
        
        for item in exercises['Isolation']:
            if all(equipmentItem.lower() in equipment for equipmentItem in exercises['Isolation'][item]['Equipment']):
                returnIsos.append(item)
        mj.logToFile('planlogs.txt', f'\n{self}.getCompIsol returned \n{[returnCompounds, returnIsos]}\n')
        return [returnCompounds, returnIsos]

    def establishRatios(self):
        dayPercentVolume = sum(defaultDirectVolumeRatios[muscle[2]] for muscle in self.muscles)
        newVol = {}
        for muscle in self.muscles:
            newVol[muscle[2]] = defaultDirectVolumeRatios[muscle[2]] / dayPercentVolume
        return newVol
                               
    def generate(self, sets: list[int], equipment: list[str]):
        if len(sets) != len(self.muscles) or 0 in sets: 
            mj.logToFile('planlogs.txt',f'\nError in {self}.generate():\n len(sets) != len(self.muscles).\nSets: {sets}\nMuscles: {self.muscles}\n')
            raise Exception(f'Sets must be a list of len(self.muscles) ({len(self.muscles)}) nonzero integers')
        if any(i < 0 for i in sets): 
            mj.logToFile('planlogs.txt',f'\nSets: {sets} contains negative value\n')
            raise Exception('All values in sets must be positive')

        ciStructure = []
        for muscle, mSets in zip(self.muscles, sets):
            if mSets > 9:
                ciStructure.append([muscle, 'c', math.ceil(mSets / 3)])
                ciStructure.append([muscle, 'c', math.floor(mSets / 3)])
                ciStructure.append([muscle, 'i', mSets - (math.ceil(mSets / 3) + math.floor(mSets / 3))])
            elif mSets > 4:
                ciStructure.append([muscle, 'c', math.ceil(mSets / 2)])
                ciStructure.append([muscle, 'i', mSets - math.ceil(mSets / 2)])
            else:
                ciStructure.append([muscle,random.choice(['c','c','i']), mSets])

        mj.logToFile('planlogs.txt',f"Generated ciStructure (compounds and isolations split): {ciStructure}")

        exerciseList = []
        for muscle in ciStructure:
            ci = self.getCompIsol(muscle[0], equipment)
            comp = ci[0]
            iso = ci[1]
            mj.logToFile('planlogs.txt',f"\nAvailable compound exercises for {muscle[0]}: {comp}\n")
            mj.logToFile('planlogs.txt',f"\nAvailable isolation exercises for {muscle[0]}: {iso}\n")

            if muscle[1] == 'c' and len(comp) != 0:
                selected_exercise = random.choice(comp)
                exerciseList.append({selected_exercise: muscle[2]})
                mj.logToFile('planlogs.txt',f"\nSelected compound exercise: {selected_exercise} with {muscle[2]} sets")
            elif len(iso) != 0:
                selected_exercise = random.choice(iso)
                exerciseList.append({selected_exercise: muscle[2]})
                mj.logToFile('planlogs.txt',f"\nSelected isolation exercise: {selected_exercise} with {muscle[2]} sets")

        mj.logToFile('planlogs.txt',f"\nFinal exercise list: {exerciseList}")
        return exerciseList

pushMuscles = [
    ["upperbody", "chest", "chest"],
    ["upperbody", "shoulders", "frontdelts"],
    ["upperbody", "shoulders", "sidedelts"],
    ["upperbody", "arms", "triceps"]
]
pushConstruct = DayType(pushMuscles)

pullMuscles = [
        ["upperbody", "back", "lats"],
        ["upperbody","back","midback"],
        ["upperbody","arms","biceps"],
        ["upperbody","arms","forearms"],
        ["upperbody", "shoulders", "reardelts"]
]
pullConstruct = DayType(pullMuscles)

legMuscles =   [
       ["lowerbody","legs","quads"] ,
       ["lowerbody","legs","hamstrings"],
       ["lowerbody","legs","glutes"],
       ['lowerbody',"legs","calves"],
       ['lowerbody','abs','abs'],
       ['lowerbody','abs','obliques']
]
legConstruct = DayType(legMuscles)

upperMuscles = random.choice([pushMuscles+pullMuscles,pullMuscles+pushMuscles])
upperMuscles.remove(["upperbody", "shoulders", "reardelts"])
upperMuscles.remove(["upperbody","arms","forearms"])
upperConstruct = DayType(upperMuscles)

fbMuscles = [
        ["upperbody", "back", "lats"],
        ["upperbody","back","midback"],
        ["upperbody","arms","biceps"],
        ["upperbody", "chest", "chest"],
        ["upperbody", "shoulders", "sidedelts"],
        ["upperbody", "arms", "triceps"],
        ["lowerbody","legs","quads"] ,
        ["lowerbody","legs","hamstrings"],
        ["lowerbody","legs","glutes"],
        ['lowerbody',"legs","calves"],
        ['lowerbody','abs','abs'],
]
fbMuscles.remove(['lowerbody','abs','abs'])
fullConstruct = DayType(fbMuscles)

#print(pushConstruct.generate([5, 5, 6, 3, 4], ['Dumbbell', 'Machine', 'Barbell', 'Bench', 'Incline Bench']))
