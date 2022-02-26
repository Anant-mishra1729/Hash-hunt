import numpy as np
import cv2

def hamming_dist(h1, h2):
	return bin(int(h1) ^ int(h2)).count("1")

def convert_hash(hash):
	# Converting hash to numpy float 64 bit and then to int
	return int(np.array(hash,np.float64))

def dhash(img,size = 8):

	resized = cv2.resize(img,(size + 1,size));

	# Creating horizontal gradient
	diff = enumerate([resized[i,j-1] < resized[i,j] for i in range(0,size) for j in range(1,size+1)])

	# Generating hash by summing up power(2,i) for which pixel is true
	s = 0
	for (i,v) in diff:
		if v:
			s += 2**i
	return s;
