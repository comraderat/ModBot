from PIL import Image
from io import BytesIO
import requests
import imagehash
import os
import time, datetime

def LoadImageFromURL(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def LoadImageFromDisk(fp):
    return Image.open(fp)

def downloadfiles(post):
    sources = post["imagesources"]
    for i in range(len(sources)):
        image = LoadImageFromURL(sources[i])
        image.save(os.path.join("removedimages","{}_{}.jpeg".format(str(post["postID"]), str(i))), "JPEG")


def downloadandhashimagepost(postlist):
    for post in postlist:
        yield {"board": post["board"],
               "postID": post["postID"],
               "deletelink": post["deletelink"],
               "imagesources": post["imagesources"],
               "imagehashes": [imagehash.dhash(LoadImageFromURL(x)) for x in post["imagesources"]]
               }

def BannedImageFolderCheck():
    folderpath = os.path.join(os.path.dirname(__file__), "bannedimages")
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
        return False
    return True


examplejsonusername = """{
	"username": "admin",
	"password": "admin"
}"""


def ConfigCheck():
    configpath = "config.json"
    if not os.path.exists(configpath):
        with open(configpath, "w") as f:
            f.write(examplejsonusername)
        return False
    return True


def HashFolderOfImages(folder):
    files = os.listdir(os.path.join(os.path.dirname(__file__), folder))
    fileswithpath = [os.path.join(os.path.dirname(__file__), folder, x) for x in files]
    return [imagehash.dhash(LoadImageFromDisk(x)) for x in fileswithpath]

def CurrentTimeReadable():
    value = datetime.datetime.fromtimestamp(time.time())
    return value.strftime('%Y-%m-%d_%H-%M-%S')