from django.shortcuts import render
from django.contrib import messages
# Create your views here.
def collapse(request):
    modified_text=''
    template = 'index.html'
    file=''
    indenter='.'
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
        line_number=1

        for line in data.splitlines():
            # print('----------------------------------------------')
            # print(line,previous_space,next_space)
            if line.startswith('*'):
                star_count=len(line)-len(line.lstrip('*'))
                if star_count>1:
                    str_line_number = str(line_number)
                    for i in range(1,star_count):
                        sub_line_number = 1
                        str_line_number=str_line_number+'.'+str(sub_line_number)
                    sub_line_number += 1
                else:
                    str_line_number=str(line_number)
                    line_number += 1
                if previous_space != 0:
                    modified_text.append(' ' * (previous_space+1) + '-' + previous_line.lstrip(indenter))
                modified_text.append(str_line_number + line[1:])

                previous_line=''
                previous_space=0
                next_space = 0
                continue

            if not len(line.lstrip()):
                #print('continue')
                continue
            if previous_line=='':
                previous_line=line
                previous_space = len(previous_line) - len(previous_line.lstrip(indenter))
                continue
            if line.startswith('.'):
                next_space = len(line) - len(line.lstrip(indenter))
            if(previous_space<next_space):
                adder = '+'
                if previous_space==0:
                    previous_line = line
                    previous_space = next_space
                    continue
                modified_text.append(' '* (previous_space+1) +adder+previous_line.lstrip(indenter))
            else:
                adder = "-"
                previous_space = len(previous_line) - len(previous_line.lstrip(indenter))
                modified_text.append(' '* (previous_space+1) +adder +previous_line.lstrip(indenter) )
            # else:
            #     modified_text.append(' '*previous_space+previous_line.lstrip(indenter))
            previous_line=line
            previous_space=next_space
            adder = "-"
        if previous_line.startswith('.'):
            indenter = '.'
        else:
            indenter = ' '
        #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',previous_line,indenter,'aaaaaaa',previous_line.lstrip(indenter))
        #print(' '* (previous_space+1) +adder+previous_line.lstrip(indenter))
        modified_text.append(' '* (previous_space+1) +adder+previous_line.lstrip(indenter))
        modified_text='\n'.join(modified_text)

    return render(request,template_name=template,context={'modified_text':modified_text,'file':file})

