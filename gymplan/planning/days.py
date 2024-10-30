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

class RoutineDay():
   def __init__(self, muscles: list[list[str]], ciStructures: list[list[list[str],str,int]] = None): #me when nested lists
        """
        muscles: muscles trained in the day being constructed. the first item of each object should be the SECTION (i.e: upper body), the second should be GROUP (i,e: chest) and the third should be the subgrouP (i.e: upperchest)
        ciStructures: list of the the distribution of compound/isolation exercises of each day. should be structured something like [[[[upperbody,chest,upperchest], c,3]. c represents compound, i represents isolation. strings. if None, one is automatically generated as per the logic in self.generate()
        """

       self.muscles =  muscles 
       self.ciStructure = ciStructure
    
    def getCompIsol(self, muscle[list[str,str,str]],equipment: list[str]):
        """
        muscle: [section,group,subgroup] i.e: [upperbody,chest,upperchest]
        equipmnent: aviable equipment
        """
        exercises = getMGroupExercises(muscle[0],muscle[1],muscle[2])

        #not finished

    def generate(sets: list[int], equipment: list[str]):
        """
        sets: list of sets per muscle. sets[i] coresponds to self.muscles[i] YES I COULDVE MADE THIS  A KV PAIR
        equipment: all avaible equipment, or [] if None
        """
        if len(sets) != len(self.muscles) or 0 in sets: raise Exception('Sets must be a list of 4 integers')
        if any(i < 0 for i in sets): raise Exception('All values in sets must be positive')
        
        ciStructure = self.ciStructure
        if ciStructure is None:
            indexTracker = -1
            for muscle,mSets in zip(muscles,sets): #compounds first
                indexTracker += 1
                if mSets > 9:
                    ciStructure.append([muscle,'c',math.ceil(mSets/3)])
                    ciSturcture.append([muscle,'c',math.floor(mSets/3)])
                    sets[indexTracker] -= math.ceil(mSets/3) + math.floor(mSets/3)
                elif mSets > 4:
                    ciStructure.append([muscle,'c',math.ceil(mSets/2)])
                    sets[indexTracker] -= math.ceil(mSets/2)
                else:
                    ciStructure.append([muscle,random.choice(['c','i']),mSets])
            for muscle, mSets in zip(muscles,sets): #isolations
                if mSets != 0:
                    ciStructure.append([muscle,'i',mSets])

        for muscle in ciStructure:
            ci = self.getCompIsol(muscle)
            #not finished