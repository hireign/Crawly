#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# In[2]:


global domainName
global rootURL
global alternativeURLs
domainRegex = re.compile(r"https?://?(www\.)?")


# ### To format any url to http://www. format and eliminate other alternatives

# In[3]:


def URLFormatter(url):
    formattedURL = domainRegex.sub('', url).strip().strip('/')
    formattedURL = re.sub("www.", "", formattedURL)
    formattedURL = 'http://www.' + formattedURL
    return formattedURL
# URLFormatter("//domain.com/home")


# ### Fetching homepage of the website

# In[23]:


# Ads http:// to the given URL because it is the only way to check for server response
# If the user will add to the URL directions then they will be deleted
# Example: 'https://moz.com/learn/seo/external-link' will turn to 'https://moz.com/'
# https://stackoverflow.com/questions/32314304/check-if-an-url-is-relative-to-another-ie-they-are-on-the-same-host

rootURL = "https://www.astrologer-astrology.com/"
domainName = URLFormatter(rootURL)
rootURL = domainName.split('/')[0] + "//" + domainName.split('/')[2]
source_code = requests.get(rootURL)
status_code = source_code.status_code
if(status_code != 200):
    source_code = requests.get(rootURL, headers={"User-Agent": "XY"})
soup = BeautifulSoup(source_code.text, "lxml")
rootTitle = soup.find("title").text
print("fetched "+rootURL+" status code: "+str(status_code))


# In[24]:


def alternativeURLCreator(url):
    noPrefix = domainRegex.sub('', url).strip().strip('/')
    noPrefix = re.sub("www.", "", noPrefix)
    alternativeURLs = []
    alternativeURLs.append(noPrefix)
    alternativeURLs.append("http://"+noPrefix)
    alternativeURLs.append("http://"+noPrefix+"/")
    alternativeURLs.append("http://"+noPrefix+"//")
    alternativeURLs.append("https://"+noPrefix)
    alternativeURLs.append("https://"+noPrefix+"/")
    alternativeURLs.append("https://"+noPrefix+"//")
    alternativeURLs.append("http://www."+noPrefix)
    alternativeURLs.append("http://www."+noPrefix+"/")
    alternativeURLs.append("http://www."+noPrefix+"//")
    alternativeURLs.append("https://www."+noPrefix)
    alternativeURLs.append("https://www."+noPrefix+"/")
    alternativeURLs.append("https://www."+noPrefix+"//")
    alternativeURLs.append("//"+noPrefix)
    alternativeURLs.append("//"+noPrefix+"/")
    alternativeURLs.append("//"+noPrefix+"//")
    alternativeURLs.append("//www."+noPrefix)
    alternativeURLs.append("//www."+noPrefix+"/")
    alternativeURLs.append("//www."+noPrefix+"//")
    return alternativeURLs


# In[25]:


alternativeDomains = alternativeURLCreator(rootURL)
print(alternativeDomains)


# In[26]:


def commonURLChecker(url):
    a = alternativeURLCreator(url)
    b = urlList
    common = list(set(a) & set(b))
    common = str(common).strip("[]").strip('\'')
    return common


# In[27]:


externalURLKeywords = ["http", "www", ".com", "https"]
exceptions = ["#", " ", "tel:", "callto:", "mailto:", "wp-content", "wp-login", ".pdf", "twitter.com", "facebook.com", "google.com", "pinterest.com", ".jpg", ".jpeg", ".webm", "javascript:void", "/out/", "?share="]


# In[28]:


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


# In[29]:


def urlCrawler(url, current_page, max_pages):
    global pageCount
    pageCount += 1
    tempTargetList = []
    outgoing_links = 0
    print("\n\n"+color.BLUE+color.BOLD+"now crawling page: "+color.END+url)
#     Fetching Data
    try:
        source_code = requests.get(url)
    except:
        status_code = source_code.status_code
        print(color.BLUE+color.BOLD+"status code: "+color.END+str(status_code))
    else:
        status_code = source_code.status_code
        print(color.BLUE+color.BOLD+"status code: "+color.END+""+str(status_code))
    if(source_code.status_code != 200):
        source_code = requests.get(rootURL, headers={"User-Agent": "XY"})
        status_code = source_code.status_code
        print(color.BLUE+color.BOLD+"new status code: "+color.END+str(status_code))
#     source_code = requests.get(url)
    if(status_code == 200):
#         not sure whether to keep the above if statement or not. The code works perfectly without it too
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        a = soup.findAll("a")
    #     Assiging Page Data to Dictionary
        if url not in pageDict:
            pageDict[""+url+""] = {}
        data = pageDict[""+url+""]
        try:
            data['title'] = soup.find("title").text
        except:
            print("error: title could not be found")
        data['status_code'] = status_code
        if(url == rootURL): 
            data['clickDepth'] = 0
            data["incoming_links"] = 0
        cur_clickDepth = data['clickDepth']
    #     Run a loop to find target urls
        for eachURL in a:
            href = eachURL.get("href")
            if(eachURL.get("title")):
                anchor = eachURL.get("title")
                anchor = anchor.replace("\n", "").strip()
            else:
                anchor = eachURL.text
                anchor = anchor.replace("\n", "").strip()
            if(href):
                if not any(x in href for x in exceptions):
#                 if any(x in href for x in alternativeURLs) and not any(x in href for x in exceptions):
#                 if not any(x in href for x in alternativeURLs) and not any(x in href for x in exceptions):
    #                 need to change above if statement. Works perfectly for with any x for puppywire.com and with not any x for hotelhalifax.ca but does not work in the alternative case for both
                    if (href == "/" or href in alternativeDomains):
                        tempURL = rootURL
                        tempURL = URLFormatter(tempURL)
                        print("\nfound "+href+" = "+tempURL+" for href in alternativeDomains")
                    elif any(href.startswith(x) for x in alternativeDomains):
                        tempURL = href
                        tempURL = URLFormatter(tempURL)
                        print("\nfound "+href+" = "+tempURL+" for href.startswith(x) for x in alternativeDomains")
                    elif(len(href)>1 and href[0] == "/" and not any(x in href for x in externalURLKeywords)):
                        tempURL = rootURL+""+href
                        tempURL = URLFormatter(tempURL)
                        print("\nfound "+href+" = "+tempURL+" for len(href)>1 and href[0] == / and not any(x in href for x in externalURLKeywords")
                    elif any(x in href for x in externalURLKeywords):
                        tempURL = ""
                        print(color.RED+color.BOLD+"\ndeclined external URL "+color.END+href)
                    else:
#                         added for URLs like "music.html"
                        tempURL = rootURL+"/"+href
                        tempURL = URLFormatter(tempURL)
                        print("\nfound "+href+" = "+tempURL+" for else")
                    if(tempURL!="" and tempURL not in tempTargetList and tempURL != url):
                        sourceList.append(url)
                        targetList.append(tempURL)
                        anchorList.append(anchor)
                        hrefList.append(href)
                        print(color.BOLD+"for source: "+color.END+url+color.BOLD+" , appending target: "+color.END+tempURL+color.BOLD+" , anchor: "+color.END+anchor)
                        outgoing_links += 1
                        tempTargetList.append(tempURL)
                        if (tempURL not in urlList):
                            if not any(x in alternativeURLCreator(tempURL) for x in urlList):  
#                       checking if triggered url is a new one and appending ot the urllist if affirmative
                                urlList.append(tempURL)
                                pageDict[""+tempURL+""] = {}                            
                                pageDict[""+tempURL+""]['clickDepth'] = cur_clickDepth+1
                                pageDict[""+tempURL+""]["incoming_links"] = 1
                                print(color.GREEN+color.BOLD+"appending new url: "+color.END+tempURL+color.BOLD+" click depth: "+color.END+str(pageDict[""+tempURL+""]['clickDepth']))
                            else:
                                duplicateURL = commonURLChecker(tempURL)
                                pageDict[""+duplicateURL+""]["incoming_links"] += 1
                                print("URL already in URLlist")
                        else:
                            pageDict[""+tempURL+""]["incoming_links"] += 1
                            print("URL already in URLlist")
                    elif(tempURL!=""):
                        print(color.RED+color.BOLD+"duplicate target link"+color.END)
                else:
                    print(color.RED+color.BOLD+"\ndeclined url (href in exceptions): "+color.END+""+href)
        if(pageCount < max_pages and pageCount < len(urlList)): 
            data['outgoing_links'] = outgoing_links
            urlCrawler(urlList[pageCount], pageCount, max_pages)
        else:
            data['outgoing_links'] = outgoing_links
    else:
#         skeptical about this else statement too. it is meant to add rows for URLs failed to fetch
        if url not in pageDict:
            pageDict[""+url+""] = {}
        data = pageDict[""+url+""]
        data['status_code'] = status_code
        print(color.RED+color.BOLD+"failed to crawl: "+color.END+url+color.BOLD+" status code: "+color.END+status_code)
        if(pageCount < max_pages and pageCount < len(urlList)): 
            data['outgoing_links'] = outgoing_links
            urlCrawler(urlList[pageCount], pageCount, max_pages)
        else:
            data['outgoing_links'] = outgoing_links


# In[31]:


pageDict = {}
pageCount = 0

sourceList = []
targetList = []
anchorList = []
hrefList = []

urlList = [rootURL]
outgoing_links = 0
import time
start_time = time.time()
urlCrawler(rootURL, 0, 400)
time = (time.time() - start_time)
print("--- %s seconds ---"%time)


# In[32]:


pageInfoDF = pd.DataFrame.from_dict({(i): pageDict[i] 
                           for i in pageDict.keys()},
                       orient='index')
pageInfoDF.head(4000)


# In[33]:


Links = {}
Links['source'] = sourceList
Links['target'] = targetList
Links['anchor'] = anchorList
Links['href'] = hrefList
linkInfoDF = pd.DataFrame(Links)
linkInfoDF.head(25000)


# In[34]:


urlName = rootURL
urlName = urlName.replace("http://","")
urlName = urlName.replace("https://","")
urlName = urlName.replace("www.","")
# urlName = urlName.replace("/","")
linkInfoDF.to_csv(r'C:\Users\hiren\crawly\links_news'+urlName+'.csv')
pageInfoDF.to_csv(r'C:\Users\hiren\crawly\pages_news'+urlName+'.csv')


# In[35]:


urlList


# In[36]:


len(urlList)


# In[17]:


a = ['a', 'b', 'c']
b = ['p', 'a', 'r']
c = "hapay"
# if any(x in c for x in a) and not any(x in c for x in b):
#     print("true")
# else:
#     print("false")
if any(x in a for x in b):
    print(a)
else:
    print(b)


# In[ ]:





# In[ ]:





# In[37]:


from flask import Flask
app = Flask(__name__)

@app.route('/home/index')
def hello_world():
    return 'Hello, World!'


# In[41]:


app.run()


# In[ ]:




