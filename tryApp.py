#
from sklearn.feature_extraction.text import TfidfVectorizer
import pymongo
from flask import Flask, request, render_template, flash
from flask_paginate import Pagination, get_page_args
import mysql.connector
from mysql.connector import Error
import re
import string 
import numpy as np
import pandas as pd
# create app instance
app = Flask(__name__)


import requests
from bs4 import BeautifulSoup


#extracts all paragraphs from websites and preprocess them to be vectorized
def ParagrahExtractor(listOfLinks):
    documents = []
    for i in listOfLinks:
        # Make a request to the link
        r = requests.get(i)
  
        # Initialize BeautifulSoup object to parse the content 
        soup = BeautifulSoup(r.text, 'html.parser')
  
        # Retrieve all paragraphs and combine it as one
        sen = [] #find('div', {'class':'read__content'})
        for i in soup.find_all('p'):
            sen.append(i.text)
  
        # Add the combined paragraphs to documents
        documents.append(' '.join(sen))
        
        
        
    documents_clean = []
    for d in documents:
        # Remove Unicode
        document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
        # Remove Mentions
        document_test = re.sub(r'@\w+', '', document_test)
        # Lowercase the document
        document_test = document_test.lower()
        # Remove punctuations
        document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
        # Lowercase the numbers
        document_test = re.sub(r'[0-9]', '', document_test)
        # Remove the doubled space
        document_test = re.sub(r'\s{2,}', ' ', document_test)
        documents_clean.append(d)
        
    return documents_clean

#this functions searches fro similart results to putput depending in the query

def get_similar_articles(q, df, vectorizer, doc):
    print("query:", q)
    print("Here are the most useful results: ")
    # Convert the query become a vector
    q = [q]
    q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
    sim = {}
    # Calculate the similarity
    for i in range(10):
        sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
  
    # Sort the values 
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    
    # Print the articles and their similarity values
    connection = mysql.connector.connect(host='localhost',database='MY_CUSTOM_BOT',user='root',password='Soyunaloca1',
                                    auth_plugin='caching_sha2_password')
    
    for k, v in sim_sorted:
        if v != 0.0:
            iD = doc[k][0]
            
            if connection.is_connected():
                cursor = connection.cursor()
                query  = "SELECT link FROM url_table WHERE ID = %s LIMIT 10"
                cursor.execute(query, [(iD)])
                links = []
                for link in cursor:
                    links.append(link)
                cursor.close()
                connection.close()
            
            
    return links
            


@app.route('/')
def home():
    if 'search' in request.args:
        
        connection = mysql.connector.connect(host='localhost',
                                         database='MY_CUSTOM_BOT',
                                         user='root',
                                         password='Soyunaloca1',
                                         auth_plugin='caching_sha2_password')
        
        if connection.is_connected():
            cursor = connection.cursor()
            """
            This is basically just displaying all the finds at the end after the user hist search.
            This part will be done only after the vectorizer is applied so that only the most relevant
            results are show
            """
            #client.execute("select database();")
            #record = cursor.fetchone()
            #print("You're connected to database: ", record)
        
        #connect_uri = 'mongodb+srv://cmk:342124@todolist-c483l.gcp.mongodb.net/search?retryWrites=true&w=majority'
        #client = pymongo.MongoClient(connect_uri)
        
            
        # create db client
      

            query = { '$text': {'$search': request.args.get('search')} }
            sql = "select URL from urls_table where key_word like %s"
            cursor.execute(sql,("%"+query +"%",))
            search_results = cursor.fetchall()
        
        for entry in search_results:
            flash(entry, 'success')
        
        # close connection
        connection.close()
        cursor.colse()


    return render_template('search.html')










@app.route('/search_results')
def search_results():
    if 'search' in request.args:
        
        
        connection = mysql.connector.connect(host='localhost',database='MY_CUSTOM_BOT',
                                             user='root',password='Soyunaloca1',
                                             auth_plugin='caching_sha2_password')
        
        cursor = connection.cursor()
    
        #description column is tbd based on the new name of the database
        query = { '$text': {'$search': request.args.get('search')} }
        
        sql = "select URL from urls_table where key_word like %s limit 8"
        cursor.execute(sql,("%"+query +"%",))
        search_results = cursor.fetchall()
        links = []
        for link in search_results:
            links.append(link[0])
        
        
        doc = ParagrahExtractor(links)
        vectorizer = TfidfVectorizer()
        # It fits the data and transform it as a vector
        X = vectorizer.fit_transform(doc)
        # Convert the X as transposed matrix
        X = X.T.toarray()
        # Create a DataFrame and set the vocabulary as the index
        df = pd.DataFrame(X, index=vectorizer.get_feature_names())
        search_results = get_similar_articles(query, df, vectorizer, doc)
        
        """
        connect_uri = 'mongodb+srv://cmk:342124@todolist-c483l.gcp.mongodb.net/search?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)
        
        # create db client
        db = client.search

        query = db.search_results.find({ '$text': {'$search': request.args.get('search')} })
        search_results = []
        
        for doc in query:
            search_results.append(doc)
        
        # close connection
        client.close()
        """
        # automatic pagination handling
        total = len(search_results)
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
        return render_template('search_results.html',
                                search_results=search_results[offset: offset + per_page],
                                page=page,
                                per_page=per_page,
                                pagination=pagination,
                                len=len)



if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True, threaded=True)

    
    
    
    
    
    





            