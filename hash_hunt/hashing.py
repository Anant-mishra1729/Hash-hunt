import numpy as np
import cv2
import pickle 

def hamming_dist(h1, h2):
	return bin(int(h1) ^ int(h2)).count("1")

def convert_hash(hash):
	# Converting hash to numpy float 64 bit and then to int
	return int(np.array(h,dtype = "float-64"))

def dhash(img, hashsize = 8):
	# Convert image to grayscale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Resizing image to (hashsize +1, hashsize) .i.e 9x8 
	resized = cv2.resize(gray,(hashsize + 1, hashsize));

	# Computing horizontal gradient .i.e (col[0,0] > col[0,1] etc.) between adjacent column pixels
	diff = resized[:,1:] > resized[:,:-1]
	
	'''
	diff.flatten() # Converts diff to 1d list
	enumerate(diff.flatten())  # Assigns index with converted 1d list
	diff1 = list(enumerate(diff.flatten())) # Converting from enumerate type to list

	Calculating hash by summing up power(2,i) for which pixel is true
	s = 0
	for (i,v) in diff1:
		if v:
			s += 2**i
	print(s)
	'''	
	diff = enumerate(diff.flatten())
	return sum([2 ** i for (i, value) in diff if value])