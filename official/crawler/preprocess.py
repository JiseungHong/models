import csv
import re
import kss

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from konlpy.tag import Okt
okt = Okt()

def morpheme(sentence):
    morphemes = okt.pos(sentence, norm=True, stem=False)
    list = [x[0] for x in morphemes if x[1] not in ['Josa', 'Punctuation']]
    target = " ".join(list)
    
    return target

data_dir = 'sample_output.csv'

with open(data_dir, newline='') as read_file:
    reader = csv.DictReader(read_file)
    
    # This variable is a list of dictionary, which contains same value of reader.
    # However, the values are 'preprocessed' by the following processes. e.g. [{'title': ..., 'content': ...}]
    preprocessed_reader = []
    
    # (a) Preprocessing.
    for row in reader:
        # (a-1) Extracting key sentence from the content.
        contents = kss.split_sentences(row['content'])
        title = row['\ufefftitle']
        
        # corpus is a list containing title and contents. It is used to vectorize words.
        corpus = []
        corpus.append(title)
        corpus.extend(contents)
        
        corpus_morpheme = [morpheme(x) for x in corpus]
        
        # 형태소 분석후 각각의 형태소를 space 단위로 쪼개서 입력해야한다.
        # Vectorization.
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(corpus_morpheme)
        
        assert(tfidf_matrix.shape[0] >= 2)
        
        max_cos_similarity, max_size = 0, tfidf_matrix.shape[0]
        max_sim_idx = 1
        for i, val in enumerate(tfidf_matrix):
            if i==0 or i==max_size-1:
                continue
            else:
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[i:i+1])
                if similarity > max_cos_similarity:
                    max_cos_similarity = similarity
                    max_sim_idx = i
        
        print(max_cos_similarity)
        content = corpus[max_sim_idx]
              
        # (a-2) Preprocessing the title, content.
        bracket_pattern = r'\s*\[.*\]\s*'
        paren_pattern = r'\(.*\)'
        
        preprocessed_content = re.compile(bracket_pattern).sub("", content)
        preprocessed_title = re.compile(bracket_pattern).sub("", title)
        
        # I think parenthesis includes meaningful infos.
        # preprocessed_content = re.compile(paren_pattern).sub("", preprocessed_content)
        # preprocessed_title = re.compile(paren_pattern).sub("", preprocessed_title)
        
        preprocessed_reader.append({'title': preprocessed_title,
                                    'content': preprocessed_content})
    
    # (b) Adding 'id' column. 'id' is not that important.
    with open("modified_output.csv", 'w', newline='') as write_file:
        
        fieldnames = ['', 'title', 'content']
        writer = csv.DictWriter(write_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in preprocessed_reader:
            writer.writerow({'': '9999993', 'title': row['title'], 'content': row['content']})
