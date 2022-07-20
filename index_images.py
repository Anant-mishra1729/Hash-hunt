from libs.hashing import ahash, dhash,phash, hamming_dist
from libs import vptree
from libs.progress import progress
from os import walk, path
import argparse
import pickle
import cv2


def getImagePaths(imgPath):
    imgPaths = []
    exts = [".jpeg", ".jpg", ".jpe", ".png", ".bmp", ".tiff", ".tif"]
    for (root, _, files) in walk(imgPath):
        for f in files:
            if path.splitext(f)[1] in exts:
                imgPaths.append(path.join(root, f))
    return imgPaths


def generate_hash(imgPaths, algo = dhash):
    hashes = {}
    collision = 0
    total = len(imgPaths)
    print("Generating hash for images, images will be listed below if collision occurs")

    for (index, imgPath) in enumerate(imgPaths, 1):
        h = algo(cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE))
        l = hashes.get(h, [])
        l.append(imgPath)
        if len(l) > 1:
            print(l)
            collision += 1
        hashes[h] = l
        progress(index, total)
    print("\nTotal collisions : ", collision)
    return hashes, collision


# Parsing arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="Path to input dir of images")
ap.add_argument(
    "-t",
    "--tree",
    default="Resources/Indexed/vptree.pickle",
    help="Path to vptree file",
)
ap.add_argument(
    "-b",
    "--hashes",
    default="Resources/Indexed/hashes.pickle",
    help="Path to generated image hash file",
)
ap.add_argument(
    "-a",
    "--algo",
    default="dhash",
    help="Algorithm for image hashing",
)
args = vars(ap.parse_args())

# Retriving image paths
imgPaths = getImagePaths(args["images"])

if not len(imgPaths):
    raise FileNotFoundError("No images found at desired location!")

# Generating dictionary of hash values
if args["algo"] == "phash":
    algo = phash
elif args["algo"] == "ahash":
    algo = ahash
else:
    algo = dhash
hashes, collision = generate_hash(imgPaths,algo)


if len(hashes) != len(imgPaths) - collision:
    raise ValueError("Some error has occured!")

# Creating vp tree for hashes and paths of images
tree = vptree.VPTree(list(hashes.keys()), hamming_dist)

try:
    # Storing tree in pickle file
    with open(args["tree"], "wb") as file:
        pickle.dump(tree, file)

    # Storing hash values in pickle file
    with open(args["hashes"], "wb") as file:
        pickle.dump(hashes, file)

except FileNotFoundError:
    print("Wrong file path!")
