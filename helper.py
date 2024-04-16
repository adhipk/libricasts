import requests
import os
import logging
import json
import re
from time import sleep
from dotenv import load_dotenv
from redisHelper import RedisHelper
load_dotenv()
GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN","")

r = RedisHelper()
log = logging.getLogger('root.helper')
def writeGist(content,filename):
    filename = f"{filename}.rss"
    url=GITHUB_API+"/gists"
    # print("Request URL: %s"%url)

    #print headers,parameters,payload
    headers={"Authorization":"token %s"%GITHUB_TOKEN}
    params={"scope":"gist"}
    payload = {
        "description":"GIST created by python code",
        "public":True,
        "files":{
            filename:{
                "content":content
                }
            }
        }

    #make a requests
    res=requests.post(url,headers=headers,params=params,data=json.dumps(payload))
    
    response = res.json()
    # print("resp",response,type(res.status_code)) 
    if res.status_code >= 200 and res.status_code < 300:
        
        return response["files"][filename]["raw_url"]
    else:
        return None

def uploadToPocketcasts(rss_url):
    # print("url",rss_url)
    endpoint = "https://refresh.pocketcasts.com/author/add_feed_url"
    headers={
        "origin": "https://pocketcasts.com",
        "referer": "https://pocketcasts.com/"
    }
    payload = {
        "public_option":"yes",
        "url":rss_url
    }
    response = requests.post(endpoint,headers=headers,json=payload)
    if response.status_code==200:
        result = response.json()
        
        if(result["status"] == "poll"):
            # wait 2 secs then call api again;
            timeout = 0.5
            while result["status"] == "poll":
                sleep(timeout)
                timeout *= 2
                response = requests.post(endpoint,headers=headers,json=payload)
                result = response.json()
        if(result["status"] == "ok"):
            return {"status":"ok", "url":result["result"]["share_link"]}
    # error state return error info
    return result

def fixRSSfile(rss_url):
    rss_response = requests.get(rss_url)
    rss_response_content = rss_response.text
    
    # add valid pubdate
    rss_response_content = re.sub(
        pattern=r"<!--<pubDate>file element=rss.pubDate</pubDate>-->",
        string=rss_response_content,
        repl="<pubDate>2020-01-05T19:11:09Z</pubDate>"
    )
    return rss_response_content
def getBooks(search_title):
    r = "https://librivox.org/api/feed/audiobooks/"
    
    req =requests.get(
        r,
        params={
            "title":f"^{search_title}",
            "format":"json",
            "limit":10
        }
    )
    
    result = req.json()
    if 'books' in result:
        return result["books"]
    return []


def uploadRss(librivox_rss_url,book_title,book_id):
    key = f"book_{book_id}"
    # check if original file works
    pocketCasts = uploadToPocketcasts(librivox_rss_url)
    if(pocketCasts["status"] !='ok'):
        
        # check if it is already in redis
        cached_rss_url = r.get(key)
        if cached_rss_url:
            log.info(f"use the cached url {cached_rss_url}")
            rss_url = cached_rss_url
        else:
            fixed_rss = fixRSSfile(librivox_rss_url)
            log.info(f"generate a new url {fixed_rss}")
            rss_url = writeGist(fixed_rss,f"librivox_{book_id}")
            # store the gist url in redis
            r.set(key,rss_url)
        
        
        if(rss_url):
            pocketCasts = uploadToPocketcasts(rss_url)
        else:
            # delete the gist url in redis
            r.delete(key)
            return {"status":"error","message":"Failed to upload to gist"}

    return pocketCasts
