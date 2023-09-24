import pandas as pd
import requests
import time
from datetime import datetime
import os
import warnings
warnings.filterwarnings("ignore")

#obscure inputs
import getpass


# client_id = #alphanumeric string provided under "personal use script"
client_id = 'ZpjnKq7Ab99HyPreJxhCig'
# client_secret =  #alphanumeric string provided as "secret"
client_secret = 'nQeQG8OSqWHX_ibw2ct4DPCNYNSQyw'
# user_agent =  #the name of your application
user_agent = 'LukaDSIProject3'
# username =  #your reddit username
username = 'SwimmingBasic8173'
# password =  #your reddit password
password = 'Penguins87'


auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

data = {
    'grant_type': 'password',
    'username': username,
    'password': password
}



#create an informative header for your application
headers = {'User-Agent': 'DSI626LK/0.0.1'}

res = requests.post(
    'https://www.reddit.com/api/v1/access_token',
    auth=auth,
    data=data,
    headers=headers)

print(res)


res.json()


#retrieve access token
token = res.json()['access_token']



headers['Authorization'] = f'bearer {token}'

requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).status_code == 200



base_url = 'https://oauth.reddit.com/r/'
subreddit = 'nfl'
params = {'limit': 100
          
}

res = requests.get(base_url+subreddit, headers= headers, params = params)



#check out response object
res.json()['data']['children'][0]['data']

#create a dataframe of your submissions
len(res.json()['data']['children'])



def scraper(subreddit, tab):
    base_url = 'https://oauth.reddit.com/r/'
    subreddit = subreddit
    params = {'limit': 100}
    posts = []
    for x in range(0, 10):
        
        res = requests.get(base_url+subreddit+"/"+tab, headers=headers, params = params)
        observation = res.json()
        for  i in range(0, len(observation['data']['children'])):
            text = {}
            text['title'] = observation['data']['children'][i]['data']['title']
            text['subreddit'] = observation['data']['children'][i]['data']['subreddit']
            text['selftext'] = observation['data']['children'][i]['data']['selftext']
            text['subreddit_id'] = observation['data']['children'][i]['data']['subreddit_id']
            text['name'] = observation['data']['children'][i]['data']['name']
            # text['upvote_ratio'] = observation['data']['children'][i]['data']['upvote_ratio']
            # text['media'] = observation['data']['children'][i]['data']['media']
            # text['is_video'] = observation['data']['children'][i]['data']['is_video']
            # text['created_utc'] = observation['data']['children'][i]['data']['created_utc']
            
            if text['title'] not in posts:
                posts.append(text)
                
        params['after'] = posts[-1]['name']
    df = pd.DataFrame(posts)
        
    return df



df_nfl = scraper('nfl', 'new')


df_nba = scraper('nba', 'new')



df_nfl.to_csv('./data/nfl_aug_13_new_tab.csv'.format(datetime.now().strftime("%Y-%m-%d %H%M%S")), index = True)
df_nba.to_csv('./data/nba_aug_13_new_tab.csv'.format(datetime.now().strftime("%Y-%m-%d %H%M%S")), index = True)