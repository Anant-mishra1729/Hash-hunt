import cv2

def hamming_dist(h1, h2):
	return bin(int(h1,16) ^ int(h2,16)).count("1")

def dhash(img,size = 8):
	resized = cv2.resize(img,(size + 1,size));
	diff = enumerate([resized[i,j-1] < resized[i,j] for i in range(0,size) for j in range(1,size+1)])
	s = 0
	for (i,v) in diff:
		if v:
			s += 2**i
	return hex(s)
