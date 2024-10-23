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

    
            
     
           
     
`