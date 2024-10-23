import json

with open("data\goals.json",'r') as file:
    goals = json.load(file)

def makeRoutine(goal: str,time: float,daysPerWeek: int ,estTimePerSet: float = 10/3,priorityMuscles: list = None):
  #handling bad inputs
  if goal not in goals: raise KeyError('Goal not an existing goal, please update goals.json or try a different goal.')
  elif goal not in goals[goal]["Day_Options"]: raise KeyError(f"Invalid number of days, daysPerWeek must be in {goals[goal]["Day_Options"]}")

  if goal == 'A' and priorityMuscles is not None:
     priorityMuscles = ['Hamstrings','Calves','Quads','Glutes']
    
  if goal == 'B':
     """match daysPerWeek:
        case 3:
           trainingVolume = {'Chest':}"""
     
