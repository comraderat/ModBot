from Login import Login
from NewPostGetting import *
import json
import time
from Functions import *

IgnoreWithAge = 60*60*24
LastCheck = time.time() - IgnoreWithAge
RunInterval_seconds = 10*60

#startup

imagesok = BannedImageFolderCheck()
configok = ConfigCheck()

if not imagesok or not configok:
    print("Please add images and/or valid moderation credentials")
    exit()

with open("config.json") as f:
    config = json.load(f)
username = config["username"]
password = config["password"]


Bannedimages = HashFolderOfImages("bannedimages")

log = open("Log_{}.log.txt".format(CurrentTimeReadable()), mode="w")
log.writelines("Started modbot at {}\n".format(CurrentTimeReadable()))
log.flush()

#periodical

while(True):
    print("Starting cycle at {}".format(CurrentTimeReadable()))
    log.writelines("Starting cycle at {}\n".format(CurrentTimeReadable()))
    log.flush()
    CheckLimit = LastCheck
    LastCheck = time.time() - 100
    session = requests.session()
    Login(session, username, password)
    imageposts = GetNewImagePostsUntil(session, CheckLimit)
    hashed = downloadandhashimagepost(imageposts)

    for post in hashed:
        for imagehash in post["imagehashes"]:
            if imagehash in Bannedimages:
                session.get(post["deletelink"])
                print("Deleted post #{}".format(post["postID"]))
                log.writelines("Deleted post #{}\n".format(post["postID"]))
                log.flush()

    time.sleep(RunInterval_seconds)