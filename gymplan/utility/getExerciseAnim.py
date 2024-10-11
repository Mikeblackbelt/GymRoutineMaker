from pytube import Search
import mergeJson
import filePaths


exerciseList = mergeJson.extract_exercises(mergeJson.merge(filePaths.fpExerJson()))

def getExerAm(savepath,exerciseName):
    equipmentused = ('with' + exerciseList[exerciseName]['Equipment'][0]) if len(exerciseList[exerciseName]['Equipment']) > 0 else ''
    videos = Search(f'{exerciseName} {equipmentused} form demonstration')
    return {exerciseName: videos.results[0].watch_url}

exerlist = []
for exercises in exerciseList.keys():
    exerlist.append(getExerAm(f"{filePaths.fpExerVid()}\\{exercises}",exercises))

print(exerlist)