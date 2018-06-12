#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Ilya Markov"
__email__ = "markovilya at yahoo dot com"

" (1) Markov, Ilia, Efstathios Stamatatos, and Grigori Sidorov. Improving cross-topic authorship attribution: The role of pre-processing. Proceedings of the 18th International Conference on Computational Linguistics and Intelligent Text Processing. CICLing. 2017."

from collections import Counter
import re, string

def typedNgrams(file_content,n):
    ngramCounter = Counter()

    file_content = digits(file_content)
    tokens = []
    #words
    file_content1 = cleaning_text(file_content)

    #typed
    if n == 3:
        tokens.append(prefix(file_content1, n))
        tokens.append(suffix(file_content1, n))
        tokens.append(space_prefix(file_content, n))
        tokens.append(space_suffix(file_content, n))
        tokens.append(multi_word(file_content1, n))
        tokens.append(whole_word(file_content1, n))
        tokens.append(mid_word(file_content1, n))
        tokens.append(beg_punct(file_content, n))
        tokens.append(mid_punct(file_content1))
        tokens.append(end_punct(file_content, n))
    elif n == 4:
        tokens.append(prefix(file_content1, n))
        tokens.append(suffix(file_content1, n))
        tokens.append(space_prefix(file_content, n))
        tokens.append(space_suffix(file_content, n))
        tokens.append(multi_word(file_content1, n))
        tokens.append(whole_word(file_content1, n))
        tokens.append(mid_word(file_content1, n))
        tokens.append(beg_punct(file_content, n))
        tokens.append(end_punct(file_content, n))
    
    result = sum(tokens, [])
    ngramCounter.update(result)
    
    return ngramCounter

def cleaning_text(file_content):
    
    punctuation = string.punctuation
    for c in punctuation:
        file_content = file_content.replace(c, ' %s '%c)
    file_content = re.sub('\s{2,}', ' ', file_content)
    
    return file_content

def digits(file_content):
    file_content =re.sub('\d+', '0', file_content)  
    
    return file_content


def prefix(file_content1, n):

    prefixes = []
    for token in file_content1.split():
        if len(token) > n:
            prefix = token[:n]
            prefixes.append(prefix + "pr" + str(n))
                
    return prefixes

############################################################

def suffix(file_content1, n):

    suffixes = []
    for token in file_content1.split():
        if len(token) > n:
            suffix = token[-n:]
            suffixes.append(suffix + "su" + str(n))
                
    return suffixes

############################################################

def space_prefix(file_content, n):
    
    space_prefixes = []
    for tokens in file_content.split('\n'):
        for token in tokens.split()[1:]:
            if n == 3:
                if len(token) > n-2 and token[0] not in string.punctuation and token[1] not in string.punctuation:
                    spacetwo = token[:n-1]
                    space_prefixes.append("_" + spacetwo + "sp" + str(n))
                if len(token) == n-2 and token[0] not in string.punctuation:
                    space_prefixes.append("_" + token + "_" + "sp" + str(n))
            else:
                if len(token) > n-2 and token[0] not in string.punctuation and token[1] not in string.punctuation and token[2] not in string.punctuation:
                    spacetwo = token[:n-1]
                    space_prefixes.append("_" + spacetwo + "sp" + str(n))
                if len(token) == n-2 and token[0] not in string.punctuation and token[1] not in string.punctuation:
                    space_prefixes.append("_" + token + "_" + "sp" + str(n))
                                    
    return space_prefixes
    
############################################################ 

def space_suffix(file_content, n):
    
    space_suffixes = []
    for tokens in file_content.split('\n'):
        for token in tokens.split()[:-1]:
            if n == 3:
                if len(token) > n-2 and token[-1] not in string.punctuation and token[-2] not in string.punctuation:
                    twospace = token[-(n-1):]
                    space_suffixes.append(twospace + "_" + "ss" + str(n))
            else:
                if len(token) > n-2 and token[-1] not in string.punctuation and token[-2] not in string.punctuation and token[-3] not in string.punctuation:
                    twospace = token[-(n-1):]
                    space_suffixes.append(twospace + "_" + "ss" + str(n))    
                    
    return space_suffixes
    
############################################################ 
    
def multi_word(file_content1, n):
    
    multi_words = []
    tokens = file_content1.split()
    
    for i in range(len(tokens)-1):
        if tokens[i+1][0] in string.punctuation:
            i = i + 1
        elif tokens[i][-1] in string.punctuation:
            i = i + 1
        else:        
            if n == 3:
                tokenlast = tokens[i][-1]
                tokenfirst = tokens[i+1][0]
                
                multi = tokenlast + "_" + tokenfirst
                multi_words.append(multi + "mu" + str(n))
                i = i + 1
            else:
                if len(tokens[i]) == 1: 
                    tokenlast = tokens[i][-1]
                    tokenfirst = tokens[i+1][0]
                    
                    multi = tokenlast + "_" + tokenfirst
                    multi_words.append(multi + "mu" + str(n))
                    i = i + 1
                    
                elif len(tokens[i]) > 1 and tokens[i][-1] not in string.punctuation and tokens[i][-2] in string.punctuation:
                    tokenlast = tokens[i][-1:]
                    tokenfirst = tokens[i+1][0]
        
                    multi = tokenlast + "_" + tokenfirst
                    multi_words.append(multi + "mu" + str(n))
                    i = i + 1    
                    
                elif len(tokens[i]) > 1 and tokens[i][-1] not in string.punctuation and tokens[i][-2] not in string.punctuation:
                    tokenlast = tokens[i][-2:]
                    tokenfirst = tokens[i+1][0]
        
                    multi = tokenlast + "_" + tokenfirst
                    multi_words.append(multi + "mu" + str(n))
                    
                    i = i + 1
    return multi_words

###########################################################

def whole_word(file_content1, n):
    
    whole_words = []
    for token in file_content1.split():
        if len(token) == n:
            whole_word = token[:]
            whole_words.append(whole_word + "wh" + str(n))
            
    return whole_words

############################################################

def mid_word(file_content1, n):
    
    mid_words = []
    for token in file_content1.split():
        if len(token) > n+1:
            stripfirstlsat = token[1:-1]
            i = 0
            for mid in stripfirstlsat:
                mid = stripfirstlsat[i:i+n]
                i = i + 1
                if len(mid) == n:
                    mid_words.append(mid + "mi" + str(n))
                    
    return mid_words

############################################################

def beg_punct(file_content, n):
    
    beg_puncts = []
    for tokens in file_content.split('\n'):
        for i in range(0, len(tokens)-(n-1)):
            beg_punct = tokens[i:i+n]
            if n == 3:
                if beg_punct[0] in string.punctuation and beg_punct[1] not in string.punctuation:    
                    beg_puncts.append(beg_punct + "bp" + str(n))
            else:
                if beg_punct[0] in string.punctuation and beg_punct[1] not in string.punctuation and beg_punct[2] not in string.punctuation:    
                    beg_puncts.append(beg_punct + "bp" + str(n))
                    
    return beg_puncts

############################################################

def mid_punct(file_content1):
    
    mid_punct = []
    for token in file_content1.split():
        if token in string.punctuation: 
            mid_punct.append(token + 'mp3')
            
    return mid_punct

###########################################################    

def end_punct(file_content, n):
    
    end_puncts = []
    for tokens in file_content.split('\n'):
        for i in range(0, len(tokens)-(n-1)):
            end_punct = tokens[i:i+n]
            if n == 3:
                if end_punct[-1] in string.punctuation and end_punct[0] not in string.punctuation and end_punct[1] not in string.punctuation:    
                    end_puncts.append(end_punct + "ep" + str(n))
            else:
                if end_punct[-1] in string.punctuation and end_punct[0] not in string.punctuation and end_punct[1] not in string.punctuation and end_punct[2] not in string.punctuation:   
                    end_puncts.append(end_punct + "ep" + str(n))
                    
    return end_puncts
