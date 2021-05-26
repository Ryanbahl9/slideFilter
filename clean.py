from PIL import Image
import imagehash
import os

lastfilename = ""
maxlen = 0

for root, dirs, files in os.walk("."):
    for filename in files:
        maxlen = max(len(filename), maxlen)

print (maxlen)

for root, dirs, files in os.walk("."):
    for filename in files:
        if (filename.endswith(".png") and len(filename) < maxlen):
            newfilename = filename
            newfilename = newfilename.zfill(maxlen)
            os.rename(filename, newfilename)



for root, dirs, files in os.walk("."):
    files.sort()
    for filename in files:
        if (filename.endswith(".png")):
            if (lastfilename == ""):
                lastfilename = filename
            else:
                if (filename == "001801.png"):
                    print("here")
                hash0 = imagehash.phash(Image.open(lastfilename).crop((0,30,1215,870)))
                hash1 = imagehash.phash(Image.open(filename).crop((0,30,1215,870)))
                dif = abs(hash0 - hash1)
                if (dif < 3):
                    print("removing: " + filename)
                    os.remove(filename)
                else:
                    lastfilename = filename
        
