# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 18:16:54 2021

@author: Kevin
"""

import requests

import praw


auth = requests.auth.HTTPBasicAuth('shufDH8eeJfC42Cn7P0NaA', 'L-LG-kVZWNauGiAoBWp5Dvgyh6SYAg')

data = {'grant_type':'password',
        'username' : '<USERNAME>',
        'password':'<PASSWORD>'}

headers = {'User-Agent': 'win64 : text_nlp_gather v1.0.0 by /u/theauknet'}

res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

oauth = res.json()['access_token']


headers = {**headers, **{'Authorization': f"bearer {oauth}"}}


requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

##Function that takes a list of strings with subreddit names and returns titles and comment text

def title_import(subreddits:list, number = '10', sort = '/hot'):
    jsons = []
    titles = []
    
    for sub in subreddits:
        r = requests.get('https://oauth.reddit.com'+sub+sort, headers=headers, params={'limit':number})
        jsons.append(r)
    for json in jsons:
        for post in json.json()['data']['children']:
            titles.append(post['data']['url'])
            
    return titles  
      
titlelist = title_import(['/r/bitcoin'])
print(titlelist)

reddit = praw.Reddit(user_agent="win64 : text_nlp_gather v.1.0.0 by /u/theauknet", client_id="shufDH8eeJfC42Cn7P0NaA",
                     client_secret="L-LG-kVZWNauGiAoBWp5Dvgyh6SYAg", username="<USERNAME>", password="<PASSWORD>",)


def comment_scrape(urls:list):
    for url in urls:
        address = url
        if address[0:18] == 'https://www.reddit':
            submission = reddit.submission(url=address)
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                print(comment.body)
        else:
            pass


comment_scrape(titlelist)