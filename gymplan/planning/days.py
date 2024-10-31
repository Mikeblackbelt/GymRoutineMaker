import json
import sys
import os
import random
import math

sys.path.append(os.path.abspath(r'C:\Users\mike.mat\Desktop\GymRoutineMaker'))

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
   def __init__(self, muscles: list[list[str,str,str]], ciStructures: list[list[list[str],str,int],str] = None): #me when nested lists
        """
        muscles: muscles trained in the day being constructed. the first item of each object should be the SECTION (i.e: upper body), the second should be GROUP (i,e: chest) and the third should be the subgrouP (i.e: upperchest)
        ciStructures: list of the the distribution of compound/isolation exercises of each day. should be structured something like [[[upperbody,chest,upperchest], c]]. c represents compound, i represents isolation. strings. if None, one is automatically generated as per the logic in self.generate()
        """

        self.muscles =  muscles 
        self.ciStructure = ciStructures
    
   def getCompIsol(self, muscle: list[list[str,str,str]],equipment: list[str]):
        """
        muscle: [section,group,subgroup] i.e: [upperbody,chest,upperchest]
        equipmnent: avaible equipment, i.e ['dumbell','dip station','bench']
        """
        equipment = [x.lower() for x in equipment]

        returnCompounds = []
        returnIsos = []

        exercises = getMGroupExercises(muscle[0],muscle[1],muscle[2])
        for item in exercises['Compound']:
           if all(equipmentItem.lower() in equipment for equipmentItem in item['Equipment']):
               returnCompounds.append(item)
        
        for item in exercises['Isolation']:
            if all(equipmentItem.lower() in equipment for equipmentItem in item['Equipment']):\
                returnIsos.append(item)
        return [returnCompounds,returnIsos]

        #not finished

   def generate(self, sets: list[int], equipment: list[str]):
        """
        sets: list of sets per muscle. sets[i] coresponds to self.muscles[i] YES I COULDVE MADE THIS  A KV PAIR
        equipment: all avaible equipment, or [] if None
        """
        if len(sets) != len(self.muscles) or 0 in sets: raise Exception('Sets must be a list of 4 integers')
        if any(i < 0 for i in sets): raise Exception('All values in sets must be positive')
        
        ciStructure = self.ciStructure
        if ciStructure is None:
            indexTracker = -1
            for muscle,mSets in zip(self.muscles,sets): #compounds first
                indexTracker += 1
                if mSets > 9:
                    ciStructure.append([muscle,'c',math.ceil(mSets/3)])
                    ciStructure.append([muscle,'c',math.floor(mSets/3)])
                    sets[indexTracker] -= math.ceil(mSets/3) + math.floor(mSets/3)
                elif mSets > 4:
                    ciStructure.append([muscle,'c',math.ceil(mSets/2)])
                    sets[indexTracker] -= math.ceil(mSets/2)
                else:
                    ciStructure.append([muscle,random.choice(['c','i']),mSets])
            for muscle, mSets in zip(self.muscles,sets): #isolations
                if mSets != 0:
                    ciStructure.append([muscle,'i',mSets])
    
        exerciseList = []
        else:
            pass #finish this

        
        for muscle in ciStructure:
           ci = self.getCompIsol(muscle[0])
           comp = ci[0]; iso = ci[1]
           if muscle[1] = 'c':
              exerciseList.append({random.choice(comp).keys()[0]:muscle[2]})
           else:
              exerciseList.append({random.choice(comp).keys()[0]:muscle[2]})

        return exerciseList

push = DayType(
    [
        ["upperbody", "chest", "upperchest"],
        ["upperbody", "chest", "lowerchest"],
        ["upperbody", "shoulders", "frontdelts"],
        ["upperbody", "shoulders", "sidedelts"],
        ["upperbody", "arms", "triceps"],
    ] #add the other one later
)
