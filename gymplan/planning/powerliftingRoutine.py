import json
import sys
import os
import random
import math
import days
import typing
import backupfp as b
sys.path.append(os.path.abspath(b.main()))

import gymplan.utility.filePaths as fp
import gymplan.utility.mergeJson as mj

def getMGroupExercises(section:str,group:str,subgroup: str) -> dict:
    with open(f'{fp.fpExerJson()}\\{section}\\{group}\\{subgroup}.json','r') as file:
        exercises = json.load(file)
    return exercises["Exercises"]

class plDayType:
    def __init__(self,lift: typing.Union[list,str],muscles: list[list[str,str,str]]) -> None:
        self.lift = lift
        self.muscles = muscles
        mj.logToFile('planlogs.txt',f'{self} initated (plDayType)*')
    def getCompIsol(self, muscle: list[list[str,str,str]], equipment: list[str]) -> list: #stolen from days.py
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
    
    def getAccessories(self, equipment: list[str]) -> list[list[str]]:
        accessories = []
        for muscle in self.muscles:
            asc = self.getCompIsol(muscle, equipment)[0]
            accessories.append(asc) #choose append bc i want to split it into muscles
            mj.logToFile('planlogs.txt',f'\nAccessories updated:\n + {asc}\n')
        while [] in accessories:
            accessories.remove([])
        for item in accessories:
           if type(self.lift) == str and self.lift in item:
               item.remove(self.lift)
           else:
               for lift in self.lift:
                   if lift in item: item.remove(lift)
        
        mj.logToFile('planlogs.txt', f'\n{self}.getAccessories({equipment}) returned:\n {accessories}\n')
        return accessories

    def generate(self, setsTotal: int, equipment: list[str]) -> list[dict[str: int]]: #slightly refactored by chatgpt
        rlist = []
        added_exercises = set()  # Track added exercises to avoid duplicates
        mj.logToFile('planlogs.txt',f'{self}.generate({setsTotal},{equipment} is being run)') 
        if 'Barbell' not in equipment or 'Bench' not in equipment:
            raise Exception('A powerlifting routine requires a barbell and a bench...how do you expect to powerlift?')

        if type(self.lift) == str:
            self.lift = [self.lift]

        if setsTotal < 4 * len(self.lift):
            for lifts in self.lift:
                rlist.append({lifts: math.ceil(setsTotal / len(self.lift))})
            mj.logToFile('planlogs.txt', f'\n{self}.generate() returned routine:\n {rlist}\n')
            return rlist
        elif setsTotal <= 6 * len(self.lift):
            setslist = [3, 4, 5]
        else:
            setslist = [3, 4, 5, 6]

        for lifts in self.lift:
            liftSets = random.choice(setslist)
            rlist.append({lifts: liftSets})
            added_exercises.add(lifts)  # Add the lift to track duplicates
            setsTotal -= liftSets  

        accessories = math.floor((setsTotal + 1) / 3) if setsTotal >= 2 else 1
        mj.logToFile('planlogs.txt', f'\nChoose {accessories} accessories.\n')
        setsPerAc = round(setsTotal / accessories)

        for _ in range(accessories):
            accessory = None
            accessory_attempts = 0
            while accessory_attempts < 10:
                candidate = random.choice(random.choice(self.getAccessories(equipment)))
                if candidate not in added_exercises and candidate not in ['Bench Press','Squat','Deadlift']:
                    accessory = candidate
                    break
                accessory_attempts += 1
            if accessory:
                rlist.append({accessory: setsPerAc})
                added_exercises.add(accessory)  # Track the added accessory to prevent duplicates

        mj.logToFile('planlogs.txt', f'\n{self}.generate() returned routine:\n {rlist}\n')
        return rlist


benchDay = plDayType('Bench Press', days.pushMuscles)
sqd = [['lowerbody', 'legs', 'quads'], ['lowerbody', 'legs', 'glutes']]

squatDay = plDayType('Squat',sqd)

dlMuscles = [
       ["lowerbody","legs","hamstrings"],
       ["upperbody","back","midback"],
       ["upperbody","arms","forearms"],
]
deadliftDay = plDayType('Deadlift',dlMuscles)
ascM = dlMuscles + days.pushMuscles + sqd
ascDay = days.DayType(ascM)

if __name__ == "__main__":
    print('asc')
    print(ascDay.generate([4]*len(ascM),['Barbell','Bench','Dumbbell','Incline Bench', 'Machine', 'Cable', 'Dip Station']))
    print('push')
    print(benchDay.generate(4*len(days.pushMuscles),['Barbell','Bench','Dumbbell','Incline Bench', 'Machine', 'Cable', 'Dip Station']))
            
                
        