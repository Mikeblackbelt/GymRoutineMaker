from pytube import Search
import mergeJson
import filePaths
import json

exerciseList = mergeJson.extract_exercises(mergeJson.merge(filePaths.fpExerJson(),'videos'))

def getExerAm(exerciseName):
    equipmentused = ('with ' + exerciseList[exerciseName]['Equipment'][0]) if len(exerciseList[exerciseName]['Equipment']) > 0 else ''
    videos = Search(f'{exerciseName} {equipmentused} form demonstration')
    return {exerciseName: videos.results[0].watch_url}

exerlist = {}
for exercises in exerciseList.keys():
    vidData = getExerAm(exercises)
    nme = list(vidData.keys())[0]
    exerlist[nme] = vidData[nme]

mergeJson.logToFile('utilLog1.txt', f"Video Data: \n{exerlist}")

with open(f'{filePaths.fpVidJson()}\\videos.json', 'w') as vidFile:
    json.dump(exerlist,vidFile)

"""
exerdict [{'Cable Crunch': 'https://youtube.com/watch?v=3qjoXDTuyOE'}, {'Decline Sit-Up': 'https://youtube.com/watch?v=IINnwHwexkg'}, {'Hanging Leg Raise': 'https://youtube.com/watch?v=Pr1ieGZ5atk'}, {'Ab Wheel Rollout': 'https://youtube.com/watch?v=9ZCoAbI7uX0'}, {'V-Up': 'https://youtube.com/watch?v=nfWQihJo-Mc'}, {'Cable Woodchopper': 'https://youtube.com/watch?v=DoACGlPyQTI'}, {'Dumbbell Side Bend': 'https://youtube.com/watch?v=dL9ZzqtQI5c'}, {'Standing Calf Raise': 'https://youtube.com/watch?v=97NbelB5yvQ'}, {'Seated Calf Raise': 'https://youtube.com/watch?v=3ZRe_QpvRPg'}, {'Smith Machine Calf Raise': 'https://youtube.com/watch?v=1lKjFPrYqf0'}, {'Single Leg Calf Raise': 'https://youtube.com/watch?v=PTn6icEeH3Y'}, {'Calf Press on Leg Press Machine': 'https://youtube.com/watch?v=Hu8i9d_IgpM'}, {'Hip Thrust': 'https://youtube.com/watch?v=xDmFkJxPzeM'}, {'Step-Up': 'https://youtube.com/watch?v=v2GfVnjmY7c'}, {'Glute Bridge': 'https://youtube.com/watch?v=Q_Bpj91Yiis'}, {'Dumbbell Glute Bridge': 'https://youtube.com/watch?v=0kx1QOzhTCQ'}, {'Cable Kickback': 'https://youtube.com/watch?v=IozaC4bS2UY'}, {'Deadlift': 'https://youtube.com/watch?v=r4MzxtBKyNE'}, {'Romanian Deadlift': 'https://youtube.com/watch?v=5zmlnbWb-g4'}, {'Good Morning': 
'https://youtube.com/watch?v=vKPGe8zb2S4'}, {'Glute-Ham Raise': 'https://youtube.com/watch?v=z15C9UZUbss'}, {'Dumbbell Single Leg Romanian Deadlift': 'https://youtube.com/watch?v=lI8-igvsnVQ'}, {'Leg Curl': 'https://youtube.com/watch?v=Orxowest56U'}, {'Lying Leg Curl': 'https://youtube.com/watch?v=vl5nUdE9mWM'}, {'Squat': 'https://youtube.com/watch?v=gcNh17Ckjgg'}, {'Leg Press': 'https://youtube.com/watch?v=VFk3RzndUEc'}, {'Lunge': 'https://youtube.com/watch?v=3TM-vVWuLYE'}, {'Leg Extension': 'https://youtube.com/watch?v=swZQC689o9U'}, {'Chin-Up': 'https://youtube.com/watch?v=KweCZJlwCw0'}, {'Barbell Curl': 'https://youtube.com/watch?v=kwG2ipFRgfo'}, {'Dumbbell Curl': 'https://youtube.com/watch?v=ykJmrZ5v0Oo'}, {'Incline Curl': 'https://youtube.com/watch?v=zPcB2ioexTk'}, {'Concentration Curl': 'https://youtube.com/watch?v=0AUGkch3tzc'}, {'Cable Curl': 'https://youtube.com/watch?v=NFzTWp2qpiE'}, {'Hammer Curl': 'https://youtube.com/watch?v=OPqe0kCxmR8'}, {"Farmer's Walk": 'https://youtube.com/watch?v=8OtwXwrJizk'}, {'Wrist Curl': 'https://youtube.com/watch?v=3VLTzIrnb5g'}, {'Reverse Wrist Curl': 'https://youtube.com/watch?v=ypfd1kaI1AU'}, {'Reverse Curl': 'https://youtube.com/watch?v=hUA-fIpM7nA'}, {'Close-Grip Bench Press': 'https://youtube.com/watch?v=wxVRe9pmJdk'}, {'Skull Crushers': 'https://youtube.com/watch?v=gTrlbuuMufQ'}, {'Tricep Pushdown': 'https://youtube.com/watch?v=2-LAMcpzODU'}, {'Overhead Tricep Extension': 'https://youtube.com/watch?v=-Vyt2QdsR7E'}, {'Overhead Cable Extension': 'https://youtube.com/watch?v=GzmlxvSFE7A'}, {'Pull-Up': 'https://youtube.com/watch?v=p40iUjf02j0'}, {'Chin up': 'https://youtube.com/watch?v=GBcUcATb8RQ'}, {'Lat Pulldown': 'https://youtube.com/watch?v=CAwf7n6Luuc'}, {'Single-Arm Dumbbell Row': 'https://youtube.com/watch?v=gfUg6qWohTk'}, {'Cable Row': 'https://youtube.com/watch?v=CsROhQ1onAg'}, {'Straight-Arm Pulldown': 'https://youtube.com/watch?v=wcVDItawocI'}, {'Dumbbell Pullover': 'https://youtube.com/watch?v=FK4rHfWKEac'}, {'T-Bar Row': 'https://youtube.com/watch?v=TyLoy3n_a10'}, {'Face Pull': 'https://youtube.com/watch?v=ljgqer1ZpXg'}, {'Shrug': 'https://youtube.com/watch?v=_t3lrPI6Ns4'}, {'Bench Press': 'https://youtube.com/watch?v=4Y2ZdHCOXok'}, {'Decline Dumbbell Press': 'https://youtube.com/watch?v=QsYre__-aro'}, {'Dips': 'https://youtube.com/watch?v=W8jXc1zaLuQ'}, {'Push-Ups': 'https://youtube.com/watch?v=IODxDxX7oi4'}, {'Decline Bench Press': 'https://youtube.com/watch?v=LfyQBUKR8SE'}, {'Dumbbell Press': 'https://youtube.com/watch?v=QsYre__-aro'}, {'Cable Crossover': 'https://youtube.com/watch?v=JUDTGZh4rhg'}, {'Chest Fly (Dumbbell)': 'https://youtube.com/watch?v=QENKPHhQVi4'}, {'Pec Deck': 'https://youtube.com/watch?v=eGjt4lk6g34'}, {'Low Cable Fly': 'https://youtube.com/watch?v=cltq5-wzObk'}, {'Incline Bench Press': 'https://youtube.com/watch?v=jPLdzuHckI8'}, {'Incline Dumbbell Press': 'https://youtube.com/watch?v=IP4oeKh1Sd4'}, {'Decline Push-Ups': 'https://youtube.com/watch?v=5QFjmotLfW4'}, {'Incline chest Press': 'https://youtube.com/watch?v=I70W7ZLBWiQ'}, {'Incline Cable Fly': 'https://youtube.com/watch?v=LGDCjwO-hFg'}, {'Dumbbell Fly (Incline)': 'https://youtube.com/watch?v=ajdFwa-qM98'}, {'Overhead Press': 'https://youtube.com/watch?v=F3QY5vMz_6I'}, {'Seated Dumbbell Press': 'https://youtube.com/watch?v=qEwKCR5JCog'}, {'Seated Barbell Press': 'https://youtube.com/watch?v=oBGeXxnigsQ'}, {'Machine Shoulder Press': 'https://youtube.com/watch?v=3R14MnZbcpw'}, {'Front Raise (Dumbbell)': 'https://youtube.com/watch?v=-t7fuZ0KhDA'}, {'Cable Front Raise': 'https://youtube.com/watch?v=vtH93qBItdk'}, {'Rear Delt Fly (Dumbbell)': 'https://youtube.com/watch?v=EA7u4Q_8HQ0'}, {'Cable Rear Delt Fly': 'https://youtube.com/watch?v=er15V96hG5U'}, {'Reverse Pec Deck': 'https://youtube.com/watch?v=6cHY60y7QRU'}, {'Lateral Raise': 'https://youtube.com/watch?v=OuG1smZTsQQ'}, {'Cable Lateral Raise': 'https://youtube.com/watch?v=Z5FA9aq3L6A'}] 
print(exerlist)
"""