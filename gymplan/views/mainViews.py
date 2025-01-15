import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from gymplan.utility import sendmsg
from gymplan.utility import filePaths as fp
from gymplan.userDataFuncs import userData as UDF
from django.views.decorators.csrf import csrf_protect


def getGoals():
    with open(r"C:\Users\mike.mat\Desktop\GymRoutineMaker\gymplan\planning\data\goals.json",'r') as f:
        return json.load(f)

def dashboard_view(request):
    username = request.session['username'] # Assuming user ID is mapped to JSON
    user_data = UDF.getUserData(username=username)
 
    if not user_data:
        return HttpResponse("User not found", status=404)

    user_settings = user_data.get('settings', {})
    print(user_settings)
    darkMode = user_settings['dark_mode']

    routines = user_data.get("routines", [])
    #print(routines)
    routine_details = [] 

    with open(fp.fpRoutineJson(), 'r') as file:
        routine_data = json.load(file)  
    
    for routine in routines:
        routine_id = list(routine.keys())[0]
        routine_name = list(routine.values())[0]
        routine_info = routine_data.get(routine_id, {})
        if routine_info:
            total_sets = sum(sum(routine_info[day][exercise]["Sets"] for exercise in routine_info[day]) for day in routine_info)
            daily_est_time = round(4*total_sets/len(routine_info))
            daily_sets = round(total_sets/len(routine_info))


        routine_details.append({
            "id": routine_id,
            "name": routine_name,
            "details": routine_info,
            "setsPerDay": daily_sets,
            'timePerDay': daily_est_time
        }) 
 
    return render(request, 'homepage.html', { 
        'Username': username,
        'user_data': user_data,
        'routine_details': routine_details,
        'dark_mode': darkMode
    })

@csrf_protect
def settingView(request):
    """Handles setting page"""
    username = request.session.get('username')
    if not username:
        return redirect('login')

    userdata = UDF.getUserData(username=username)
    user_settings = userdata.get('settings', {})
    darkMode = user_settings.get('dark_mode', False)
    print(f'Dark_Mode: {darkMode}')
    if request.method == 'POST':
        # Safeguard nested keys
        userdata['settings']['privacy_settings'] = userdata['settings'].get('privacy_settings', {})
        userdata['settings']['2auth'] = '2auth' in request.POST
        userdata['settings']['dark_mode'] = 'dark_mode' in request.POST
        userdata['settings']['privacy_settings']['logEmail'] = 'logEmail' in request.POST

        print("POST data received:", request.POST)  # Debugging
        print("User settings before update:", userdata['settings'])  # Debugging

        UDF.update_settings(userdata['settings'], username=username)

        userdata = UDF.getUserData(username=username)
        darkMode = userdata['settings'].get('dark_mode', False)  # Refresh after POST
        print("Reloaded user data:", userdata)  # Debugging

    return render(request, 'settings.html', { 
        'Username': username,
        'user_data': userdata,
        'dark_mode': darkMode,  # Now reflects the updated value
    })