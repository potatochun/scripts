import requests

#This script fetchs top stories from hacker news and display them

r = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
result = r.json()


# Display top 20 results 
for i in result[0:20]: 
    top = requests.get('https://hacker-news.firebaseio.com/v0/item/%s.json?print=pretty' % i).json()
    if top[u'type'] == 'story':
        #print(top[u'title'])
        print(top[u'title'] + "\t" + top[u'url'])
    else:
     	print("No story observed")

#print(top[u'type'])
