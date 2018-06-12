#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
__author__ = "Helena Montserrat Gómez Adorno"
__email__ = "helena.adorno at gmail dot com"

"(1) Gómez-Adorno, H., Aleman, Y., Vilariño, D., Sanchez-Perez, M. A., Pinto, D., & Sidorov, G. Author Clustering using Hierarchical Clustering Analysis in CLEF 2017 Working Notes. CEUR Workshop Proceedings, 2017"

import sys, os, codecs, re, string, math, time, json, operator, argparse, glob
import bcubed
import numpy as np
import scipy.sparse as sp 
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import fcluster
from gensim.matutils import Scipy2Corpus,corpus2csc
from gensim.models.logentropy_model import LogEntropyModel
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import silhouette_score, calinski_harabaz_score
from extractTypedNgrams import typedNgrams
from featuresExtraction import wordsVector, wordsNgrams, characterNgrams, stylometricFeatures

#########################################################################################
def computeBcubed(title, cdict, ldict):
    """Compute extended BCubed precision and recall, and print the results."""
    precision = bcubed.precision(cdict, ldict)
    recall = bcubed.recall(cdict, ldict)
    fscore = bcubed.fscore(precision, recall)

    return precision, recall, fscore

#########################################################################################
def bcubedInput(target, clDic):
    gsId = 0
    goldStandard={}
    clustering={}
    for gs in target:
        gsId +=1
        goldStandard[gs[0]]= set()
        goldStandard[gs[0]].add(str(gs[1]))
    clId = 0
    for cl in clDic:
        clId +=1
        clustering[cl[0]] = set(str(cl[1]))
    return clustering, goldStandard
        
#########################################################################################

def linkageCluster(X, n, evalType='calinski'):
    # generate the linkage matrix
    Y=pdist(X, metric='cosine')
    
    Z = linkage(Y, 'average',)
    range_n_clusters = range(2,int((n/2)+1))
    
    sil_list={}
    for n_clusters in range_n_clusters:
        # Initialize the clusterer with n_clusters value and a random generator
        # seed of 10 for reproducibility
        clusters = fcluster(Z, n_clusters, criterion='maxclust')
        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        if evalType == 'silhouette':
            silhouette_avg = silhouette_score(X, clusters)
        else:
            silhouette_avg = calinski_harabaz_score(X, clusters)
        sil_list[n_clusters]=silhouette_avg
        
    #order the cluster according to the evaluation measure
    sil_list=sorted(sil_list.items(), key=lambda x: x[1], reverse=True)
    #the maximum number of cluster is the one with the best evaluation score
    n_cluster=sil_list[0][0]
    
    clusters = fcluster(Z, n_cluster, criterion='maxclust')
    
    return clusters

#########################################################################################

def kmeansCluster(X,n,n_init=10,evalType='silhouette'):
    
    range_n_clusters = range(2,int((n/2)+1))
    sil_list={}
    for n_clusters in range_n_clusters:
        # Initialize the clusterer with n_clusters value and a random generator
        # seed of 10 for reproducibility
        clusterer = KMeans(n_clusters=n_clusters)
        clusters =  clusterer.fit_predict(X)
        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        if evalType == 'silhouette':
            silhouette_avg = silhouette_score(X, clusters)
        else:
            silhouette_avg = calinski_harabaz_score(X, clusters)
        sil_list[n_clusters]=silhouette_avg
        
    sil_list=sorted(sil_list.items(), key=lambda x: x[1], reverse=True)
    n_cluster=sil_list[0][0]
    
    clusterer = KMeans(n_clusters=n_cluster)
    clusters =  clusterer.fit_predict(X)
    return clusters
    
#########################################################################################

def generateClusteringFile(clustering, outfileDir):
    #generate cluster output files
    outputfile=codecs.open(outfileDir+'/clustering.json','w',encoding="utf-8")
    outputfile.write('[\n')
    i=0
    top=len(clustering)
    for c in clustering:
        i+=1
        outputfile.write('\t[\n')
        maxDoc=len(clustering[c])
        j=0
        for d in clustering[c]:
            j+=1
            if j == maxDoc:
                outputfile.write('\t\t{"document"'+': "'+d+'"}\n')
            else:
                outputfile.write('\t\t{"document"'+': "'+d+'"},\n')
        if i==top:
            outputfile.write('\t]\n')
        else:
            outputfile.write('\t],\n')
    outputfile.write(']\n')
    outputfile.close()

#########################################################################################

def generateRankingsFile(cos_mat, doc_vecs, outfileDir):
    #generate rankings output files
    outputfile=codecs.open(outfileDir+'/ranking.json','w',encoding="utf-8")
    outputfile.write('[\n')
    LinksScore=[]
    i=0
    top=len(cos_mat)
    cos_dict={}
    for (i,j), value in np.ndenumerate(cos_mat):
        cos_dict[(doc_vecs[i],doc_vecs[j])]=value
    cos_dict=sorted(cos_dict.items(), key=operator.itemgetter(1), reverse=True)
    for docs in cos_dict:
        i+=1
        d1=docs[0][0]
        d2=docs[0][1]
        outputfile.write('\t{"document1"'+': "'+d1+'",\n')
        outputfile.write('\t"document2"'+': "'+d2+'",\n')
        outputfile.write('\t"score"'+': '+str(docs[1])+'}')
        LinksScore.append((d1,d2))
        if i==top:
            outputfile.write('\n')
        else:
            outputfile.write(',\n')
    outputfile.write(']\n')
    outputfile.close()
    
    return LinksScore

#########################################################################################

def relevant(li,T):
    if (li[0],li[1]) in T or (li[1],li[0]) in T:
        return 1
    else:
        return 0

#########################################################################################

def precision(i, L, T):

    pr=0
    for j in range(0,i+1):
        re=relevant(L[j], T)
        pr+=float(re)
    pr=pr/(i+1)

    return pr
  
#########################################################################################
  
def averagePrecision(TrueLinks,LinksScore):
    
    ap=0
    for i in range(0,len(LinksScore)):
        p=precision(i,LinksScore, TrueLinks)
        r=relevant(LinksScore[i],TrueLinks)
        ap+=(p*r)
        
    return ap/len(TrueLinks)

#########################################################################################

def readCorpus(input):
    #Variable that contains the dictionary of files in each subdirectories of the train corpus 
    DicProblem  = {}  
    DicCluster = {}
    DicLink = {}
    
    #Reading the Training Corpus
    for directory in os.listdir(input):
        #reading problem files
        if directory[0] == "p": 
            files  =[]
            for item in os.listdir(input+"/"+directory):
                if os.path.splitext(item)[1] == ".txt":
                    files.append(input+"/"+directory+"/"+item)
            DicProblem[directory]=files
        #reading truth files
        elif directory[0] == "t":
            files = {}
            for dirInTruth in os.listdir(input+"/"+directory):
                for item in glob.glob(os.path.join(input+"/"+directory+"/"+dirInTruth, '*')):
                    #for each problem, read the clusters and the ranking gold standards
                    if "clustering.json" in item:
                        with open(item) as data_file:
                            data = json.load(data_file)
                        i=1
                        gold=[]
                        for dat in data:
                            for documents in dat:
                                for doc in documents.values():
                                    gold.append((str(doc),i))
                            i+=1
                        DicCluster[dirInTruth]=gold
                    elif "ranking.json" in item:
                        TrueLinks=set()
                        with open(item) as data_file:
                            dataR = json.load(data_file)
                        i=1
                        gold=[]
                        for dat in dataR:
                            d1=str(dat['document1'])
                            d2=str(dat['document2'])
                            TrueLinks.add((d1,d2))
                            i+=1
                        DicLink[dirInTruth]=TrueLinks
    return DicProblem, DicCluster, DicLink

#########################################################################################

def main(input,output, clusterAlg, weight, numFeat):
    #Reading corpus
    DicProblem, DicCluster, DicLink = readCorpus(input)
    print "Clustering with",numFeat,"features..."
    N=numFeat
    cont, spr, sre, sfs, sav = 0,0,0,0,0
    #Extraing features of documents
    for directory in DicProblem:
        print directory 
        #Vectores de caracteristicas por documento
        doc_vecs={}
        for filen in DicProblem[directory]:
            with codecs.open(filen, encoding="utf-8") as fid:
                filename=filen.split('/')[-1]
                text = fid.read()
                #character n-grams
                vec=dict(characterNgrams(text,2))
                vec.update(dict(characterNgrams(text,3)))
                vec.update(dict(characterNgrams(text,4)))
                vec.update(dict(characterNgrams(text,5)))
                vec.update(dict(characterNgrams(text,6)))
                vec.update(dict(characterNgrams(text,7)))
                vec.update(dict(characterNgrams(text,8)))
                #word n-grams
                vec.update(dict(wordsVector(text)))
                vec.update(dict(wordsNgrams(text,2)))
                vec.update(dict(wordsNgrams(text,3)))
                #character typed n-grams
                vec.update(dict(typedNgrams(text,3)))
                vec.update(dict(typedNgrams(text,4)))
                #stylometric features
                vec.update(stylometricFeatures(text))
                
                doc_vecs[filename] = vec
        
        #transform into matrix of n samples and m features
        v = DictVectorizer()
        X = v.fit_transform(doc_vecs.values())
        
        #Keeping feature above threshold N
        #sum all values in column
        values=np.sum(X,axis=0)
        #get indices of the N most common values
        #print "Max features",len(values.getA()[0])
        indices=np.argsort(values[0],axis=1)[0,-N:]
        #select columns with the indices list
        X=X[:,indices.getA()[0]]
        ndoc,nterm=X.shape
        
        #applying weighting scheme
        if weight == 'logEnt':
            Xc = Scipy2Corpus(X)
            log_ent=LogEntropyModel(Xc)
            X=log_ent[Xc]
            X=corpus2csc(X,num_terms=nterm,num_docs=ndoc)
            X=sp.csc_matrix.transpose(X)
        elif weight == 'tfidf':
            transformer = TfidfTransformer()
            X = transformer.fit_transform(X)

        X=X.toarray()
        
        if clusterAlg == 'hierarchical' :
            clusters=linkageCluster(X,len(doc_vecs))
        else:#kmeans
            clusters=kmeansCluster(X,len(doc_vecs))
        
        clustering=[]
        for i in range(len(clusters)):
            clustering.append((doc_vecs.keys()[i],clusters[i]))
            
        outfileDir=output+'/'+directory
        if not os.path.exists(outfileDir):
            os.mkdir(outfileDir)
        
        #Evaluation measures
        clDict, goldDict=bcubedInput(DicCluster[directory],clustering)
        pr, re, fs= computeBcubed("Prueba", clDict, goldDict)
                    
        #generate clustering output files
        clusteringOut={}
        for i in range(len(clusters)):
            clusteringOut.setdefault(clusters[i],[]).append(doc_vecs.keys()[i])
        generateClusteringFile(clusteringOut,outfileDir)
        
        #calculate cosine similarity
        cos_mat=cosine_similarity(X)
        LinksScore=generateRankingsFile(cos_mat,doc_vecs.keys(),outfileDir)
        av=averagePrecision(DicLink[directory], LinksScore)
        cont+=1
        spr+=pr
        sre+=re
        sfs+=fs
        sav+=av
    print "Number of features", N, "Mean F-Score", sfs/cont, "MAP", sav/cont


#########################################################################################
if __name__ == '__main__':        
    t0 = time.time()
    #Execute the program as follows:
    #python clusterAuthors.py -i Training2017 -o Output
    #> myTrainingSoftware -i path/to/training/corpus -o path/to/output/directory
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Author Clustering system for PAN 2017 shared task.')
    parser.add_argument('-i', type=str, help='Path to the main folder of a collection of attribution problems')
    parser.add_argument('-o', type=str, help='Path to an output folder')
    parser.add_argument('-c', type=str, default='hierarchical', help='Clustering algorithm: hierarchical o kmeans')
    parser.add_argument('-w', type=str, default='logent', help='Weighting scheme: logEnt (Log-Entropy), tfidf, tf (Term Frequency)')
    parser.add_argument('-n', type=int, default=20000, help='Threshold of number of features. Default 20000')
    args = parser.parse_args()
    if not args.i:
        print('ERROR: input (-i) option missing. Use the next syntaxis')
        print 'clusterAuthors.py -i path/to/training/corpus -o path/to/output/directory'
        parser.exit(1)
    if not args.o:
        print('ERROR: output (-o) option missing. Use the next syntaxis')
        print 'clusterAuthors.py -i path/to/training/corpus -o path/to/output/directory'
        parser.exit(1)   
    if not (args.c == 'hierarchical' or args.c == 'kmeans') :
        print('ERROR: Valids clusterings algorithms are: hierarchical or kmeans')
        parser.exit(1)   
    if not (args.w == 'logEnt' or args.w == 'tfidf' or args.w == 'tf') :
        print('ERROR: Valids clusterings algorithms are: LogEnt, tfidf or tf')
        parser.exit(1)  
        
    if not os.path.exists(args.i):
        print "Path doesn't exist: "+args.i
        exit(1)  
    if not os.path.exists(args.o):
        os.mkdir(args.o)                                             

    print "Input path: " + args.i
    print "Output path: "+ args.o
    
    clusterAlg = args.c
    weight = args.w
    numFeat = args.n
    
    main(args.i, args.o, clusterAlg, weight, numFeat)
    print "Done. Time taken:", time.time() - t0
