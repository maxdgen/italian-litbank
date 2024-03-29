import argparse
import os

# Class to manage annotations
class Annotations:
    def __init__(self, jsonl_file: str):
        self.texts = {}
        
        with open(jsonl_file, 'rt', encoding = 'utf-8') as jsonl:
            for line in jsonl.readlines():
                # Get the id from the jsonl
                i = 0
                j = (i + 6)
                text_id = 0
                if line[i : j] == '{"id":':
                    i = j
                    while (line[j] != ','):
                        j += 1
                    text_id = int(line[i : j])
                
                # Get the text from the jsonl
                i = (j + 1)
                j = (i + 7)
                text = ''
                if line[i : j] == '"text":':
                    i = (j + 1)
                    while (line[j : (j + 2)] != '",'):
                        j += 1
                    text = line[i : j].replace('\\n', '\n').replace('\\"', '"')
                
                # Get the labels from the jsonl
                i = (j + 2)
                j = (i + 8)
                labels = []
                if line[i : j] == '"label":':
                    i = (j + 1)
                    if line[i] == '[':
                        while (line[i] != ','):
                            i += 1
                            j = (i + 1)
                            while (line[j] != ','):
                                j += 1
                            first = int(line[i : j])
                            
                            i = (j + 1)
                            j = i
                            while (line[j] != ','):
                                j += 1
                            last = int(line[i : j])
                            
                            i = (j + 2)
                            j = i
                            while (line[j] != '"'):
                                j += 1
                            name = line[i : j]
                            
                            labels.append(
                                {
                                    'first': first,
                                    'last': last,
                                    'name': name
                                }
                            )
                            i = (j + 3)
                    else:
                        i += 1
                
                # Get the comments from the jsonl
                i += 1
                j = (i + 11)
                Comments = []
                if line[i : j] == '"Comments":':
                    i = (j + 1)
                    if line[i] == '"':
                        while line[i] != '}':
                            i += 1
                            j = (i + 1)
                            while (line[j] != '"'):
                                j += 1
                            comment = line[i : j]
                            
                            Comments.append(comment)
                            i = (j + 2)
                
                self.texts[text_id] = {
                    'text': text,
                    'labels': labels,
                    'Comments': Comments
                }
    
    # Print the id of every text
    def print_ids(self):
        print('id = [', end = '')
        i = 0
        for text_id in self.texts:
            print(text_id, end = '')
            if i != (len(self.texts) - 1):
                print(', ', end = '')
            i += 1
        print(']\n')
    
    # Print every text
    def print_texts(self):
        for text_id in self.texts:
            print('id =', text_id)
            print('text = [')
            print(self.texts[text_id]['text'] + ']\n')
    
    # Print the text with the specified id ("text_id")
    def print_text(self, text_id: int):
        if text_id in self.texts:
            print('id =', text_id)
            print('text = [')
            print(self.texts[text_id]['text'] + ']\n')
        else:
            print("The id doesn't match any of the texts!\n")
    
    # Print the labels of every text
    def print_annotations(self):
        for text_id in self.texts:
            print('id =', text_id)
            print('labels = [', end = '')
            
            i = 0
            for label in self.texts[text_id]['labels']:
                print('[' + self.texts[text_id]['text'][label['first'] : label['last']] + ', ', end = '')
                print(label['name'] + ']', end = '')
                if i != len(self.texts[text_id]['labels']) - 1:
                    print(', ', end = '')
                i += 1
            print(']\n')
    
    # Print the labels of the text with the specified id ("text_id")
    def print_text_annotations(self, text_id: int):
        if text_id in self.texts:
            print('id =', text_id)
            print('labels = [', end = '')
            
            i = 0
            for label in self.texts[text_id]['labels']:
                print('[' + self.texts[text_id]['text'][label['first'] : label['last']] + ', ', end = '')
                print(label['name'] + ']', end = '')
                if i != len(self.texts[text_id]['labels']) - 1:
                    print(', ', end = '')
                i += 1
            print(']\n')
        else:
            print("The id doesn't match any of the texts!\n")
    
    # Print all the labels of a certain type (e.g. "PER") for every text
    def print_labels_of_type(self, label_name: str):
        for text_id in self.texts:
            print('id =', text_id)
            print('labels = [', end = '')
            
            i = 0
            b = False
            for label in self.texts[text_id]['labels']:
                if label['name'] == label_name:
                    if b:
                        print(', ', end = '')
                    print('[' + self.texts[text_id]['text'][label['first'] : label['last']] + ', ', end = '')
                    print(label['name'] + ']', end = '')
                    b = True
                i += 1
            print(']\n')
    
    # Print all the labels of a certain type (e.g. "PER") for the text with the specified id ("text_id")
    def print_text_labels_of_type(self, text_id: int, label_name: str):
        separators = ["'", '"', '.', ':', ',', ';', '!', '?', '-', '—', '\n']
        if text_id in self.texts:
            print('id =', text_id)
            print('label name =', label_name)
            print('labels = [')
            
            i = 0
            b = False
            for label in self.texts[text_id]['labels']:
                if label['name'] == label_name:
                    if b:
                        print('\n')
                    print(self.texts[text_id]['text'][label['first'] : label['last']], end = '')
                    print('\t' + str(label['first']) + '-' + str(label['last']))
                    j = label['first'] - 3
                    while self.texts[text_id]['text'][j] not in separators and j >= 0:
                        j -= 1
                    if self.texts[text_id]['text'][j] == '\n':
                        j += 1
                    else:
                        j += 2
                    k = label['last'] + 3
                    while self.texts[text_id]['text'][k] not in separators and k < len(self.texts[text_id]['text']):
                        k += 1
                    if self.texts[text_id]['text'][k] == '\n':
                        k -= 2
                    else:
                        k -= 1
                    print(self.texts[text_id]['text'][j : k])
                    b = True
                i += 1
            print(']\n')
        else:
            print("The id doesn't match any of the texts!\n")
    
    # Print the comments of every text
    def print_comments(self):
        for text_id in self.texts:
            print('id =', text_id)
            print('Comments =', self.texts[text_id]['Comments'])
            print()
    
    # Print the comments of the text with the specified id ("text_id")
    def print_text_comments(self, text_id: int):
        if text_id in self.texts:
            print('id =', text_id)
            print('Comments =', self.texts[text_id]['Comments'])
            print()
        else:
            print("The id doesn't match any of the texts!\n")
    
    # Print the word, or words, of every text, with the associated annotations, until "upper_limit"
    def print_word(self, word: str, upper_limit: int):
        print('word =', word + '\n\n')
        separators = ["'", '"', '.', ':', ',', ';', '!', '?', '-', '—', '\n']
        occurrences = 0
        for text_id in self.texts:
            if text_id < upper_limit:
                i = 0
                cont = 0
                while i < len(self.texts[text_id]['text']):
                    if self.texts[text_id]['text'][i] == word[cont]:
                        cont += 1
                    else:
                        cont = 0
                    if cont == len(word):
                        print('id =', str(text_id) + '\n')
                        occurrences += 1
                        
                        j = i - len(word) - 3
                        while self.texts[text_id]['text'][j] not in separators and j >= 0:
                            j -= 1
                        if self.texts[text_id]['text'][j] == '\n':
                            j += 1
                        else:
                            j += 2
                        k = i + 3
                        while self.texts[text_id]['text'][k] not in separators and k < len(self.texts[text_id]['text']):
                            k += 1
                        if self.texts[text_id]['text'][k] == '\n':
                            k -= 2
                        else:
                            k -= 1
                        print('"' + self.texts[text_id]['text'][j : k] + '"' + '\t' + str(j), end = '')
                        print('-' + str(k))
                        
                        cont = 0
                        for label in self.texts[text_id]['labels']:
                            if label['first'] >= j and label['last'] <= k:
                                z = label['first']
                                while z != (label['last'] + 1):
                                    if self.texts[text_id]['text'][z] == word[cont]:
                                        cont += 1
                                    else:
                                        cont = 0
                                    if cont == len(word):
                                        print(self.texts[text_id]['text'][label['first'] : label['last']] + '\t', end = '')
                                        print(str(label['first']) + '-' + str(label['last']) + '\t' + label['name'])
                                        cont = 0
                                    z += 1
                        
                        print('\n')
                    i += 1
        print('occurrences = ' + str(occurrences) + '\n')
    
    # Print the numbers of annotations for each type
    def print_annotations_number(self):
        annotations = {}
        for text_id in self.texts:
            for label in self.texts[text_id]['labels']:
                if label['name'] in annotations:
                    annotations[label['name']] += 1
                else:
                    annotations[label['name']] = 0
        
        print('In the next lines will be printed the numbers of annotations for each type:')
        total = 0
        for annotation_type in annotations:
            total += annotations[annotation_type]
            print(annotation_type + ' = ' + str(annotations[annotation_type]))
        print('There is a total of ' + str(total) + ' annotations.\n')

# Check if all the labels start with a number lower than the other
def check_correctness(a: Annotations):
    found = False
    for text_id in a.texts:
        for label in a.texts[text_id]['labels']:
            label_phrase = a.texts[text_id]['text'][label['first'] : label['last']]
            if label['first'] >= label['last']:
                print('"' + label_phrase + '"', end = ' ')
                print(str(label['first']) + '-' + str(label['last']) + ' ' + label['name'])
                print('id =', str(text_id) + '\n')
                found = True
    
    if not found:
        print("There aren't labels that cannot be read correctly.\n")

# Check if the labels are sorted for every text
def check_if_sorted(a: Annotations):
    found = False
    for text_id in a.texts:
        previous_label = None
        for label in a.texts[text_id]['labels']:
            if previous_label != None:
                if previous_label['first'] > label['first']:
                    print('In text ' + str(text_id) + ' there are labels that appear to be not sorted:')
                    print(str(previous_label['first']) + '-' + str(previous_label['last']), end = '')
                    print('\t' + str(label['first']) + '-' + str(label['last']))
                    found = True
                elif previous_label['first'] == label['first']:
                    if previous_label['last'] == label['last']:
                        print('In text ' + str(text_id) + ' there are labels that appear to be the same:')
                        print(str(previous_label['first']) + '-' + str(previous_label['last']), end = '')
                        print('\t' + str(label['first']) + '-' + str(label['last']))
                        found = True
            previous_label = label
    
    if not found:
        print('The labels are sorted for every text.\n')

# Check if the labels start or end with a or more white spaces
def find_spaces_at_the_sides(a: Annotations):
    found = False
    for text_id in a.texts:
        for label in a.texts[text_id]['labels']:
            label_phrase = a.texts[text_id]['text'][label['first'] : label['last']]
            if label_phrase.startswith(' ') or label_phrase.endswith(' '):
                print('"' + label_phrase + '"', end = ' ')
                print(str(label['first']) + '-' + str(label['last']) + ' ' + label['name'])
                print('id =', str(text_id) + '\n')
                found = True
    
    if not found:
        print("There aren't labels that start or end with white spaces.\n")

# Check if the labels start or end with a truncated word
def find_words_at_the_sides(a: Annotations):
    separators = ["'", '"', '.', ':', ',', ';', '!', '?', '-', '—', '\n']
    found = False
    for text_id in a.texts:
        for label in a.texts[text_id]['labels']:
            label_phrase = a.texts[text_id]['text'][label['first'] : label['last']]
            
            before = a.texts[text_id]['text'][label['first'] - 1]
            if before != ' ' and before != '\n':
                print('"' + label_phrase + '"', end = ' ')
                print(str(label['first']) + '-' + str(label['last']) + ' ' + label['name'])
                i = label['first'] - 1
                while a.texts[text_id]['text'][i] not in separators:
                    i -= 1
                print(a.texts[text_id]['text'][i : label['last']])
                print('id =', str(text_id) + '\n')
                found = True
            
            after = a.texts[text_id]['text'][label['last']]
            if after != ' ' and after != '\n':
                print('"' + label_phrase + '"', end = ' ')
                print(str(label['first']) + '-' + str(label['last']) + ' ' + label['name'])
                i = label['last']
                while a.texts[text_id]['text'][i] not in separators:
                    i += 1
                print(a.texts[text_id]['text'][label['first'] : i])
                print('id =', str(text_id) + '\n')
                found = True
    
    if not found:
        print("There aren't labels that start or end with words.\n")

# Check if all the labels have one of the type specified by "labels_types"
def check_labels_types(a: Annotations, labels_types: list):
    found = False
    for text_id in a.texts:
        for label in a.texts[text_id]['labels']:
            label_phrase = a.texts[text_id]['text'][label['first'] : label['last']]
            if label['name'] not in labels_types:
                print('"' + label_phrase + '"', end = ' ')
                print(str(label['first']) + '-' + str(label['last']) + ' ' + label['name'])
                print('id =', str(text_id) + '\n')
                found = True
    
    if not found:
        print("There aren't labels that have a strange type.\n")

# Make the ann file for every text
def make_ann(a: Annotations, input_folders_name: str, output_folders_name: str):
    i = 1
    for filename in os.listdir(input_folders_name):
        j = 0
        with open(output_folders_name + '\\' + filename[: -3] + 'ann', 'wt', encoding = 'utf-8') as file:
            for label in a.texts[i]['labels']:
                if j != 0:
                    file.write('\n')
                file.write('T' + str(j) + '\t')
                file.write(label['name'] + ' ' + str(label['first']) + ' ' + str(label['last']) + '\t')
                file.write(a.texts[i]['text'][label['first'] : label['last']])
                j += 1
        i += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help = 'input jsonl file', required = True)
    parser.add_argument('-o', '--output', help = 'output directory to write new ann files to', required = True)
    
    args = vars(parser.parse_args())
    input_file = args['input']
    output_directory = args['output']
    
    a = Annotations(input_file)
    
    '''
    a.print_ids()
    
    #a.print_texts()
    a.print_text(5)
    
    #a.print_annotations()
    a.print_text_annotations(10)
    
    #a.print_labels_of_type('ORG')
    a.print_text_labels_of_type(25, 'FAC')
    
    #a.print_comments()
    a.print_text_comments(25)
    
    a.print_word('lago', 101)
    '''
    
    check_correctness(a)
    
    check_if_sorted(a)
    
    find_spaces_at_the_sides(a)
    
    find_words_at_the_sides(a)
    
    check_labels_types(a, ['PER', 'FAC', 'LOC', 'GPE', 'VEH', 'ORG'])
    
    a.print_annotations_number()
    
    make_ann(a, output_directory, output_directory)