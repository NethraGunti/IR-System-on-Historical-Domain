import sqlite3, re, time, math, os, json, pprint

import numpy as np
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from spell import main

docs = {}
result = {}
con = sqlite3.connect('inforet.db')
con.isolation_level = None
cur = con.cursor()

def process_doc(docname):
    data_path = 'dataset'
    f = open(os.path.join(data_path, docname), 'r')
    content = json.loads(f.read())['text']
    unicode = re.compile(r"[^\U00000000-\U0000007F]")
    content = unicode.sub(" ", content)
    clean = re.compile(r'[\-#"():+,.*/$%&]')
    delim = re.compile(r'\W+')
    newline = re.compile(r'\n+')
    content = re.sub(newline, " ", content)
    content = clean.sub(" ", content)
    content = re.sub("'", "", content)
    pre_data = pre_process(content)
    # print(pre_data)
    return pre_data

def pre_process(query):
    stop_words = set(stopwords.words('english'))
    stop_words.remove('of')
    # print(stop_words)
    word_tokens = word_tokenize(query)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence

def get_term_id(term):
    q_word_id = '''SELECT TERMID FROM TERMSTABLE WHERE TERM="{}"'''.format(term)
    try:
        cur.execute(q_word_id)
        row = cur.fetchone()
        return row[0]
    except:
        pass

def commonElements(docs_list):
    common = set(docs_list[0])
    for l in docs_list:
        common = common.intersection(set(l))
    return common

def calc_tf(words, docs):
    tf = {}
    for word in words:
        tf[word] = {}
        for doc in docs:
            # print(doc, word)
            q = '''SELECT P.TERMCOUNT FROM POSITIONALINDEX AS P WHERE P.TERMID={} AND P.DOCID={}'''.format(get_term_id(word), doc)
            try:
                cur.execute(q)
                row = cur.fetchone()
                tf[word][doc] = row[0]
            except:
                continue
            # print(row[0])
    return tf

def calc_idf(N, words):
    idf = {}
    for word in words:
        q = '''SELECT DOCCOUNT FROM TERMSTABLE WHERE TERMID={}'''.format(get_term_id(word))
        try:
            cur.execute(q)
            row = cur.fetchone()
            idf[word] = round(math.log(N/row[0], 10), 3)
        except:
            continue
    return idf
    
def calc_tfidf(N, words, docs):
    tf = calc_tf(words, docs)
    idf = calc_idf(N, words)
    tfidf ={}
    for i in words:
        tfidf[i] = {}
        for doc in docs:
            try:
                tfidf[i][doc] = tf[i][doc] * idf[i]
            except:
                tfidf[i][doc] = 0
    return tfidf



def get_doc(name):
    f = open('dataset/{}'.format(name), 'r')
    data = json.loads(f.read())
    f.close()
    return data


# query: search item
# N: number of documents in the databse
# 
def search_query(q=None):

    if not q:
        query = input("Enter Query: ")
    else:
        query = q

    start_time = time.time()
    processed_input = pre_process(query)
    processed_input = [main(correct) for correct in processed_input]
    
    postings = {}
    docs_list = []
    for word in processed_input:
        pquery = '''SELECT * FROM POSITIONALINDEX WHERE TERMID={}'''.format(get_term_id(word))
        s = cur.execute(pquery)

        posting = [i for i in s]
        d = []
        for p in posting:
            pd = p[1]
            d.append(pd)
        docs_list.append(d)
        postings[word] = posting

    if docs_list:
        common_docs = commonElements(docs_list)
        if not common_docs:
            common_docs = []
            for i in docs_list:
                common_docs.extend(i)
    
    else:
        print('No Matching Results!')
        exit()

    for doc in common_docs:
        q = '''SELECT DOCTITLE FROM DOCTABLE WHERE DOCID={}'''.format(doc)
        try:
            cur.execute(q)
            row = cur.fetchone()
            docs[doc] = row[0]
        except:
            continue
    # print(docs)
    
    q = '''SELECT COUNT(*) FROM DOCTABLE'''
    cur.execute(q)
    row = cur.fetchone()
    N = row[0]

    # tf(i, d) = termcount from postingstable where i=word and d=docid
    #idf N/doccount
    tfidf = calc_tfidf(N, processed_input, common_docs)
    # print(tfidf)
    query_vector = []
    doc_vector = {}
    query_vector = {}
    similarity = {}
    for docid, docname in docs.items():
        # try:
        #get a sorted, clean doc
        text = process_doc(docname)
        processed_doc = set(sorted(text))
        doc_tfidf = calc_tfidf(N, processed_doc, [docid])
        

        set_words = sorted(list(set(processed_input).union(processed_doc)))
        query_vector[docid] = []
        doc_vector[docid] = []

        for w in set_words:
            if w in processed_input:
                query_vector[docid].append(tfidf[w][docid])
            else:
                query_vector[docid].append(0)
            if w in processed_doc:
                doc_vector[docid].append(doc_tfidf[w][docid])
            else:
                doc_vector[docid].append(0)

        query_norm = np.linalg.norm(query_vector[docid])
        doc_norm = np.linalg.norm(doc_vector[docid])
        cosine_similarity = np.sum(np.multiply(query_vector[docid], doc_vector[docid])) / (query_norm*doc_norm)
        similarity[docid] = cosine_similarity
        # except:
            # continue


    result = dict(sorted(similarity.items(), key=lambda t: t[1], reverse=True))
    print('results retrieved in ', time.time()-start_time, ' secs')
    
    print(";dihd")
    for d in result:
        print(d)
        q = '''SELECT DOCTITLE FROM DOCTABLE WHERE DOCID={}'''.format(d)
        cur.execute(q)
        row = cur.fetchone()[0]
        data = get_doc(row)
        print('DocID: ',row)
        print('Title: ',data['title'])
        print('URL: ',data['url'])
        print('=================================================================')

    return result


def search_tag():
    tag = input("Enter Tag: ")
    q = '''SELECT DOCIDS FROM TAGSTABLE WHERE TAG="{}"'''.format(tag)
    cur.execute(q)
    row = cur.fetchone()[0]
    docs = row.split(", ")
    return docs



def fetch(did=None):
    if not did:
        docID = int(input("Enter docid to retrieve: "))
    else:
        docID = did
    file = json.loads(open(os.path.join(data_path, docID)))
    pprint(f"DocID: {docID} Title: {file['title']}")
    pprint(f"URL: {file['url']}\n")
    kf = figures(file['text'])
    pprint(f"Key Figures:\n\n {kf}\n")
    pprint(f"Doc Excerpt:\n\n {file['text']}")
    rec_docs = set()
    for item in kf:
        docs=search(item[0])
        for doc in docs:
            rec_docs.add(doc)
    pprint(f"Similar Docs:\n\n")
    pprint(rec_docs)