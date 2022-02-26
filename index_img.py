from libs.hashing import dhash, hamming_dist, convert_hash
from imutils import paths
import argparse
import pickle
import vptree
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--images",required = True, help = "Path to input dir of images")
ap.add_argument("-t","--tree", required=True,help = "Path to vptree file")
ap.add_argument("-a", "--hashes",required=True,help ="Path to generated image hash file")
args = vars(ap.parse_args())

imgPaths = list(paths.list_images(args["images"]))
hashes = {}

for (i,imgPath) in enumerate(imgPaths):
    print("[INFO] processing image {}/{}".format(i + 1,len(imgPaths)))
    img = cv2.imread(imgPath,cv2.IMREAD_GRAYSCALE)
    h = convert_hash(dhash(img))

    # Get a list of same hashes
    l = hashes.get(h,[])

    # Also append image path with it
    l.append(imgPath)
    hashes[h] = l

print("Writing hashes to disk")
f = open(args["hashes"],"wb")
f.write(pickle.dumps(hashes))
f.close()

print("Building VP tree...")
points = list(hashes.keys())
tree = vptree.VPTree(points,hamming_dist)

print("Writing vptree to disk...")
f = open(args["tree"],"wb")
f.write(pickle.dumps(tree))
f.close()

