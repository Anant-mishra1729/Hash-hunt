# Hash-hunt

Reverse image searching engine based on Perpetual image hashing technique.

Image hashing algorithms are based on 
<a href="https://www.hackerfactor.com/blog/?/archives/529-Kind-of-Like-That.html">Kind of like that</a> and 
<a href="https://hackerfactor.com/blog/index.php%3F/archives/432-Looks-Like-It.html">Looks Like It</a> by Dr. Neal Krawetzy.

# Description

## What is Image hashing?
Image hashing is the process of using a hashing algorithm to assign a unique hash value to an image.

### Test Image

<img src = "Resources/lake.jpg">

### Generated hash using dhash algorithm: 784806da92483094

## Ahash algorithm 
* Simplest of all image hashing algorithms
* More false positives compared to phash and ahash

**Working**
* Convert image to **grayscale** and resize to **8x8** pixels.
* Compute the mean of the image array.
* If P[x] > mean : P[x] = 1 else P[x] = 0
* Compute hash

## Phash algorithm
* Very few false positives
* High computational time

<br />
<img src = "Resources/Phash.svg">

<br />

## Dhash algorithm
* Few false positives, more than phash
* Less computational time

<br />
<img src = "Resources/Dhash.svg">

<br />

## How does Image hashing work with the fast search on Images?

* The Hash value of input images is calculated using (Phash, Dhash, Ahash) algorithm.
* This hash value and its corresponding image are stored in a database.
* **VPTree** or **KD-Tree** can be used to store hash values of images on the based hamming distance between them.
* On searching a particular image its hash value is calculated which is then passed to KD-Tree/VP-Tree, it finds related images based on the hamming distance between calculated hash and stored hash values.

## Getting Started

### Dependencies 

* OpenCV
* Python 3

### Executing program

* Clone this repository

```
git clone https://github.com/Anant-mishra1729/Hash-hunt.git
```
* For indexing images execute
```
python index_images.py 

--images or -i: Path to the source directory of images to index

--dataset or -d: Path to generated index file

--algo or -a: Algorithm to use phash, dhash or ahash
```

* For searching an image execute
```
python search.py 

--image or -i: Image to search

--dataset or -d: Path to generated index file
```

## Results
Images are taken from <a href = "https://www.kaggle.com/datasets/erennik/places">dataset</a>

<img src = "Resources/result.jpg">

## Contributors

<a href="https://github.com/Anant-mishra1729">Anant Mishra</a>

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments
<a href="https://www.hackerfactor.com/blog/?/archives/529-Kind-of-Like-That.html">Kind of like that</a> and 
<a href="https://hackerfactor.com/blog/index.php%3F/archives/432-Looks-Like-It.html">Looks Like It</a> by Dr. Neal Krawetzy.
