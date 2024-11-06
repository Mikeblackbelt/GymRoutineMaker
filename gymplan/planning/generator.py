import json
import math
import asyncio
import sys
import os
import random
import days

sys.path.append(os.path.abspath(r'C:\Users\mike.mat\Desktop\GymRoutineMaker'))
import gymplan.utility.filePaths as fp
import gymplan.utility.mergeJson as mj

with open(f"{fp.fpPlanData()}\\goals.json",'r') as file:
    goals = json.load(file)

async def getMGroupExercises(section: str, group: str, subgroup: str) -> dict:
    with open(f'{fp.fpExerJson()}\\{section}\\{group}\\{subgroup}.json', 'r') as file:
        exercises = json.load(file)
    mj.logToFile('planlogs.txt',f'{subgroup} exercises found: \n{exercises}')
    return exercises["Exercises"]

async def makeRoutine(goal: str, timePerDay: float, daysPerWeek: int, equipmentPresent: list[str], estTimePerSet: float = 10/2, priorityMuscles: list = None):
    if goal not in goals:
        mj.logToFile('planlogs.txt',f'\nerror, {goal} (input) not in {goals} (valid inputs)\n')
        raise KeyError('Goal not an existing goal, please update goals.json or try a different goal.')
    elif daysPerWeek not in goals[goal]["Day_Options"]:
        mj.logToFile(f'\nerror, {goal} has {goals[goal]["Day_Options"]} as valid day options whereas {daysPerWeek} was inputted\n')
        raise KeyError(f"Invalid number of days, daysPerWeek must be in {goals[goal]['Day_Options']}")

    if goal == 'A' and priorityMuscles is None:
        mj.logToFile('planlogs.txt','\nprioritymuscles updated due to goal type\n')
        priorityMuscles = ['Hamstrings', 'Calves', 'Quads', 'Glutes']
    
    if goal in ['B', 'M', 'H', 'A']:
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
    
    setsPerWeek = math.floor(daysPerWeek*timePerDay / estTimePerSet)
    defaultDirectVolumeRatios = days.defaultDirectVolumeRatios
    newVolumeRatio = defaultDirectVolumeRatios.copy()
    mj.logToFile('planlogs.txt',f'\n{split} split chosen with {setsPerWeek} weekly sets\n')
    if priorityMuscles is not None:
        for muscle in priorityMuscles:
            newVolumeRatio[muscle] = 2 * defaultDirectVolumeRatios[muscle]

        ratioError = abs(1 - sum(newVolumeRatio.values()))
        for mc in newVolumeRatio:
            newVolumeRatio[mc] -= ratioError / len(newVolumeRatio)
    mj.logToFile('planlogs.txt', f'\nVolume ratios:\n\n{newVolumeRatio}\n')
    weeklySetStructure = [[] for _ in range(daysPerWeek)]
    exlist = []

    match split:
        case 'FB':
            for i in range(daysPerWeek):
                for muscle in days.fbMuscles:
                    weeklySetStructure[i].append(math.ceil(setsPerWeek * newVolumeRatio[muscle[2]] / daysPerWeek))
                exlist.append(days.fullConstruct.generate(weeklySetStructure[i], equipmentPresent))
        
        case 'UL':
            for i in range(2):
                for muscle in days.upperMuscles:
                    weeklySetStructure[2*i].append(math.ceil(0.5*newVolumeRatio[muscle[2]]*setsPerWeek))
                for muscle in days.legMuscles:
                    weeklySetStructure[2 * i + 1].append(math.ceil(0.5 * newVolumeRatio[muscle[2]] * setsPerWeek))
                exlist.append(days.upperConstruct.generate(weeklySetStructure[2 * i], equipmentPresent))
                exlist.append(days.legConstruct.generate(weeklySetStructure[2 * i + 1], equipmentPresent))

        case 'ULPPL':
            exlist = [None] * 5
            for muscle in days.upperMuscles:
                weeklySetStructure[0].append(math.ceil(newVolumeRatio[muscle[2]] * setsPerWeek / 3))
            exlist[0] = days.upperConstruct.generate(weeklySetStructure[0], equipmentPresent)

            for i in [1, 4]:
                for muscle in days.legMuscles:
                    weeklySetStructure[i].append(math.ceil(0.5 * newVolumeRatio[muscle[2]] * setsPerWeek))
                exlist[i] = days.legConstruct.generate(weeklySetStructure[i], equipmentPresent)

            for muscle in days.pushMuscles:
                weeklySetStructure[2].append(math.ceil(newVolumeRatio[muscle[2]] * 2 / 3 * setsPerWeek))
            exlist[2] = days.pushConstruct.generate(weeklySetStructure[2], equipmentPresent)

            for muscle in days.pullMuscles:
                weeklySetStructure[3].append(math.ceil(newVolumeRatio[muscle[2]] * 2 / 3 * setsPerWeek))
            exlist[3] = days.pullConstruct.generate(weeklySetStructure[3], equipmentPresent)

        case 'PPL':
            for i in range(2):
                for muscle in days.pushMuscles:
                    weeklySetStructure[3*i].append(math.ceil(newVolumeRatio[muscle[2]] * setsPerWeek / 2))
                for muscle in days.pullMuscles:
                    weeklySetStructure[3*i + 1].append(math.ceil(newVolumeRatio[muscle[2]] * setsPerWeek / 2))
                for muscle in days.legMuscles:
                    weeklySetStructure[3*i + 2].append(math.ceil(newVolumeRatio[muscle[2]] * setsPerWeek / 2))
                exlist.append(days.pushConstruct.generate(weeklySetStructure[3*i], equipmentPresent))
                exlist.append(days.pullConstruct.generate(weeklySetStructure[3*i + 1], equipmentPresent))
                exlist.append(days.legConstruct.generate(weeklySetStructure[3*i + 2], equipmentPresent))
                mj.logToFile('planlogs.txt',f'\nPPL Cycle {i+1} generated succesfully\n')
    mj.logToFile('planlogs.txt',f'\nFinal Exercises: \n\n{exlist}\n') 
    return exlist
    
data = asyncio.run(makeRoutine('M', 60, 6, ['Dumbbell', 'Machine', 'Barbell', 'Bench', 'Incline Bench',"Pull-up bar"]))
print(data)
index = 0
for object in data:
    
    print(f'Day {index + 1}:\n')
    index += 1
    for exercise in object:
        print(f'{list(exercise.keys())[0]} for {list(exercise.values())[0]} sets.\n')
    
