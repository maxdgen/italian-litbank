import argparse
import os

# Truncate the texts contained in "input_folders_name" to texts with 2100 words and save them in "output_folders_name"
def truncate_texts(input_folders_name: str, output_folders_name: str):
    separators = ["'", '"', '.', ':', ',', ';', '!', '?', '-', '—', ' ', '\n']
    for filename in os.listdir(input_folders_name):
        if filename[-3 :] == 'txt':
            with open(input_folders_name + '\\' + filename, 'rt', encoding = 'utf-8') as file:
                text = file.read()
                
                words_num = 0
                i = 0
                while i < len(text) and words_num < 2100:
                    if text[i] in separators:
                        if i != 0 and text[i - 1] not in separators:
                            words_num += 1
                    i += 1
            
            with open(output_folders_name + '\\' + filename, 'wt', encoding = 'utf-8') as new_file:
                new_file.write(text[0 : i])

# Widen the texts contained in "input_folders_name" and save the results in "output_folders_name"
def widen_texts(input_folders_name: str, output_folders_name: str):
    for filename in os.listdir(input_folders_name):
        if filename[-3 :] == 'txt':
            with open(input_folders_name + '\\' + filename, 'rt', encoding = 'utf-8') as file:
                text = file.read()
                
                # Replace and remove particular letters
                text = text.replace("’", "'").replace("ʼ", "'").replace('“', '"').replace('„', '"')
                text = text.replace('«', '').replace('»', '').replace('_', '')
                text = text.replace('\n', ' ')
                found = text.find('[')
                while found != -1:
                    text = text[0 : found] + text[(text.find(']') + 1) : len(text)]
                    found = text.find('[')
                
                # Remove extra whitespace
                i = 0
                while i < len(text):
                    if text[i] == ' ':
                        j = i + 1
                        while j != len(text) and text[j] == ' ':
                            j += 1
                        if j != (i + 1):
                            text = text[0 : (i + 1)] + text[j : len(text)]
                        i = j - 1
                    i += 1
                
                # Widen the texts
                separators1 = [',', ';', ':', "'", '(', ')']
                separators2 = ['"', '?', '!']
                separators3 = ['-', '—']
                i = 0
                while i < len(text):
                    if text[i] in separators1:
                        if text[i - 1] != ' ':
                            text = text[0 : i] + ' ' + text[i : len(text)]
                            i += 1
                        if text[i + 1] != ' ':
                            text = text[0 : (i + 1)] + ' ' + text[(i + 1) : len(text)]
                            i += 1
                    elif text[i] in separators2:
                        if text[i - 1] != ' ':
                            text = text[0 : i] + ' ' + text[i : len(text)]
                            i += 1
                        if (i + 1) == len(text):
                            text += '\n'
                        elif text[i + 1] == ' ':
                            if text[i + 2] not in separators1:
                                text = text[0 : (i + 1)] + '\n' + text[(i + 2) : len(text)]
                                i += 1
                        elif text[i + 1] not in separators1:
                            text = text[0 : (i + 1)] + '\n' + text[(i + 1) : len(text)]
                            i += 1
                        elif text[i + 1] in separators1:
                            text = text[0 : (i + 1)] + ' ' + text[(i + 1) : len(text)]
                            i += 1
                    elif text[i] in separators3:
                        if text[i - 1] != ' ' and text[i - 1] != '\n':
                            text = text[0 : i] + ' ' + text[i : len(text)]
                            i += 1
                        j = i + 1
                        while text[j] in separators3:
                            j += 1
                        if text[j] != ' ':
                            text = text[0 : j] + ' ' + text[j : len(text)]
                        i = j
                    elif text[i] == '.':
                        if text[i - 1] != ' ':
                            text = text[0 : i] + ' ' + text[i : len(text)]
                            i += 1
                        j = i + 1
                        while j != len(text) and text[j] == '.':
                            j += 1
                        if j == len(text):
                            text += '\n'
                        elif j == (i + 1):
                            if text[j] == ' ':
                                text = text[0 : j] + '\n' + text[(j + 1) : len(text)]
                            else:
                                text = text[0 : j] + '\n' + text[j : len(text)]
                        else:
                            if text[j] != ' ':
                                text = text[0 : j] + ' ' + text[j : len(text)]
                        i = j
                    i += 1
            
            new_name = output_folders_name + '\\' + filename[0 : -4] + '_brat.txt'
            with open(new_name, 'wt', encoding = 'utf-8') as new_file:
                new_file.write(text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    '''
    parser.add_argument('-i', '--input', help = 'folder where the texts to truncate are located', required = True)
    parser.add_argument('-o', '--output', help = 'folder where the texts truncated will be located', required = True)
    
    args = vars(parser.parse_args())
    
    truncate_texts(args['input'], args['output'])
    
    '''
    parser.add_argument('-i', '--input', help = 'folder where the texts to widen are located', required = True)
    parser.add_argument('-o', '--output', help = 'folder where the texts widened will be located', required = True)
    
    args = vars(parser.parse_args())
    
    widen_texts(args['input'], args['output'])