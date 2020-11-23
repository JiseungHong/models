import csv
import re
import kss

data_dir = 'sample_output.csv'

with open(data_dir, newline='') as read_file:
    reader = csv.DictReader(read_file)
    
    # This variable is a list of dictionary, which contains same value of reader.
    # However, the values are 'preprocessed' by the following processes. e.g. [{'title': ..., 'content': ...}]
    preprocessed_reader = []
    
    # (a) Preprocessing.
    for row in reader:
        # (a-1) Extracting key sentence from the content.
        content = kss.split_sentences(row['content'])[0]
        title = row['\ufefftitle']
        
        # (a-2) Preprocessing the title, content.
        bracket_pattern = r'\[.*\]'
        paren_pattern = r'\(.*\)'
        
        preprocessed_content = re.compile(bracket_pattern).sub("", content)
        preprocessed_title = re.compile(bracket_pattern).sub("", title)
        
        preprocessed_content = re.compile(paren_pattern).sub("", preprocessed_content)
        preprocessed_title = re.compile(paren_pattern).sub("", preprocessed_title)
        
        preprocessed_reader.append({'title': preprocessed_title,
                                    'content': preprocessed_content})
    
    # (b) Adding 'id' column. 'id' is not that important.
    with open("modified_output.csv", 'w', newline='') as write_file:
        
        fieldnames = ['', 'title', 'content']
        writer = csv.DictWriter(write_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in preprocessed_reader:
            writer.writerow({'': '9999995', 'title': row['title'], 'content': row['content']})