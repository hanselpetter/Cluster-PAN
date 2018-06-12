#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Helena Montserrat Gómez Adorno and Yuridiana Alemán"
__email__ = "helena.adorno at gmail dot com"

"(1) Gómez-Adorno, H., Aleman, Y., Vilariño, D., Sanchez-Perez, M. A., Pinto, D., & Sidorov, G. Author Clustering using Hierarchical Clustering Analysis in CLEF 2017 Working Notes. CEUR Workshop Proceedings, 2017"
"(2) Gomez Adorno, H. M., Rios, G., Posadas Durán, J. P., Sidorov, G., & Sierra, G. (2018). Stylometry-based Approach for Detecting Writing Style Changes in Literary Texts. Computación y Sistemas, 22(1)."

import re, string
from collections import Counter

#########################################################################################
def wordsVector(infile_content):
    
    wordCounter = Counter()
    wordlist = []
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    infile_content = regex.sub('', infile_content)
    for word in infile_content.split():
        wordlist.append(word.lower())
    wordCounter.update(wordlist)
    
    return wordCounter

def wordsNgrams(file_content, n):
    
    wordCounter = Counter()
    bigramslist = []
    punctuation = string.punctuation
    for c in punctuation:
        file_content = file_content.replace(c, ' %s '%c)
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    
    for line in file_content.split("."):
        line = regex.sub('', line)

        for i in range(0, len(line.split())-(n-1)):
            bigram = [t.lower() for t in line.split()[i:i+n]]
            
            bigramslist.append('_'.join(bigram))  
    wordCounter.update(bigramslist)
         
    return wordCounter 

#########################################################################################

def characterNgrams(infile_content, n):
    
    untyped = []
    ngramCounter = Counter()
    for line in infile_content.split('\n'):
        for i in range(0, len(line)-(n-1)):
            ngram = line[i:i+n]
            untyped.append(ngram)
    ngramCounter.update(untyped)
    
    return ngramCounter  
    
#########################################################################################

def stylometricFeatures(text):
    
    text=text.replace(u"\u2018", "'").replace(u"\u2019", "'")
    DosPuntos=text.split(":")
    PuntoComa=text.split(";")
    Coma=text.split(",")
    Punto=text.split(".")
    Interrogacion=text.split("?")
    Admiracion=text.split("!")
    text=text.replace("!","").replace("?","").replace(".","").replace(",","").replace(";","").replace(":","")
    Palabras=text.split(" ")
    Mayusc=0
    Digito=0
    Longitud=0
    Frec4=0
    Frec6=0
    for p in Palabras:
        if p != '':
            Longitud=Longitud+len(p)
            if len(p)>6:
                Frec6=Frec6+1
            if len(p)<4:
                Frec4=Frec4+1
            if p[0]== p[0].upper():
                Mayusc=Mayusc+1
            if p.isdigit():
                Digito=Digito+1
    PromLongPalabra=float(Longitud)/float(len(Palabras))
    PromOracPalabra=float(len(Palabras))/float(len(Punto))
    PromOracChar=float(Longitud)/float(len(Punto))
    Voc = dict(wordsVector(text))
    RatioPalabra=float(len(Voc))/float((len(Palabras)))
    FrecUno=0
    for palabra, frec in Voc.iteritems():
        if frec < 2:
            FrecUno=FrecUno+1
    RatioFrecUno=float(FrecUno)/float((len(Palabras)))
    RatioFrec4=float(Frec4)/float((len(Palabras)))
    RatioFrec6=float(Frec6)/float((len(Palabras)))
        
    #all features
    vec={'NumPalabras':len(Palabras)-1, 'LongText':len(text),'DosPuntos':len(DosPuntos)-1,'PuntoComa':len(PuntoComa)-1,'Coma': len(Coma)-1,'Punto':len(Punto)-1,'Interrogacion':len(Interrogacion)-1,'Admiracion':len(Admiracion)-1,'Mayusc': Mayusc,'Digito': Digito,'PromPalabras':PromLongPalabra,'PromOracPalabra':PromOracPalabra,'PromOracChar':PromOracChar,'RatioPalabra':RatioPalabra,'RatioFrecUno':RatioFrecUno,'RatioFrec4':RatioFrec4,'RatioFrec6':RatioFrec6}
    #vec={'PromPalabras':PromLongPalabra,'PromOracPalabra':PromOracPalabra,'PromOracChar':PromOracChar,'RatioPalabra':RatioPalabra,'RatioFrecUno':RatioFrecUno,'RatioFrec4':RatioFrec4,'RatioFrec6':RatioFrec6}
    #vec={'NumPalabras':len(Palabras)-1, 'LongText':len(text),'DosPuntos':len(DosPuntos)-1,'PuntoComa':len(PuntoComa)-1,'Coma': len(Coma)-1,'Punto':len(Punto)-1,'Interrogacion':len(Interrogacion)-1,'Admiracion':len(Admiracion)-1,'Mayusc': Mayusc,'Digito': Digito}

    return vec

