import json

with open("goals.json",'r') as file:
    goals = json.load(file)

def makeRoutine(goal: str,time: float,daysPerWeek: float ,estTimePerSet: float = 10/3,priorityMuscles: list = None):
  #handling bad inputs
  if goal not in goals: raise KeyError('Goal not an existing goal, please update goals.json or try a different goal.')
  elif goal not in goals[goal]["Day_Options"]: raise KeyError

  return None
     
     
     