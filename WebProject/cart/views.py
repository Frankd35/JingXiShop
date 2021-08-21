from django.shortcuts import render

# Create your views here.
def cart_view(request):
    goodsList = []
    return render(request,'shopcar.html', {'goodsList':goodsList})


def collect_view(request):
    return None


def orderplace_view(request):
    return None