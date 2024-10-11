from pytube import YouTube,Search
import mergeJson
import filePaths

exerciseList = mergeJson.extract_exercises(mergeJson.merge(filePaths.fpExerJson()))

def getExerAm(savepath,exerciseName):
    equipmentused = exerciseList[exerciseName]['Equipment'][0]
    videos = Search(f'{exerciseName} with {equipmentused} form demonstration')

    for video in videos.results:
        try:
            # Create a YouTube object
            yt = YouTube(video.watch_url)
            
            # Select the highest resolution stream available
            stream = yt.streams.get_highest_resolution()
            
            # Download the video to the specified path
            stream.download(output_path=savepath)
            print(f'Downloaded: {yt.title}')
        
        except Exception as e:
            print(f'Error downloading {video.title}: {e}')

getExerAm(f'{filePaths.fpExerVid}\\{'Bench_Press'}', "Bench Press")