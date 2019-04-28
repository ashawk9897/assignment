from django.shortcuts import render
from django.contrib import messages
# Create your views here.
def collapse(request):
    modified_text=''
    template = 'index.html'
    file=''
    mt_array=[]
    if request.method=='POST':
        try:
            file = request.FILES['file']
            data = file.read().decode("utf-8")
        except:
            messages.error(request, 'Oops, Please upload a valid text file')
            return render(request,template_name=template,context={'modified_text':modified_text})

        star_array = [0]
        indenter = '.'
        previous_line = ''
        mt_array = []
        for line in data.splitlines():
            #print(line)
            if not len(line.strip()):
                #print(line,'continueing')
                continue
            if line.startswith('*'):
                if previous_line:
                    mt, previous_line = indent_finder(line, previous_line, indenter)
                    mt_array.append(mt)
                mt, star_array, line_len = stars(line, star_array)
                mt_array.append(mt)
                previous_line = ''
                continue
            elif line.startswith(indenter):
                if previous_line == '':
                    previous_line = line
                    continue
                mt, previous_line = indent_finder(line, previous_line, indenter)
            else:
                previous_line_len=len(previous_line) - len(previous_line.lstrip(indenter))
                previous_line = previous_line+'\n'+' ' * (previous_line_len+3) + line
                continue
            mt_array.append(mt)
        if previous_line:
            previous_text_space = len(previous_line) - len(previous_line.lstrip(indenter))
            mt_array.append(' ' * (previous_text_space+1) + '-' + previous_line[previous_text_space:])

        # mt_array.append()
        mt_array = '\n'.join(mt_array)
        #print(mt_array)


    return render(request,template_name=template,context={'modified_text':mt_array,'file':file})


def stars(text, star_array):
    star_count = len(text) - len(text.lstrip('*'))
    if star_count > len(star_array):
        star_array.append(1)
    elif star_count < len(star_array):
        star_array = star_array[:star_count]
        star_array[-1] = star_array[-1] + 1
    else:
        star_array[-1] = star_array[-1] + 1
    #print(star_count)
    position = '.'.join([str(a) for a in star_array])
    modified_text = position + text[star_count:]

    return [modified_text, star_array, star_count]


def indent_finder(text, previous_text, indenter):
    text_space = len(text) - len(text.lstrip(indenter))
    modified_text = ''
    previous_text_space = len(previous_text) - len(previous_text.lstrip(indenter))
    if previous_text_space >= text_space:
        coll_type = '-'
        modified_text = ' ' * (previous_text_space+1) + coll_type + previous_text[previous_text_space:]
        previous_text = text
    elif previous_text_space < text_space:
        coll_type = '+'
        modified_text = ' ' * (previous_text_space+1) + coll_type + previous_text[previous_text_space:]
        previous_text = text

    return [modified_text, previous_text]

def jsview(request):
    modified_text = ''
    template = 'indexjs.html'
    file = ''
    mt_array=[]
    return render(request, template_name=template, context={'modified_text': mt_array, 'file': file})