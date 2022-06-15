import os
import string
import math
import nltk
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
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
    dict = {}

    for file in os.listdir(directory):
        with open(os.path.join(directory, file), mode='r', encoding='utf8') as f:
            dict[file[:-4]] = f.read().replace('\n', '')

    return dict
        
        

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    list_of_words = nltk.word_tokenize(document)
    list_of_words = (list)(map(lambda word : word.lower(), list_of_words))
    list_of_words = [word for word in list_of_words if (word not in string.punctuation and not word in nltk.corpus.stopwords.words("english") and not word == "``")]

    return list_of_words

def unique_words(documents):
    words = set()

    for _, value in documents.items():
        for word in value:
            words.add(word)

    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}
    set = unique_words(documents)
    all_docs = len(documents)

    for word in set:
        curr_docs = 0

        for key, _ in documents.items():
            if word in documents[key]:
                curr_docs += 1

        idfs[word] = math.log((all_docs / curr_docs))

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    top_files = {}

    for file_name in files:
        top_files[file_name] = 0
        for word in query:
            top_files[file_name] += files[file_name].count(word) * idfs[word]

    return sorted(top_files, key=top_files.get, reverse=True)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    top_sentences = {}

    for sentence, sentence_words in sentences.items():
        top_sentences[sentence] = 0
        counter = 0
        density_counter = 0
        for word in query:
            if word in sentence_words:
                counter += idfs[word]
                density_counter += 1
        density = density_counter / len(sentence_words)
        top_sentences[sentence] = (counter, density)

    return sorted(top_sentences.keys(), key=lambda s: (top_sentences[s][0], top_sentences[s][1]), reverse=True)[:n]


if __name__ == "__main__":
    main()
