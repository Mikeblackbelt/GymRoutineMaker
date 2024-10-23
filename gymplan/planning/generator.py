`import json
import math

with open("data\goals.json",'r') as file:
    goals = json.load(file)

def makeRoutine(goal: str,timePerDay: float,daysPerWeek: int ,estTimePerSet: float = 10/3,priorityMuscles: list = None):
  #handling bad inputs
  if goal not in goals: raise KeyError('Goal not an existing goal, please update goals.json or try a different goal.')
  elif goal not in goals[goal]["Day_Options"]: raise KeyError(f"Invalid number of days, daysPerWeek must be in {goals[goal]["Day_Options"]}")

  if goal == 'A' and priorityMuscles is not None:
     priorityMuscles = ['Hamstrings','Calves','Quads','Glutes']
    
  if goal in ['B','M','H']:
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
  elif goal == 'A':
        split = 'A'
   
   setsPerWeek = math.floor(daysPerWeek*timePerDay/estTimePerSet)
   
""""   volumeRatios = [
      ('chest',0.15), #12 sets of 80 sets/week
      ('back',0.2), #16
      ('frontdelts',0.05), #4
      ('sidedelts',0.1), #8
      ('reardelts',0.05), #4
      ('biceps',0.125), #10
      ('triceps',0.1), #8
      ('calves',0.075), #6
      ('quads',0.15) #
   ]""""
   if priorityMuscles is not None:
     for muscles in priorityMuscles:
        """weeklyVolume = setsPerWeek/ """
     
           
     
`