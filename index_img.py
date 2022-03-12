from libs.hashing import dhash, hamming_dist, convert_hash
from libs import vptree
from os import walk, path
import argparse
import pickle
import cv2
import time

def getImagePaths(imgPath):
    imgPaths = []
    exts = {".jpeg", ".jpg", ".jpe", ".png", ".bmp", ".tiff", ".tif"}
    for (root, dirs, files) in walk(imgPath):
        for f in files:
            if path.splitext(f)[1] in exts:
                imgPaths.append(path.join(root, f))
    return imgPaths


def generate_hash(imgPaths):
    hashes = {}
    for (index, imgPath) in enumerate(imgPaths,1):
        print("Working on image {}/{}".format(index, len(imgPaths)))
        img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
        h = convert_hash(dhash(img))
        l = hashes.get(h, [])
        l.append(imgPath)
        hashes[h] = l
    return hashes


# Parsing arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="Path to input dir of images")
ap.add_argument("-t", "--tree", default="Resources\\vptree.pickle" ,help="Path to vptree file")
ap.add_argument("-a", "--hashes",default="Resources\\hashes.pickle" ,help="Path to generated image hash file")
args = vars(ap.parse_args())

# Retriving image paths
imgPaths = getImagePaths(args["images"])

# Creating dictionary of hash values
start = time.time()
hashes = generate_hash(imgPaths)
end = time.time()
print("Time elapsed : {} seconds".format(end - start))

# Generating VP Tree of keys .i.e hashvalues
# It takes point (keys or hashvalues) and
# A function on basis of which it calculates distance between point
# In our case it is hamming distance
tree = vptree.VPTree(list(hashes.keys()), hamming_dist)

# Storing tree in pickle file
f = open(args["tree"], "wb")
f.write(pickle.dumps(tree))
f.close()

# Storing hash values in pickle file
f = open(args["hashes"], "wb")
f.write(pickle.dumps(hashes))
f.close()
