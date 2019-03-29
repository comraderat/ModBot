from bs4 import BeautifulSoup
from itertools import chain
import re



def HandleImagePost(postsoup):
    images = postsoup.find_all('img', attrs = {"class":"post-image"})
    if len(images) <= 0:
        return None
    board = postsoup["data-board"]
    postid = postsoup.contents[3]["id"].split("_")[1]
    imagesources = [x.parent["href"] for x in images]
    deletea = postsoup.find_all('a', href = True, text = '[D]')[0]
    deletelink = "https://sys.8ch.net/mod.php?" + re.findall("document.location='\?.*?';", deletea["onclick"])[0]\
        .replace("document.location='?", "")\
        .replace("';", "")
    return{
        "board": board,
        "postID": postid,
        "deletelink": deletelink,
        "imagesources": imagesources
    }


def generatewithnone(func, list):
    for x in list:
        result = func(x)
        if result is not None:
            yield result


def DisectNewPostPage(page):
    soup = BeautifulSoup(page, features="html.parser")
    posts = soup.find_all(attrs={"class":"post-wrapper"})
    generator = generatewithnone(HandleImagePost, posts)
    nextlink = soup.findAll('a', href = True, text = 'Next 25 posts')[0]['href']
    return nextlink, generator



starturl = "https://sys.8ch.net/mod.php?/recent/25"
def GetNewImagePostsUntil(session, time, url = starturl):
    r = session.get(url)
    (nextlink, generator) = DisectNewPostPage(r.text)
    if int(nextlink.split("=")[1]) >= time:
        return chain(generator, GetNewImagePostsUntil(session, time, "https://sys.8ch.net" + nextlink))
    else:
        return generator