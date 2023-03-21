from libs.hashing import ahash, dhash,phash, hamming_dist
from libs import vptree
import datetime
from os import walk, path
import argparse
import pickle
import cv2
import tqdm

class Indexer:
    def __init__(self, image_path, database_path, algo):
        self.image_path = image_path
        self.database_path = database_path
        self.algo = algo

    def getImagesPaths(self):
        exts = [".jpeg", ".jpg", ".jpe", ".png", ".bmp", ".tiff", ".tif"]
        imgPaths = [path.join(root,f) for (root, _, files) in walk(self.image_path) for f in files if path.splitext(f)[1] in exts]
        return imgPaths
    
    def generateHash(self):
        images = self.getImagesPaths()
        hashes = {}
        collisions = 0
        total = len(images)
        print("Generating hash for images, images will be listed below if collision occurs")
        if total:
            for index, image in enumerate(tqdm.tqdm(images)):
                # Generating hash for image
                h = self.algo(cv2.imread(image, cv2.IMREAD_GRAYSCALE))
                l = hashes.get(h, [])
                l.append(image)
                if len(l) > 1:
                    print("Collision occured for hash : ", h, " with images : ", l)
                    collisions += 1
                hashes[h] = l
            print("\nTotal collisions : ", collisions)
            return hashes, collisions
        else:
            raise ValueError("No images found in the given path!")
    
    def createTree(self):
        hashes, collisions = self.generateHash()
        if len(hashes) != len(self.getImagesPaths()) - collisions:
            raise ValueError("Some error has occured!")
        tree = vptree.VPTree(list(hashes.keys()), hamming_dist)
        # Combine the hashes and the tree
        algo_tree_hash = {"algo": self.algo, "tree": tree, "hashes": hashes}
        return algo_tree_hash
    
    def storeResults(self):
        try:
            algo_tree_hash = self.createTree()
            pickle.dump(algo_tree_hash, open(self.database_path, "wb"))
        except FileNotFoundError:
            print("Wrong file path!")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--images", required=True, help="Path to input dir of images")
    ap.add_argument(
        "-db",
        "--database",
        default=datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".pickle",
        help="Path to save indexed database",
    )
    ap.add_argument(
        "-a",
        "--algo",
        default="dhash",
        help="Algorithm for image hashing",
    )
    args = vars(ap.parse_args())

    if args["algo"] == "phash":
        algo = phash
    elif args["algo"] == "ahash":
        algo = ahash
    else:
        algo = dhash

    indexer = Indexer(args["images"], args["database"], algo)
    indexer.storeResults()