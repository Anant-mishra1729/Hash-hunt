import cv2
import numpy as np

def hamming_dist(h1, h2):
	return bin(int(h1, 16) ^ int(h2, 16)).count("1")


def dhash(img, size=8):
	resized = cv2.resize(img, (size + 1, size))
	conv = ((resized[:,1:] > resized[:,:-1]).astype("uint8")).flatten()
	binstr = ''.join(str(val) for val in conv)
	width = -(-len(binstr)//4) # Performing ciel operation ciel(a/b) is same as -(-a//b) 
	return '{:0>{width}x}'.format(int(binstr, 2), width=width)


if __name__ == "__main__":
	img1 = cv2.imread("abra.png",cv2.IMREAD_GRAYSCALE)
	# img2 = cv2.imread("test2.png",cv2.IMREAD_GRAYSCALE)
	print(dhash(img1,16))
