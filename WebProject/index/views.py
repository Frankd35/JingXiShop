from django.shortcuts import render


# Create your views here.
def index_view(request):
    return render(request, 'index.html')


def index_template_view(request):
    usr_id = int(request.session.get('uid', -1))
    isLogin = usr_id != -1
    return render(request, 'index_template.html', {'isLogin': isLogin})
