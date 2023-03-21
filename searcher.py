from libs.hashing import dhash, ahash, phash
import argparse
import cv2
import pickle
from time import time
import numpy as np

class Searcher:
	def __init__(self, database_path):
		self.database_path = database_path
		self.algo, self.tree, self.hashes = self.loadDatabase()

	def montage(self, images, distances, image_shape=(250, 250)):
		"""
		Create a montage from a list of 10 images
		:param images: List of images
		:param image_shape: Shape of each image
		:dist: List of distances
		:return: Montage of images
		"""
		# Resize the images to the given shape
		images = [cv2.resize(image, image_shape) for image in images]

		# If there are less than 10 images, add empty images
		if len(images) < 10:
			for i in range(10 - len(images)):
				images.append(np.zeros(shape=(image_shape[0], image_shape[1], 3), dtype="uint8"))
				distances.append("")
		
		# Add distance to each image
		for i, image in enumerate(images):
			cv2.putText(image, str(distances[i]), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

		# Create a montage using 10 images
		montage = cv2.vconcat([cv2.hconcat(images[0:5]), cv2.hconcat(images[5:10])])
		return montage

	def showResults(self, query_image ,results, limit=10):
		"""
		Show results
		:param query_image: Image to search
		:param res: List of similar images
		:return: None
		"""
		images = []
		distances = []
		for (dist, image) in results[:limit]:
			images.append(cv2.imread(image))
			distances.append(dist)
		
		montage = self.montage(images, distances)
		while True:
			cv2.imshow("Query", query_image)
			cv2.imshow("Top 10 Results (Press q to exit)", montage)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		cv2.destroyAllWindows()

	def search(self, query_image, precision, show_results=False):
		"""
		Search for similar images in the database
		:param query_image: Image to search
		:param precision: Precision or hamming distance
		:param show_results: Show results or not
		:return: List of similar images
		"""
		queryhash = self.algo(cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY))

		# Fetching related hashes from vptree
		start = time()
		res = self.tree.get_all_in_range(queryhash, precision)
		end = time()
		print(f"{len(res)} results fetched in {end - start} seconds")
		results = []
		for (dist, hash) in res:
			images = self.hashes.get(hash, [])
			for image in images:
				results.append((dist, image))

		# Sort the results
		results = sorted(results)
		print(results)

		if show_results:
			self.showResults(query_image, results)
		return results

	def loadDatabase(self):
		try:
			db = pickle.load(open(self.database_path, "rb"))
		except FileNotFoundError:
			print("Files not found!\
				  \n Make sure you have generated the tree and hashes file using index_images.py")
		return db["algo"], db["tree"], db["hashes"]

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True, help="Image to search")
	ap.add_argument(
		"-db",
		"--database",
		default="Resources/Indexed/database.pickle",
		help="Path to indexed database",
	)
	ap.add_argument(
		"-p", "--dist", default=10, type=int, help="Precision or hamming distance"
	)
	args = vars(ap.parse_args())


	searcher = Searcher(args["database"])
	query_image = cv2.imread(args["image"])
	searcher.search(query_image, args["dist"], show_results=True)
