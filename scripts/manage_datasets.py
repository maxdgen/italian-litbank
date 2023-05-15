import argparse
import pandas
import os

# Get all the annotations from the ann files contained in the folder "input_folders_name"
def read_ann_from_files(input_folders_name: str):
    total_annotations = {}
    for filename in os.listdir(input_folders_name):
        if filename[-3 :] == 'ann':
            total_annotations[filename] = []
            with open(input_folders_name + '\\' + filename, 'rt', encoding = 'utf-8') as file:
                for line in file.readlines():
                    annotation = {}
                    
                    if line[-1] == '\n':
                        line = line[0 : -1]
                    line = line.split('\t')
                    
                    annotation['index'] = line[0]
                    
                    label = line[1].split(' ')
                    annotation['label'] = {
                        'name': label[0],
                        'first': int(label[1]),
                        'last': int(label[2])
                    }
                    
                    annotation['phrase'] = line[2]
                    
                    total_annotations[filename].append(annotation)
    
    return total_annotations

# Get all the annotations from the input file
def read_ann_from_file(filename: str):
    total_annotations = {}
    with open(filename, 'rt', encoding = 'utf-8') as file:
        for line in file.readlines():
            if len(line) > 1:
                if line[-2] == ':':
                    text = line[0 : -2]
                    
                    total_annotations[text] = []
                else:
                    annotation = {}
                    
                    if line[-1] == '\n':
                        line = line[0 : -1]
                    line = line.split('\t')
                    
                    annotation['index'] = line[0]
                    
                    label = line[1].split(' ')
                    annotation['label'] = {
                        'name': label[0],
                        'first': int(label[1]),
                        'last': int(label[2])
                    }
                    
                    annotation['phrase'] = line[2]
                    
                    total_annotations[text].append(annotation)
    
    return total_annotations

# Write the ann files in the "output_folders_name" with the annotations contained in "dataset"
def write_ann_to_files(output_folders_name: str, dataset: dict):
    for text in dataset:
        with open(output_folders_name + '\\' + text, 'wt', encoding = 'utf-8') as file:
            i = 1
            for annotation in dataset[text]:
                file.write(annotation['index'] + '\t')
                file.write(annotation['label']['name'] + ' ' + str(annotation['label']['first']) + ' ' + str(annotation['label']['last']) + '\t')
                file.write(annotation['phrase'])
                
                if i < len(dataset[text]):
                    file.write('\n')
                i += 1

# Create a file where all the annotations for each text will be written
def write_ann_to_file(filename: str, dataset: dict):
    with open(filename, 'wt', encoding = 'utf-8') as file:
        i = 1
        for text in dataset:
            file.write(text + ':')
            for annotation in dataset[text]:
                file.write('\n')
                
                file.write(annotation['index'] + '\t')
                file.write(annotation['label']['name'] + ' ' + str(annotation['label']['first']) + ' ' + str(annotation['label']['last']) + '\t')
                file.write(annotation['phrase'])
            
            if i != len(dataset):
                file.write('\n\n')
            i += 1

# Get all the equal or different annotations between the input datasets
def get_occurrences(dataset1: dict, dataset2: dict, equals: bool = True):
    occurrences_dataset = {}
    for text in dataset1:
        occurrences_in_text = []
        for annotation1 in dataset1[text]:
            found = False
            for annotation2 in dataset2[text]:
                if (annotation1['label']['first'] == annotation2['label']['first']):
                    if (annotation1['label']['last'] == annotation2['label']['last']):
                        if (annotation1['label']['name'] == annotation2['label']['name']):
                            found = True
                            break
            if equals:
                if found:
                    occurrences_in_text.append(annotation1)
            else:
                if not found:
                    occurrences_in_text.append(annotation1)
        
        occurrences_dataset[text] = occurrences_in_text
    
    return occurrences_dataset

# Remove all the matches of the words contained in the list "to_consider" in the annotated phrases
# only when the next word in the annotation doesn't match any word in the list "to_skip"
def remove_words_from_start(dataset: dict, to_consider: list, to_skip: list = []):
    for text in dataset:
        for annotation in dataset[text]:
            if len(annotation['phrase']) > 3:
                for word in to_consider:
                    length = len(word)
                    if annotation['phrase'][0 : length] == word:
                        found = False
                        if len(to_skip) != 0:
                            for skip in to_skip:
                                if annotation['phrase'][length : length + (len(skip))] == skip:
                                    found = True
                                    break
                        
                        if not found:
                            #print(annotation['phrase'] + '\t' + str(annotation['label']['first']) + ' ' + str(annotation['label']['last']))
                            annotation['phrase'] = annotation['phrase'][length :]
                            annotation['label']['first'] += length
                            #print(annotation['phrase'] + '\t' + str(annotation['label']['first']) + ' ' + str(annotation['label']['last']))
                        
                        break

# Sort the input dataset
def sort_dataset(dataset: dict):
    for text in dataset:
        i = 0
        while i < len(dataset[text]):
            if i != 0:
                if dataset[text][i]['label']['first'] < dataset[text][i - 1]['label']['first']:
                    j = i
                    while (dataset[text][j]['label']['first'] < dataset[text][j - 1]['label']['first']) and (j != 0):
                        dataset[text][j], dataset[text][j - 1] = dataset[text][j - 1], dataset[text][j]
                        j -= 1
            i += 1
    
    for text in dataset:
        i = 0
        for annotation in dataset[text]:
            annotation['index'] = 'T' + str(i)
            i += 1

# Create a new dataset starting from the input dataset and the files "differences" and "final_differences"
def fuse_datasets(differences: str, final_differences: str, dataset: dict):
    fused_dataset = dataset
    
    differences_dataset = read_ann_from_file(differences)
    final_differences_dataset = read_ann_from_file(final_differences)
    
    to_remove = {}
    for text in differences_dataset:
        to_remove[text] = []
        for annotation in differences_dataset[text]:
            if annotation not in final_differences_dataset[text]:
                to_remove[text].append(annotation)
    #print(to_remove)
    for text in to_remove:
        for annotation in to_remove[text]:
            if annotation in fused_dataset[text]:
                fused_dataset[text].remove(annotation)
    
    to_add = {}
    for text in final_differences_dataset:
        to_add[text] = []
        for annotation in final_differences_dataset[text]:
            if annotation not in differences_dataset[text]:
                to_add[text].append(annotation)
    #print(to_add)
    for text in to_add:
        for annotation in to_add[text]:
            if annotation not in fused_dataset[text]:
                fused_dataset[text].append(annotation)
    
    sort_dataset(fused_dataset)
    
    return fused_dataset

# Get the number of all the annotations present in the dataset
def get_ann_number(dataset: dict):
    entity_types = {}
    total = 0
    for text in dataset:
        for annotation in dataset[text]:
            if not annotation['label']['name'] in entity_types:
                entity_types[annotation['label']['name']] = 0
            else:
                entity_types[annotation['label']['name']] += 1
            total += 1
    keys = list(entity_types.keys())
    keys.sort()
    sorted_entity_types = {i: entity_types[i] for i in keys}
    
    occurrences = {
        'types': sorted_entity_types,
        'total': total
    }
    
    return occurrences

# Print the number of all the annotations present in "occurrences"
def print_ann_number(occurrences: dict, to_print: str):
    print('There is a total of ' + str(occurrences['total']) + ' annotations present in ', end = '')
    print(to_print, end = '')
    print(', of which:')
    for labels_type in occurrences['types']:
        print(labels_type + ' = ' + str(occurrences['types'][labels_type]) + '\t', end = '')
    print()

# Plot the comparison of the types of the entities between "occurrences1" and "occurrences2"
def plot_types_comparison(occurrences1: dict, occurrences2: dict):
    for entity_type in occurrences1['types']:
        occurrences1['types'][entity_type] /= occurrences1['total']
    for entity_type in occurrences2['types']:
        occurrences2['types'][entity_type] /= occurrences2['total']
    
    df = pandas.DataFrame({'entities1': occurrences1['types'].values(),
                           'entities2': occurrences2['types'].values()},
                          index = occurrences1['types'].keys())
    df.plot.bar(figsize = (4, 4), title = 'frequency')

# Get the number of annotations of the dataset for each level
def get_ann_number_for_levels(dataset: dict):
    levels = {}
    total = 0
    for text in dataset:
        i = 0
        nested_ann = []
        while i < len(dataset[text]):
            actual_level = 'no'
            
            found = False
            for ann in nested_ann:
                if dataset[text][i]['label']['first'] < ann['label']['last']:
                    if actual_level == 'no':
                        actual_level = 1
                    else:
                        actual_level += 1
                    found = True
            if not found:
                nested_ann.clear()
            
            total += 1
            if actual_level in levels:
                levels[actual_level] += 1
            else:
                levels[actual_level] = 1
            
            nested_ann.append(dataset[text][i])
            i += 1
    
    occurrences = {
        'levels': levels,
        'total': total
    }
    
    return occurrences

# Print the number of annotations of "occurrences" for each level
def print_ann_number_for_levels(occurrences: dict):
    print('Below are the number of annotations for each level:')
    for level in occurrences['levels']:
        print(str(level), end = '')
        print(':\t\t' + str(occurrences['levels'][level]) + '\t\t', end = '')
        if occurrences['levels'][level] < 1000:
            print('\t', end = '')
        print(str('{:.3f}'.format((occurrences['levels'][level] / occurrences['total']) * 100)) + '%')

# Plot the comparison of the nested levels between "occurrences1" and "occurrences2"
def plot_levels_comparison(occurrences1: dict, occurrences2: dict):
    for level in occurrences1['levels']:
        if level not in occurrences2['levels']:
            occurrences2['levels'][level] = 0
        occurrences1['levels'][level] /= occurrences1['total']
    for level in occurrences2['levels']:
        if level not in occurrences1['levels']:
            occurrences1['levels'][level] = 0
        occurrences2['levels'][level] /= occurrences2['total']
    
    df = pandas.DataFrame({'entities1': occurrences1['levels'].values(),
                           'entities2': occurrences2['levels'].values()},
                          index = occurrences1['levels'].keys())
    df.plot.bar(figsize = (4, 4), title = 'nesting')

# Print the average of the annotations of the dataset
def print_ann_average(dataset: dict):
    average = 0
    for text in dataset:
        average += len(dataset[text])
    average /= len(dataset)
    print('There is an average of ' + str('{:.1f}'.format(average)) + ' annotations for each text.')

# Compare the datasets and plot the results
def compare_datasets(dataset1: dict, name_dataset1: str, dataset2: dict, name_dataset2: str):
    types1 = get_ann_number(dataset1)
    print_ann_number(types1, name_dataset1)
    print_ann_average(dataset1)
    levels1 = get_ann_number_for_levels(dataset1)
    print_ann_number_for_levels(levels1)
    print()
    types2 = get_ann_number(dataset2)
    print_ann_number(types2, name_dataset2)
    print_ann_average(dataset2)
    levels2 = get_ann_number_for_levels(dataset2)
    print_ann_number_for_levels(levels2)
    
    plot_types_comparison(types1, types2)
    plot_levels_comparison(levels1, levels2)

# Analyse the two input datasets by printing the number of annotations they have in common and
# the number of different annotations between them
def analyse_datasets(dataset1: dict, name_dataset1: str, dataset2: dict, name_dataset2: str):
    commons_dataset = get_occurrences(dataset1, dataset2)
    c_types = get_ann_number(commons_dataset)
    print_ann_number(c_types, 'both datasets')
    print_ann_average(commons_dataset)
    print()
    
    differents_dataset1 = get_occurrences(dataset1, dataset2, False)
    d_types1 = get_ann_number(differents_dataset1)
    print_ann_number(d_types1, (name_dataset1 + ' and absent in ' + name_dataset2))
    print_ann_average(differents_dataset1)
    differents_dataset2 = get_occurrences(dataset2, dataset1, False)
    d_types2 = get_ann_number(differents_dataset2)
    print_ann_number(d_types2, (name_dataset2 + ' and absent in ' + name_dataset1))
    print_ann_average(differents_dataset2)

# Analyse the input dataset by plotting the number of annotations
def analyse_dataset(dataset: dict):
    types = get_ann_number(dataset)
    print_ann_number(types, 'the fused dataset')
    print_ann_average(dataset)
    levels = get_ann_number_for_levels(dataset)
    print_ann_number_for_levels(levels)
    
    df1 = pandas.DataFrame({'Italian-Litbank': types['types'].values()}, index = types['types'].keys())
    df1.plot.pie(y = 'Italian-Litbank', figsize = (4, 4), title = 'frequency')
    for level in levels['levels']:
        levels['levels'][level] /= levels['total']
    df2 = pandas.DataFrame({'Italian-Litbank': levels['levels'].values()}, index = levels['levels'].keys())
    df2.plot.bar(figsize = (4, 4), title = 'nesting')

# Make the jsonl file for the dataset
def make_jsonl(input_folders_name: str, dataset: dict):
    texts = {}
    for filename in os.listdir(input_folders_name):
        if filename[-3 :] == 'txt':
            with open(input_folders_name + '\\' + filename, 'rt', encoding = 'utf-8') as file:
                texts[filename[0 : -3] + 'ann'] = file.read()
    
    with open(input_folders_name[0 : -4] + 'annotations.jsonl', 'wt', encoding = 'utf-8') as file:
        i = 0
        for text in dataset:
            i += 1
            file.write('{"id":' + str(i) + ',')
            file.write('"text":"' + texts[text].replace('\n', '\\n') + '",')
            file.write('"label":[')
            j = 0
            for annotation in dataset[text]:
                file.write('[' + str(annotation['label']['first']) + ',')
                file.write(str(annotation['label']['last']) + ',')
                file.write('"' + annotation['label']['name'] + '"]')
                if j < len(dataset[text]) - 1:
                    file.write(',')
                j += 1
            file.write('],"Comments":[]}\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    '''
    parser.add_argument('dir_dataset1', help = 'directory containing the first annotated dataset (brat folder)')
    parser.add_argument('dir_dataset2', help = 'directory containing the second annotated dataset (brat folder)')
    
    args = parser.parse_args()
    
    annotated_dataset1 = read_ann_from_files(args.dir_dataset1)
    annotated_dataset2 = read_ann_from_files(args.dir_dataset2)
    
    compare_datasets(annotated_dataset1, args.dir_dataset1.split('/')[-2], annotated_dataset2, args.dir_dataset2.split('/')[-2])
    print()
    
    analyse_datasets(annotated_dataset1, args.dir_dataset1.split('/')[-2], annotated_dataset2, args.dir_dataset2.split('/')[-2])
    print()
    
    definite_articles = ['Il ', 'il ', 'Lo ', 'lo ', 'La ', 'la ', 'I ', 'i ', 'Gli ', 'gli ',
                         'Le ', 'le ', "L ' ", "l ' "]
    indefinite_articles = ["Un ' ", "un ' ", 'Un ', 'un ', 'Uno ', 'uno ', 'Una ', 'una ']
    
    words_to_skip = ['Dei ', 'dei ', 'Di ', 'di ', 'Da ', 'da ', 'Ha ', 'ha ', 'Si ', 'si ', 'O ', 'o ',
                     'Che ', 'che ', 'Soltanto', 'soltanto', '....', 'Paio ', 'paio ', 'E ', 'e ',
                     'Delle ', 'delle ', 'Degli ', 'degli ', 'Fra ', 'fra ', 'Tra ', 'tra ',
                     'Solo', 'solo', 'Poteva ', 'poteva ', 'Ventina ', 'ventina ', "Po ' ", "po ' "]
    
    remove_words_from_start(annotated_dataset1, definite_articles)
    remove_words_from_start(annotated_dataset1, indefinite_articles, words_to_skip)
    
    remove_words_from_start(annotated_dataset2, definite_articles)
    remove_words_from_start(annotated_dataset2, ["D ' ", "d ' "], ['Azeglio', 'Artagnan', 'Accorsi'])
    remove_words_from_start(annotated_dataset2, indefinite_articles, words_to_skip)
    
    analyse_datasets(annotated_dataset1, args.dir_dataset1.split('/')[-2], annotated_dataset2, args.dir_dataset2.split('/')[-2])
    #write_ann_to_file(args.dir_dataset1[0 : -4] + 'differences', get_occurrences(annotated_dataset1, annotated_dataset2, False))
    #write_ann_to_file(args.dir_dataset2[0 : -4] + 'differences', get_occurrences(annotated_dataset2, annotated_dataset1, False))
    
    fused_dataset = fuse_datasets(args.dir_dataset1[0 : -4] + 'differences', args.dir_dataset1[0 : -4] + 'final_differences', annotated_dataset1)
    #write_ann_to_files('/'.join(args.dir_dataset1.split('/')[0 : -2]) + '/results/brat', fused_dataset)
    '''
    parser.add_argument('dir_dataset', help = 'directory containing the fused annotated dataset (brat folder)')
    
    args = parser.parse_args()
    
    fused_dataset = read_ann_from_files(args.dir_dataset)
    
    analyse_dataset(fused_dataset)
    
    #make_jsonl(args.dir_dataset, fused_dataset)