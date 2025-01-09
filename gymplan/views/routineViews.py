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

def addRView(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')
    
    userdata = UDF.getUserData(username=username)
    user_settings = userdata.get('settings', {})
    darkMode = user_settings.get('dark_mode', False)

    request.session['goal'] = None
    if request.method == 'POST':
        selected_goal = request.POST.get('goal')
        if not selected_goal:
            return render(request, 'routineGenStart.html', {
                'Username': username,
                'user_data': userdata,
                'dark_mode': darkMode,
                'goals': getGoals(),
                'error': 'Please select a goal.',
            })
        return redirect('routine_gen_main', selected_goal=selected_goal)

    return render(request, 'routineGenStart.html', {
        'Username': username,
        'user_data': userdata,
        'dark_mode': darkMode,
        'goals': getGoals(),
    })

def rgm_View(request, goal_key):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    userdata = UDF.getUserData(username=username)
    user_settings = userdata.get('settings', {})
    darkMode = user_settings.get('dark_mode', False)

    goals = getGoals()
    selected_goal_data = goals.get(goal_key[0], {}) 
    available_days = selected_goal_data.get('Day_Options', range(2,6))  # Default options

    return render(request, 'routineGenMain.html', {
        'Username': username,
        'user_data': userdata,
        'dark_mode': darkMode,
        'selected_goal': goal_key,
        'available_days': available_days,
    })

def viewRoutine(request, routineID):
    return 
    
