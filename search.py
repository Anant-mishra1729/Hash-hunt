from libs.hashing import dhash
import argparse
import cv2
import pickle
from time import time

def fetchResults(tree,hashes,qImage,prec):
    queryhash = dhash(cv2.cvtColor(qImage,cv2.COLOR_BGR2GRAY))

    # Fetching related hashes from vptree
    start = time()
    res = tree.get_all_in_range(queryhash, prec)
    end = time()
    print("{} results fetched in {} seconds".format(len(res),end-start))

    # Image output
    cv2.imshow("Input",qImage)
    for (index,hashval) in res:
        for respath in hashes[hashval]:
            resimg = cv2.imread(respath)
            cv2.imshow("Output",resimg)
            cv2.waitKey(0)


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Image to search")
ap.add_argument("-t", "--vptree", default = "Resources\\vptree.pickle", help = "Path to generated VPtree")
ap.add_argument("-a", "--hashes", default = "Resources\\hashes.pickle", help = "Path of generated hashes")
ap.add_argument("-p", "--dist", default = 10, type = int,help="Precision or hamming distance")
args = vars(ap.parse_args())

try:
    # Loading image and calculating its hash value
    qImage = cv2.imread(args["image"])
except cv2.error as error:
    print("[Error]: {}".format(error))

try:
    # Loading VPTree
    with open(args["vptree"],"rb") as file:
        tree = pickle.load(file)

    # Loading Hashes
    with open(args["hashes"],"rb") as file:
        hashes = pickle.load(file)
    
    fetchResults(tree,hashes,qImage,args["dist"])

except FileNotFoundError:
    print("Can't find required files, generate them using index_img.py")
