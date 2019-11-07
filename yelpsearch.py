import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from textblob import TextBlob
from collections import Counter 
from flask import Flask, redirect, render_template, request, session, url_for

## PROCESS DATA
resturant_name = []
resturant_id = []
api_key= "RZMGNepw-0uL71Ur4gG4bCh6gCVFCy5SXZrzV7vJBTYnTu7z6JFf_ZgIQ0DMAl-r9WdOfKzT-vkgm2LCKFZQu-dyY1MzmQnQQARbmqHqJm7irB4LupeKX04lH6W9XXYx"
headers = {'Authorization': 'Bearer %s' % api_key}
area =["newyork", "hoboken","newport", "westnewyork","fortlee"]  # limit the area to vicinity
url = 'https://api.yelp.com/v3/businesses/search'
for address in area:
    params = {'term':'dinner','location':address,'limit':50}
    req = requests.get(url, params=params, headers=headers)
    parsed = json.loads(req.text)
    businesses = parsed["businesses"]
    for business in businesses:
        resturant_name.append(business["name"])
        resturant_id.append(business["id"])  
resturant_name = set(resturant_name)
resturant_id = set(resturant_id)
database = dict(zip(resturant_name,resturant_id))

## FLASK
app = Flask(__name__, template_folder='templates')

@app.route('/yelpsearch', methods=['GET', 'POST'])
def yelpsearch():
    error = None
    if request.method == 'POST':
        all_services = {'service': ['adj','noun','translate','rate','positive','negative']}
        if request.form['service'] not in all_services['service']:
            error = 'Invalid Service. Please try again.'
        else:  # match input restaurant name with database 
            name = request.form['name']
            if name in database.keys():
                url="https://api.yelp.com/v3/businesses/" + str(database[name]) + "/reviews"    
                results = requests.get(url, headers = headers)
                parsed = json.loads(results.text)
                reviews = parsed["reviews"]
                url = reviews[0]["url"]
                page_review = requests.get(url)
                page_soup = BeautifulSoup(page_review.content, features = 'lxml')
                page_return = page_soup.find_all("span", attrs = {"class":"lemon--span__373c0__3997G","lang" :"en"})
                allreview = []
                for perreview in page_return:
                    allreview.append(perreview.text)
                allreview = str(allreview)
                allreview = allreview.replace(r'\xa0', ' ')
                # now we get all reviews of the restaurant you entered

                ## SERVICE 1: translate all reviews into Chinese
                blob = TextBlob(allreview)
                if request.form['service'] == 'translate':
                    chinese_blob = blob.translate(from_lang='en', to='zh-CN')
                    return render_template('success.html',name=chinese_blob)
                
                ## SERVICE 2: get the overall rating based on the sentiment score of all reviews
                if request.form['service'] == 'rate':
                    score_blob = blob.sentiment.polarity
                    return render_template('success.html',name=score_blob)

                ## SERVICE 3: top 10 most frequent words (adj only)
                reviewpos = blob.pos_tags
                if request.form['service'] == 'adj':
                    adj=[]
                    for item in reviewpos:
                        if item[1] in ["JJ", "JJR", "JJS"]:
                            adj.append(item[0])
                    sorted_adj = Counter(adj).most_common(10)
                    return render_template('success.html',name=sorted_adj)
                
                ## SERVICE 4: top 10 most frequent words (noun only)
                if request.form['service'] == 'noun':
                    noun = []
                    for item in reviewpos:  
                        if item[1] == "NN":
                            noun.append(item[0])
                    sorted_noun = Counter(noun).most_common(10)
                    return render_template('success.html',name=sorted_noun)
                
                ## SERVICE 5-6
                if request.form['service'] == 'positive' or request.form['service'] == 'negative':
                    np = blob.noun_phrases
                    f_cs = []
                    for i in np:
                        i = ''.join(i)
                        blob = TextBlob(i)
                        f_cs.append([blob.sentiment.polarity, i])
                    f_cs = pd.DataFrame(f_cs)
                    f_cs = f_cs.sort_values(by=0, ascending=False)
                    __re_data = dict()
                    for (i, b) in zip(f_cs[0], f_cs[1]):
                        __re_data[b] = i
                    key = []
                    key2 = []
                
                ## SERVICE 5: top 10 most common positive words
                    if request.form['service'] == 'positive':
                        for i in __re_data:
                            key.append(i)
                        for i in range(len(key)):
                            if i > 9:
                                break
                            key2.append(key[i])
                        return render_template('success.html',name=key2)
                
                ## SERVICE 6: top 10 most common negative words
                    if request.form['service'] == 'negative':                    
                        for i in __re_data:
                            key.append(i)
                        for i in range(len(key)):
                            if i > 9:
                                break
                            key2.append(key[len(key)-i-1])
                        return render_template('success.html',name=key2)
                
                                            
            else:
                error = "Your search of Restaurant Name is not valid."

    return render_template('home.html', error=error)


if __name__ == "__main__":
    app.run(port=5000, debug=True)