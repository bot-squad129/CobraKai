from django.shortcuts import render
from sudoku_solver import print_karo


def index(request):
    return render(request,template_name="index.html")

def output(request):
    print(request.GET.get("img"))
    data=print_karo(request.GET.get("img"))
    return render(request=request,template_name="output.html",context={"data":data})
