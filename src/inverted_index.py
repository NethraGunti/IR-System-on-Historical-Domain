'''
Aditi Verma S20180010006
'''
import os
import re
# import numpy
import sys
import time
import math
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer
from collections import OrderedDict


class InvertedIndex:
    def __init__(self, start: int, end: int, path=None) -> None:
        self.index = {}
        self.start = start
        self.end = end
        self.common_words = ['the', 'a', 'an', 'is', 'was', 'or', 'as', 'to', 'at',
                             'on', 'with', 'it', 'in', 'are', 'were', 'and', 'be', 'of', 'so', 'i', 'am']
        self.path = os.path.join(os.getcwd(), 'json_files')
        if path:
            self.path = path

    def tokenize_add_index(self, s: str, file_num: str) -> None:
        clean = re.compile(r'[#"():+*/$%&_]')
        delim = re.compile(r'\W+')
        newline = re.compile(r'\\n+')
        s = re.sub(newline, " ", s)
        s = clean.sub(" ", s)
        s = s.lower()
        # print(s)
        # tokenizer = TweetTokenizer()
        # tokens = tokenizer.tokenize(s)
        tokens = delim.split(s)[:-1]
        # stemmer = PorterStemmer()
        N = len(tokens)
        # for i in range(N):
        #     tokens[i] = stemmer.stem(tokens[i])
        # print(tokens)
        for i in range(N):
            if tokens[i] not in self.common_words:
                if tokens[i] not in self.index:
                    self.index[tokens[i]] = {}
                    self.index[tokens[i]][file_num] = []
                elif file_num not in self.index[tokens[i]]:
                    self.index[tokens[i]][file_num] = []
                self.index[tokens[i]][file_num].append(i)

    def file_name(self, num: int):
        name = "0" * (5 - int(math.log10(num))) + str(num)
        return name

    def readFiles(self, start: int, end: int,  dir=None) -> None:
        for i in range(start, end + 1):
            f_name = self.file_name(i)
            f = open(os.path.join(self.path, f_name),
                     'r', encoding='utf-8').read()
            # print(f)
            self.tokenize_add_index(f, f_name)

    def make_it_pretty_ffs(self) -> None:
        f = open('output.txt', 'w+')
        for key, value in sorted(self.index.items(), key=lambda x: x[0]):
            # print(key, end='       ')
            f.write("{} ({}) ==> {{".format(key, len(value)))
            for nestkey, nestvalue in value.items():
                f.write(f"{nestkey} = {len(nestvalue)}, ")
            f.write("}\n")
            # print('\n')
        f.close()

    def main(self):
        i = 0
        while i < 1:
            self.start = i * 500 + 1
            self.end = self.start + 500
            start = time.time()
            self.readFiles(self.start, self.end)
            idx = open(f'index_{i}.txt', 'w+')
            for key, value in sorted(self.index.items(), key=lambda x: x[0]):
                idx.write("{} : {}\n".format(key, value))
            end = time.time()
            print("time taken to create sorted index:", end - start)
            idx.close()
            i += 1
        # self.make_it_pretty_ffs()
        # print(self.index)


if __name__ == '__main__':
    start = 1
    end = 1000
    path = None
    # start = int(sys.argv[1])
    # end = int(sys.argv[2])
    # path = None
    # if len(sys.argv) > 3:
    #     path = sys.argv[3]
    invidx = InvertedIndex(start, end, path)
    invidx.main()
