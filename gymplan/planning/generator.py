import json
import math
import asyncio
import sys
import os
import random
sys.path.append(os.path.abspath(r'C:\Users\mike.mat\Desktop\GymRoutineMaker'))

import gymplan.utility.filePaths as fp

with open(f"{fp.fpPlanData()}\\goals.json",'r') as file:
    goals = json.load(file)

async def getMGroupExercises(section:str,group:str,subgroup: str) -> dict:
   with open(f'{fp.fpExerJson()}\\{section}\\{group}\\{subgroup}.json','r') as file:
      exercises = json.load(file)
   return exercises["Exercises"]
"""
async def pushR(sets: list[int], equipment: list[str]):
    if len(sets) != 4:
        raise Exception("sets must be a list of exactly 4 integers")
    
    # Define muscle groups for a push day
    muscle_groups = ["upperchest","lowerchest", "frontdelts", "sidedelts", "triceps"]
    coresp = ['chest','chest','shoulders','shoulders','arms']
    exerciseList = []
    i=0
    for idx, muscle in enumerate(muscle_groups):
        # Fetch exercises for the specific muscle
        exercises = await getMGroupExercises('upperbody',coresp[i], muscle) 
        i += 1 #this was improvised 
        # Filter exercises by equipment availability and type (compound/isolation)
        compound_exercises = [
           # """exercises[ex] for ex in exercises["Compound"] if exercises["Compound"][ex]["Equipment"] in equipment"""
        ]
        isolation_exercises = [
           # ex for ex in exercises["Isolation"] if exercises["Isolation"][ex]["Equipment"] in equipment
        ]
        
        for ex in exercises['Compound']:
         if exercises["Compound"]['ex']['Equipment']
        # Randomly select exercises, preferring one from each category if available
        chosen_exercises = []
        if compound_exercises:
            chosen_exercises.append(random.choice(compound_exercises))
        if isolation_exercises:
            chosen_exercises.append(random.choice(isolation_exercises))
        print(f'{compound_exercises},{isolation_exercises}')
        # Assign the specified sets to each selected exercise
        for ex in chosen_exercises:
            exerciseList.append({
                "exercise": ex["name"],
                "sets": sets[idx],
                "muscle": muscle,
                "type": "compound" if ex in compound_exercises else "isolation",
                "equipment": ex["equipment"]
            })
            
    
    return exerciseList

result = asyncio.run(pushR([4, 4, 4, 4], ["Incline Bench", 'Bench', 'Machine', "Cable", "Barbell"]))
print(result)
"""

#WARNING: VERY POORLY WRITTEN FUNCTION lmao
async def makeRoutine(goal: str,timePerDay: float,daysPerWeek: int ,equimentPresent: list[str], estTimePerSet: float = 10/3,priorityMuscles: list = None):
  #handling bad inputs
  if goal not in goals: raise KeyError('Goal not an existing goal, please update goals.json or try a different goal.')
  elif daysPerWeek not in goals[goal]["Day_Options"]: raise KeyError(f"Invalid number of days, daysPerWeek must be in {goals[goal]['Day_Options']}")

  #everythig else
  if goal == 'A' and priorityMuscles is None:
     priorityMuscles = ['Hamstrings','Calves','Quads','Glutes']
    
  if goal in ['B','M','H','A']:
     match daysPerWeek:
        case 2 | 3: 
           split = 'FB'
        case 4:
           split = 'UL'
        case 5:
           split = 'ULPPL'
        case 6:
           split = 'PPL'
  elif goal == "P":
        split = 'PL'

  setsPerWeek = math.floor(daysPerWeek*timePerDay/estTimePerSet)
   
  defaultDirectVolumeRatios = {
    'chest': 0.12, 
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

  newVolumeRatio = defaultDirectVolumeRatios

  if priorityMuscles is not None:
     for muscles in priorityMuscles:
       newVolumeRatio[muscles] = 2*defaultDirectVolumeRatios[muscles]
      
     ratioError = abs(1 - sum(list(newVolumeRatio.values())))
     for mc in newVolumeRatio:
         newVolumeRatio[mc] -= ratioError/len(newVolumeRatio)
   
  weeklySetStructure = [] 
  pushMuscles = ['chest','frontdelts','sidedelts','triceps']
  pullMuscles = ['lats','midback','reardelts','biceps']
  lowerMuscles = ['calves','quads','hamstrings','glutes','abs','obliques']

  for i in range(daysPerWeek):
      weeklySetStructure[i] = []

  match split: #WARNING: this code is very poorly written; i dont really care and i know the possible optimizations but im not rewriting this to save a few lines assuming it works fine sorryyy
     case 'FB':
          for muscle in newVolumeRatio:
             weeklySetStructure[i].append(setsPerWeek*newVolumeRatio[muscle]/daysPerWeek)
     case 'UL':
        #upper, push focused
        for muscle in pushMuscles:
           weeklySetStructure[0][muscle] = 0.6*newVolumeRatio[muscle]*setsPerWeek
        for muscle in pullMuscles:
           weeklySetStructure[0][muscle] = 0.4*newVolumeRatio[muscle]*setsPerWeek 
         #upper pull focused
        for muscle in pullMuscles:
           weeklySetStructure[2][muscle] = 0.4*newVolumeRatio[muscle]*setsPerWeek 
        for muscle in pushMuscles:
           weeklySetStructure[2][muscle] = 0.6*newVolumeRatio[muscle]*setsPerWeek
         #lower
        for i in range(2):
          for muscle in lowerMuscles:
            weeklySetStructure[2*i+1][muscle] = 0.5*newVolumeRatio[muscle]*setsPerWeek
     case 'ULPPL':
         #upper
         for muscle in pushMuscles+pullMuscles:
            weeklySetStructure[0][muscle] = newVolumeRatio[muscle]*setPerWeek/3
         #lower
         for i in [1, 4]:
            for muscle in lowerMuscles:
               weeklySetStructure[i][muscle] = 0.5*newVolumeRatio[muscle] * setsPerWeek
         #push
         for muscle in pushMuscles:
            weeklySetStructure[2][muscle] = newVolumeRatio[muscle] * 2/3 * setsPerWeek
         #pull
         for muscle in pullMuscles:
            weeklySetStructure[3][muscle] = newVolumeRatio[muscle] * 2/3 * setsPerWeek
     case 'PPL':
         for i in range(2):
            for muscle in pushMuscles:
               weeklySetStructure[i][muscle] = newVolumeRatio[muscle] * 1/2 * setsPerWeek
            for muscle in pullMuscles:
                  weeklySetStructure[i+1][muscle] = newVolumeRatio[muscle] * 1/2 * setsPerWeek
            for muscle in lowerMuscles:
                  weeklySetStructure[i+2][muscle] = newVolumeRatio[muscle] * 1/2 * setsPerWeek
     case 'PL':
         powerlifts =  ['Squat','Bench','Deadlift']
         if daysPerWeek % 3 == 0:
           for i in range(daysPerWeek):
             weeklySetStructure[i] = powerlifts[i % 3]
         else: # daysPerWeek == 4
            for i in range(3):
               weeklySetStructure[i] = powerlifts[i % 3]
            weeklySetStructure[3] = 'ac'
             
"""if split != 'PL':
      for days in weeklySetStructure:
         if daysPerWeek >= 4: #UL, ULPPL, PPL
            if 'chest' in days and chest''"""
            



           
        

    
            
     
           
     
