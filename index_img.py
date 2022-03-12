from libs.hashing import dhash, hamming_dist
from libs import vptree
from os import walk, path
import argparse
import pickle
import cv2

def getImagePaths(imgPath):
    imgPaths = []
    exts = [".jpeg", ".jpg", ".jpe", ".png", ".bmp", ".tiff", ".tif"]
    for (root, dirs, files) in walk(imgPath):
        for f in files:
            if path.splitext(f)[1] in exts:
                imgPaths.append(path.join(root, f))
    return imgPaths

def generate_hash(imgPaths):
    hashes = {}
    for (index, imgPath) in enumerate(imgPaths,1):
        print("Working on image {}/{}".format(index, len(imgPaths)))
        h = dhash(cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE))
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

if(len(imgPaths) != 0):
    # Generating dictionary of hash values
    hashes = generate_hash(imgPaths)
else:
    print("No images found at desired location!!!")

if(len(hashes) != 0):
    # Creating vp tree for hashes and paths of images
    tree = vptree.VPTree(list(hashes.keys()), hamming_dist)

    # Storing tree in pickle file
    with open(args["tree"], "wb") as file:
        pickle.dump(tree,file)

    # Storing hash values in pickle file
    with open(args["hashes"], "wb") as file:
        pickle.dump(hashes,file)
else:
    print("Error occured!, file not generated")
