import cv2


def hamming_dist(h1, h2):
    return bin(int(h1, 16) ^ int(h2, 16)).count("1")


def _dct(image):
    result = cv2.dct((image).astype("float32") / 255.0)
    return result * 255.0


def _hash(conv):
    binstr = "".join(str(val) for val in conv.astype("uint8").flatten())
    width = -(
        -len(binstr) // 4
    )  # Performing ceil operation, ceil(a/b) is equivalent to -(-a//b)
    return "{:0>{width}x}".format(int(binstr, 2), width=width)


def phash(image, size=8, freq_factor=4):
    resized = cv2.resize(image, (size * freq_factor, size * freq_factor))
    dct = _dct(resized)[:size, :size]
    mean = (dct.sum() - dct[0][0]) / (size**2 - 1)
    conv = dct > mean
    return _hash(conv)


def ahash(image, size=8):
    resized = cv2.resize(image, (size, size))
    conv = resized > resized.mean()
    return _hash(conv)


def dhash(image, size=8):
    resized = cv2.resize(image, (size + 1, size))
    conv = resized[:, 1:] > resized[:, :-1]
    return _hash(conv)


if __name__ == "__main__":
    import cv2

    image = cv2.imread("test.jpg", cv2.IMREAD_GRAYSCALE)
    print(ahash(image))
    print(dhash(image))
    print(phash(image))
