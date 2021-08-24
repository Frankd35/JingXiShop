from django.shortcuts import render

# Create your views here.
def detail_view(request):

    return render(request,'detail_template.html',{})