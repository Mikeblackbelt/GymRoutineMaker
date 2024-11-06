import json
import sys
import os
import random
import math
import days

sys.path.append(os.path.abspath(r'C:\Users\mmati\OneDrive\Documents\GitHub\GymRoutineMaker'))

import gymplan.utility.filePaths as fp
import gymplan.utility.mergeJson as mj

def getMGroupExercises(section:str,group:str,subgroup: str) -> dict:
    with open(f'{fp.fpExerJson()}\\{section}\\{group}\\{subgroup}.json','r') as file:
        exercises = json.load(file)
    return exercises["Exercises"]

class plDayType:
    def __init__(self,lift: union(list,str),muscles: list[list[str,str,str]]) -> None:
        self.lift = lift
        self.muscles = muscles
    
    def getCompIsol(self, muscle: list[list[str,str,str]], equipment: list[str]) -> list:
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
    
    def getAccessories(self, equipment: list[str]) -> list:
        accessories = []
        for muscle in self.muscles:
            accessories.append(getCompIsol(muscle, equipment)[0])
        return accessories

    def generate(self,setsTotal: int,equipment: list[str]) -> list[dict{str:int}]:
        rlist = []
        if 'Barbell' not in equipment or if 'Bench' not in equipment: raise Exception('A powerlifting routine requires a barbell and a bench...how do you expect to powerlift?')
        if type(self.lift) == list:
            if setsTotal < 4*len(self.lift):
                for lifts in self.lift:
                    rlist.append({lifts: math.ceil(setsTotal/len(self.lift))})
                return rlist
            elif setsTotal < 6*lens(self.lift):
                for lifts in self.lift:
                    liftSets = random.choice([3,4,5])
                    rlist.append({lifts: liftSets})
                    setsTotal -= liftSets
                #conttinue 
            else:
                #continue
                pass
        else:
            #continue
            pass
                
           