import cv2


def hamming_dist(h1, h2):
    return bin(int(h1, 16) ^ int(h2, 16)).count("1")


def dhash(img, size=8):
    resized = cv2.resize(img, (size + 1, size))
    conv = ((resized[:, 1:] > resized[:, :-1]).astype("uint8")).flatten()
    binstr = "".join(str(val) for val in conv)
    # Performing ciel operation, ciel(a/b) is equivalent to -(-a//b)
    width = -(-len(binstr) // 4)
    return "{:0>{width}x}".format(int(binstr, 2), width=width)

