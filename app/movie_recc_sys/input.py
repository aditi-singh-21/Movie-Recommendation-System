import pandas as pd
import numpy as np
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize

nltk.download("stopwords")
stope_words_set = set(stopwords.words("english"))

def remove_stop_words(summary):
    flag = 0
    summary_word_token = word_tokenize(summary)
    updated_summary = ""
    for w in summary_word_token:
        if w not in stope_words_set:
            if flag == 1:
                updated_summary = updated_summary + " " + w
            else:
                updated_summary = w
                flag = flag +1
    #print(updated_summary)
    return updated_summary

def input_encoding(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.google.com/',
}

    response = requests.get(url, headers=headers , timeout=15)
    response.raise_for_status()

    sample_soup = BeautifulSoup(response.text, 'html.parser')
    
    encoded = []
    
    #Name
    '''sample_name = sample_soup.find('h1' ,{'class' : 'sc-d8941411-0 dxeMrU'})
    sample_name = sample_name.find('span' ,{'class' : 'hero__primary-text'}).text
    encoded.append(sample_name)
    print(sample_name)
    
    
    #Rating
    encoded.append(sample_soup.find('span',{'class':'sc-eb51e184-1 cxhhrI'}).text)
    print(sample_soup.find('span',{'class':'sc-eb51e184-1 cxhhrI'}).text)
    
    #Year
    year_duration = sample_soup.find('ul',{'class' : 'ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt'})
    year_duration = year_duration.find_all('li',{'class':'ipc-inline-list__item'})
    flag=0
    for item in year_duration:
        if flag == 0:
            sample_year=item.text
            encoded.append(sample_year)
            print(sample_year)
            flag = flag+1
    ''' 
    #Genre
    sample_genre=[]
    input_string =""
    sample_genre_tag = sample_soup.find('div',{'class':'ipc-chip-list__scroller'})
    sample_genre_tag = sample_genre_tag.find_all('a',{'class':'ipc-chip ipc-chip--on-baseAlt'})
    for item in sample_genre_tag:
        g = item.find('span',{'class':'ipc-chip__text'}).text
        sample_genre.append(g)
    if(len(sample_genre) == 1):
        sample_genre.append(sample_genre[0])
        sample_genre.append(sample_genre[0])
    elif(len(sample_genre) == 2):
        sample_genre.append(sample_genre[0])
    encoded.append(sample_genre)
    for item in encoded:
        input_string = input_string + str(item)
    return input_string
  
    
    #Summary
    '''
    sample_intro = sample_soup.find('p' , {'class' : 'sc-2d37a7c7-3 dmZChI'})
    sample_intro = sample_intro.find('span' , {'class' : 'sc-2d37a7c7-0 caYjFF'}).text
    encoded.append(remove_stop_words(sample_intro))
    print(remove_stop_words(sample_intro))
    '''
    
            
def vectorization(corpus):
    vectorize = TfidfVectorizer(stop_words="english")
    vectorize_matrix = vectorize.fit_transform(corpus)
    return vectorize_matrix, vectorize
            
            
def find_similar_movies(vectorize_matrix, input_vector, movies_name, top_n=10):
    cosine_sim = cosine_similarity(input_vector, vectorize_matrix)
    similar_indices = cosine_sim.argsort().flatten()[-top_n:]
    similar_movies = [movies_name[idx] for idx in similar_indices]
    return similar_movies
        
def get_imp_features(df):
    important_features =[]
    for i in df.index:
        important_features.append(str(df['Genre List'][i]))
    return important_features
   
def similar(url):
    df = pd.read_csv(r'C:\Users\aditi\OneDrive\Desktop\PROJECTS\Movie-Recommendation-System\final_dta.csv')
    with open(r'C:\Users\aditi\OneDrive\Desktop\PROJECTS\Movie-Recommendation-System\movies_name.txt', 'wb') as file:
        pickle.dump(df['Movie Name'],file) 
    with open(r'C:\Users\aditi\OneDrive\Desktop\PROJECTS\Movie-Recommendation-System\movies_name.txt', 'rb') as file:
        movies_name = pickle.load(file , encoding='utf-8') 
    df['Important Features'] = get_imp_features(df)

    sample_movie = input_encoding(url)
    corpus = list(df['Important Features']) + [sample_movie]
    vectorize_matrix, vectorize = vectorization(corpus)
    input_vector = vectorize_matrix[-1]
    vectorize_matrix = vectorize_matrix[:-1]
    return find_similar_movies(vectorize_matrix,input_vector,movies_name)

def input_mov(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.google.com/',
}

    response = requests.get(url, headers=headers , timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    
    input_mov = []
    
    title = soup.find('div' ,{'class':'sc-491663c0-3 bdjVSf'})
    title = title.find('span' ,{'class' : 'hero__primary-text'}).text
    input_mov.append(title)
    return input_mov
