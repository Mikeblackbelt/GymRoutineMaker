import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .utility import sendmsg
from .utility import filePaths as fp
from .userDataFuncs import userData as UDF
from django.views.decorators.csrf import csrf_protect


def getGoals():
    with open(r"C:\Users\mike.mat\Desktop\GymRoutineMaker\gymplan\planning\data\goals.json",'r') as f:
        return json.load(f)

def login_view(request):
    """Handles user login."""
    if request.method == "POST":
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        try:
            if UDF.hauth2(username, password):
                userdata = UDF.getUserData(username=username)
                request.session['username'] = username

                if not userdata['settings'].get('2auth', False):
                    return redirect(reverse('dashboard'))

                else:
                    request.session['makingAccount'] = False  
                    try:  del request.session['OTP'] 
                    except: pass
                    return redirect(reverse('emailVerify'))
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})

        except ValueError as e:
            return render(request, 'login.html', {'error': str(e)})

    return render(request, 'login.html')


def signup_view(request):
    """Handles user signup."""
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        try:
            new_user = UDF.User(name=name, username=username, password=password, email=email)
            new_user.upload()
            request.session['makingAccount'] = True  
            request.session['username'] = username
            try:  del request.session['OTP'] 
            except: pass

            return redirect(reverse('emailVerify')) if email else redirect(reverse('login'))
                
        except Exception as e:
            return render(request, 'signup.html', {"error": str(e)})

    return render(request, 'signup.html')


def emailVerify_view(request):
    """Handles email verification."""
    making_account = request.session.get('makingAccount', False)  
    username = request.session.get('username', False)
    if username:
        userdata = UDF.getUserData(username=username)
        
        if 'email' not in userdata or userdata['email'] is None:
            return HttpResponse("Error: Email not found for this user", status=400)

        #print(request.session['OTP'])
        if 'OTP' not in request.session:  
            OTP = sendmsg.sendOTP(userdata['email'])
            request.session['OTP'] = OTP
        
    else:
        return HttpResponse("Error: Username not found in session", status=400)

    if request.method == "POST":
        OTPattempt = request.POST.get('OTP')
        
        if not OTPattempt:
             return render(request, 'emailVerify.html', {
                "makingAccount": making_account,
                "username": username,
                "error": "Please enter the OTP."
            })

        if OTPattempt == str(request.session.get('OTP')):
            del request.session['OTP'] 
            request.session['verified'] = True
            if not making_account: request.session['username'] = username
            else: del request.session['username']
            return redirect(reverse('login')) if making_account else redirect(reverse('dashboard'))
        
        else:
            return render(request, 'emailVerify.html', {
                "makingAccount": making_account,
                "username": username,
                "error": "Invalid OTP. Please try again."
            })


    return render(request, 'emailVerify.html', {"makingAccount": making_account, 'username': username})

#c
def dashboard_view(request):
    username = request.session['username'] # Assuming user ID is mapped to JSON
    user_data = UDF.getUserData(username=username)
 
    if not user_data:
        return HttpResponse("User not found", status=404)

    user_settings = user_data.get('settings', {})
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

def addRView(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    userdata = UDF.getUserData(username=username)
    user_settings = userdata.get('settings', {})
    darkMode = user_settings.get('dark_mode', False)

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

def rgm_View(request, selected_goal):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    userdata = UDF.getUserData(username=username)
    user_settings = userdata.get('settings', {})
    darkMode = user_settings.get('dark_mode', False)

    goals = getGoals()
    selected_goal_data = goals.get(selected_goal, {})
    available_days = selected_goal_data.get('Day_Options', range(2,6))  # Default options

    return render(request, 'routineGenMain.html', {
        'Username': username,
        'user_data': userdata,
        'dark_mode': darkMode,
        'selected_goal': selected_goal,
        'available_days': available_days,
    })

