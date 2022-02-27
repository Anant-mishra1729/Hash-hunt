from libs.hashing import dhash
import argparse
import cv2
import pickle
import time

dist = 15

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Image to search")
ap.add_argument("-t", "--vptree", default = "vptree.pickle", help = "Path to generated VPtree")
ap.add_argument("-a", "--hashes", default = "hashes.pickle", help = "Path of generated hashes")
args = vars(ap.parse_args())

# Loading image and calculating its hash value
queryimg = cv2.imread(args["image"])
gray = cv2.cvtColor(queryimg,cv2.COLOR_BGR2GRAY)
queryhash = dhash(gray)

# Loading VPTree
f = open(args["vptree"],"rb")
tree = pickle.load(f)
f.close()

# Loading Hashes
f = open(args["hashes"],"rb")
hashes = pickle.load(f)
f.close()

# Fetching related hashes from vptree
start = time.time()
res = tree.get_all_in_range(queryhash, dist)
end = time.time()

print("{} results fetched in {} seconds".format(len(res),end-start))
print(res)

# Image output
cv2.imshow("Input",queryimg)
for (index,hashval) in res:
    for respath in hashes[hashval]:
        resimg = cv2.imread(respath)
        cv2.imshow("Output",cv2.resize(resimg,(240,240)))
        cv2.waitKey(0)
