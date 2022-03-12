from libs.hashing import dhash
import argparse
import cv2
import pickle
import time

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Image to search")
ap.add_argument("-t", "--vptree", default = "Resources\\vptree.pickle", help = "Path to generated VPtree")
ap.add_argument("-a", "--hashes", default = "Resources\\hashes.pickle", help = "Path of generated hashes")
ap.add_argument("-p", "--dist", default = 10, type = int,help="Precision or hamming distance")
args = vars(ap.parse_args())

# Loading image and calculating its hash value
queryimg = cv2.imread(args["image"])
gray = cv2.cvtColor(queryimg,cv2.COLOR_BGR2GRAY)
queryhash = dhash(gray)

# Loading VPTree
with open(args["vptree"],"rb") as file:
    tree = pickle.load(file)

# Loading Hashes
with open(args["hashes"],"rb") as file:
    hashes = pickle.load(file)

# Fetching related hashes from vptree
start = time.time()
res = tree.get_all_in_range(queryhash, args["dist"])
end = time.time()

print("{} results fetched in {} seconds".format(len(res),end-start))

# Image output
cv2.imshow("Input",queryimg)
for (index,hashval) in res:
    for respath in hashes[hashval]:
        resimg = cv2.imread(respath)
        cv2.imshow("Output",resimg)
        cv2.waitKey(0)
