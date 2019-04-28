star_array=[0]
previous_line = ''
mt_array = []
indenter='.'
function modifier()
{
   var output= document.querySelector("#indent p");
   console.log(output)
    input = document.getElementById('fileToLoad');
    if (!input.files) {
      alert("This browser doesn't seem to support the `files` property of file inputs.");
    }

    else {
      file = input.files[0];
      reader = new FileReader();
      reader.onload = function(progressEvent){
        var lines = this.result.split('\n');
        for(var line = 0; line < lines.length; line++){
              //console.log(lines[line]);
            if (lines[line].trim().length==0)
                continue
            if (lines[line].startsWith("*")){

                if (previous_line){
                        //console.log('before star',lines[line]);
                        indent_line= indent_finder(lines[line], previous_line, indenter)
                        previous_line=indent_line[1]
                        output.innerHTML+= indent_line[0]
                        }
                star_line=stars(lines[line],star_array)
                previous_line = ''
                output.innerHTML+= star_line[0]
                continue;
                }
            else if (lines[line].startsWith(indenter)){
                    if (previous_line == ''){
                        previous_line = lines[line]
                        continue;
                        }
                    indent_line= indent_finder(lines[line], previous_line, indenter)
                    previous_line=indent_line[1]
                    output.innerHTML+= indent_line[0]
                    }
            else{
                previous_line_len=previous_line.match(/^(\.+)/)[1].length
                previous_line = previous_line+'\n'+' '.repeat(previous_line_len+3) + lines[line]
                continue
                }
        }
        if (previous_line){
            previous_text_space =previous_line.match(/^(\.+)/)[1].length
            output.innerHTML+=' '.repeat(previous_text_space+1) + '-' + previous_line.slice(previous_text_space,)
            }

        }
  };
  reader.readAsText(file);
    }


function stars(text,star_array){
//    console.log(text.match(/^(\*+)/)[1])
    star_count =text.match(/^(\*+)/)[1].length
//    console.log(star_count,text)
    if (star_count > star_array.length){
        star_array.push(1)
        }
    else if (star_count < star_array.length){
        star_array = star_array.slice(0,star_count)
        star_array[star_array.length-1]  += 1
        }
    else
         star_array[star_array.length-1]  += 1

    position = star_array.join('.');
    modified_text = position + text.slice(star_count,)
//    console.log(modified_text)
    return [modified_text, star_array, star_count]

}

function indent_finder(text, previous_text, indenter){
    console.log('--------------------',text,previous_text)
    try{
        text_space =text.match(/^(\.+)/)[1].length
        }
    catch{
        console.log('ERROR previous_text_space',previous_text)
        text_space=0
    }
    modified_text = ''
    try{
        previous_text_space =previous_text.match(/^(\.+)/)[1].length
        }
    catch{
        console.log('ERROR previous_text_space',previous_text)
        previous_text_space=0
    }
    if (previous_text_space >= text_space){
        coll_type = '-'
        }
    else if (previous_text_space < text_space){
        coll_type = '+'
        }
    modified_text = ' '.repeat(previous_text_space+1) + coll_type + previous_text.slice(previous_text_space,)
    previous_text = text
    console.log('modified_text',modified_text)
    return [modified_text, previous_text]

}