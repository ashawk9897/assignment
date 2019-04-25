from django.shortcuts import render
from django.contrib import messages
# Create your views here.
def collapse(request):
    modified_text=''
    template = 'index.html'
    file=''
    if request.method=='POST':
        try:
            file = request.FILES['file']
            data = file.read().decode("utf-8")
        except:
            messages.error(request, 'Oops, Please upload a valid text file')
            return render(request,template_name=template,context={'modified_text':modified_text})
        modified_text=[]
        previous_line=''
        previous_space=0
        next_space=0
        next_line=''
        adder='-'
        for line in data.splitlines():
            if previous_line=='':
                previous_line=line
                previous_space = len(previous_line) - len(previous_line.lstrip())
                continue
            next_space=len(line) -len(line.lstrip())
            if(previous_space<next_space):
                adder='+'
                modified_text.append(adder+previous_line)
            else:

                previous_space = len(previous_line) - len(previous_line.lstrip())
                modified_text.append(adder + previous_line )
            previous_line=line
            previous_space=next_space
            adder = "-"
        modified_text.append(adder+previous_line)
        modified_text='\n'.join(modified_text)

    return render(request,template_name=template,context={'modified_text':modified_text,'file':file})

