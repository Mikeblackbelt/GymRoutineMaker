import json
import sys
import os
import random
import math

sys.path.append(os.path.abspath(r'C:\Users\mmati\OneDrive\Documents\GitHub\GymRoutineMaker'))

import gymplan.utility.filePaths as fp

def getMGroupExercises(section:str,group:str,subgroup: str) -> dict:
    with open(f'{fp.fpExerJson()}\\{section}\\{group}\\{subgroup}.json','r') as file:
        exercises = json.load(file)
    return exercises["Exercises"]

defaultDirectVolumeRatios = {
    'upperchest': 0.06,
    'lowerchest': 0.06, 
    'lats': 0.08, 
    'midback': 0.06,
    'frontdelts': 0.05, 
    'sidedelts': 0.08, 
    'reardelts': 0.04, 
    'biceps': 0.09, 
    'triceps': 0.08, 
    'calves': 0.06, 
    'quads': 0.12, 
    'hamstrings': 0.08, 
    'glutes': 0.06, 
    'abs': 0.05,
    'obliques': 0.03
}

class DayType():
    def __init__(self, muscles: list[list[str,str,str]], ciStructures: list[list[list[str],str,int],str] = None): 
        self.muscles = muscles 
        self.ciStructure = ciStructures

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
        
        return [returnCompounds, returnIsos]

    def establishRatios(self):
        dayPercentVolume = sum(defaultDirectVolumeRatios[muscle[2]] for muscle in self.muscles)
        newVol = {}
        for muscle in self.muscles:
            newVol[muscle[2]] = defaultDirectVolumeRatios[muscle[2]] / dayPercentVolume
        return newVol
                               
    def generate(self, sets: list[int], equipment: list[str]):
        if len(sets) != len(self.muscles) or 0 in sets: 
            raise Exception('Sets must be a list of len(muscles) nonzero integers')
        if any(i < 0 for i in sets): 
            raise Exception('All values in sets must be positive')

        ciStructure = self.ciStructure
        if ciStructure is None:
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
                    ciStructure.append([muscle, random.choice(['c', 'i']), mSets])

            print(f"Generated ciStructure (compounds and isolations split): {ciStructure}")

        exerciseList = []
        for muscle in ciStructure:
            ci = self.getCompIsol(muscle[0], equipment)
            comp = ci[0]
            iso = ci[1]
            print(f"Available compound exercises for {muscle[0]}: {comp}")
            print(f"Available isolation exercises for {muscle[0]}: {iso}")

            if muscle[1] == 'c' and len(comp) != 0:
                selected_exercise = random.choice(comp)
                exerciseList.append({selected_exercise: muscle[2]})
                print(f"Selected compound exercise: {selected_exercise} with {muscle[2]} sets")
            elif len(iso) != 0:
                selected_exercise = random.choice(iso)
                exerciseList.append({selected_exercise: muscle[2]})
                print(f"Selected isolation exercise: {selected_exercise} with {muscle[2]} sets")

        print(f"Final exercise list: {exerciseList}")
        return exerciseList

push = DayType(
    [
        ["upperbody", "chest", "upperchest"],
        ["upperbody", "chest", "lowerchest"],
        ["upperbody", "shoulders", "frontdelts"],
        ["upperbody", "shoulders", "sidedelts"],
        ["upperbody", "arms", "triceps"],
    ]
)

print(push.generate([5, 5, 6, 3, 4], ['Dumbbell', 'Machine', 'Barbell', 'Bench', 'Incline Bench']))
