from django.http import HttpResponse

# The 'index' view that is referenced in urls.py
def index(request):
    return HttpResponse("Welcome to the Gym Plan app!")

def 