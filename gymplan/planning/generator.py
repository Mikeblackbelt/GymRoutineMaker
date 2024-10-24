import json
import math
import asyncio

with open("data\goals.json",'r') as file:
    goals = json.load(file)

#WARNING: VERY POORLY WRITTEN FUNCTION lmao
async def makeRoutine(goal: str,timePerDay: float,daysPerWeek: int ,estTimePerSet: float = 10/3,priorityMuscles: list = None):
  #handling bad inputs
  if goal not in goals: raise KeyError('Goal not an existing goal, please update goals.json or try a different goal.')
  elif goal not in goals[goal]["Day_Options"]: raise KeyError(f"Invalid number of days, daysPerWeek must be in {goals[goal]["Day_Options"]}")
  #everythig else
  if goal == 'A' and priorityMuscles is not None:
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
        for muscle in pushMuscles:
           weeklySetStructure[2][muscle] = 0.6*newVolumeRatio[muscle]*setsPerWeek
        for muscle in pullMuscles:
           weeklySetStructure[2][muscle] = 0.4*newVolumeRatio[muscle]*setsPerWeek 
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
             



           
        

    
            
     
           
     
