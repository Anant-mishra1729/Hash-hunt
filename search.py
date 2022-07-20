from libs.hashing import dhash, phash, ahash
import argparse
import cv2
import pickle
from time import time


def fetchResults(tree, hashes, qImage, prec, algo = dhash):
    queryhash = algo(cv2.cvtColor(qImage, cv2.COLOR_BGR2GRAY))

    # Fetching related hashes from vptree
    start = time()
    res = tree.get_all_in_range(queryhash, prec)
    end = time()
    print(f"{len(res)} results fetched in {end - start} seconds")

    # Image output
    if len(res):
        cv2.imshow("Input", qImage)
        for (dist, hashval) in sorted(res[:prec]):  # Limiting output to prec images
            print("Hamming distance : ", dist)
            for respath in hashes[hashval]:
                resimg = cv2.imread(respath)
                cv2.imshow("Output", resimg)
                if cv2.waitKey(0) & 0xFF == ord("q"):
                    break


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Image to search")
ap.add_argument(
    "-t",
    "--tree",
    default="Resources/Indexed/vptree.pickle",
    help="Path to generated VPtree",
)
ap.add_argument(
    "-b",
    "--hashes",
    default="Resources/Indexed/hashes.pickle",
    help="Path of generated hash file",
)
ap.add_argument(
    "-p", "--dist", default=10, type=int, help="Precision or hamming distance"
)
ap.add_argument(
    "-a",
    "--algo",
    default="dhash",
    help="Algorithm for image hashing",
)
args = vars(ap.parse_args())

try:
    # Loading image and calculating its hash value
    qImage = cv2.imread(args["image"])
except cv2.error as error:
    print("[Error]: {}".format(error))

try:
    # Loading VPTree
    with open(args["tree"], "rb") as file:
        tree = pickle.load(file)

    # Loading Hashes
    with open(args["hashes"], "rb") as file:
        hashes = pickle.load(file)
    if args["algo"] == "phash":
        algo = phash
    elif args["algo"] == "ahash":
        algo = ahash
    else:
        algo = dhash

    fetchResults(tree, hashes, qImage, args["dist"],algo)

except FileNotFoundError:
    print("Can't find required files, generate them using index_img.py")
