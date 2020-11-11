import nltk
import sys
import os
import math
import time

FILE_MATCHES = 1
SENTENCE_MATCHES = 3


def main():

    # Check command-line arguments
    if len(sys.argv) == 2:
        #sys.exit("Usage: python questions.py corpus")
        files = load_files(sys.argv[1])
    # Calculate IDF values across files
    else:
        path= os.path.join(os.getcwd(), "corpus")
        files= load_files(path)
 
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    result= {}
    files= os.listdir(directory)
    for key in files:
        with open(directory+ os.sep+ f"{key}", "r", encoding='utf-8') as f:
           result[key]= f.read()
    
    return result

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens= nltk.word_tokenize(document)
    to_ignore= nltk.corpus.stopwords.words("english")
    include= ["is", "was", "do", "did"]
    to_ignore= list(set(to_ignore) - set(include))
    new_data= []
    count=0
    total= len(tokens)
    for token in tokens:
        count+= 1
        ratio= count/total
        progress(percent= ratio*100, string="tokenizing:\t\t ")
        token= token.lower()
        if token.islower():
            if token not in to_ignore:
                new_data.append(token)
            
    return new_data

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    print()
    calculated= set()
    total= len(documents)
    idf_dict= {} 
    count=0
    for doc in documents:
        count+= 1
        ratio= count/total
        progress(percent= ratio*100, string= "calculating idfs:\t ")
        for word in documents[doc]:
            
            if word in calculated:
                continue
            calculated.add(word)
            doc_counter= 1
            
            for doc1 in documents:
                if doc== doc1:
                    continue
                if word in documents[doc1]:
                    doc_counter+= 1
                    
            idf_dict[word]= math.log(total/doc_counter)

    
    print("\n"*2)
    return idf_dict

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_value= {}
    for file in files:
        value= 0
        for word in query:
            if word in files[file]:
                value+= idfs[word] * files[file].count(word)
        file_value[file]= value
        
    file_value= sorted(file_value, key= lambda file: file_value[file], reverse= True)
    
     
    top_f= file_value[: n]
    print(f"\nbest matche(s): {top_f}")
    return top_f


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentences_value= {}
    for sentence in sentences:
        if "https" in sentence or "===" in sentence:
            continue
        value= 0
        counter= 0
        for word in query:
            if word in sentences[sentence]:
                counter+= sentences[sentence].count(word)
                value+= idfs[word]
        density= counter/len(sentences[sentence])
        sentences_value[sentence]= (value, density)
    
    sentences_list= [sentence for sentence in sentences_value] 
    sentences_list= sorted(sentences_list, key= lambda sentence: sentences_value[sentence][1], reverse= True)
    sentences_list= sorted(sentences_list, key= lambda sentence: sentences_value[sentence][0], reverse= True)
    top_sentences= sentences_list[: n]
    """
    for sen in top_sentences:
        print(sen, end= "\t")
        print(sentences_value[sen])
  """
    return top_sentences

def progress(percent=0, width=30, string=""):
    left = int(width * percent / 100)
    right = width - left
    print('\r', string,"[", '#' * left, ' ' * right, ']',
          f' {percent:.0f}%',
          sep='', end='', flush=True)

if __name__ == "__main__":
    main()
