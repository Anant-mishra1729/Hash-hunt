# Hash-hunt

Reverse image searching engine based on Perpetual image hashing technique.

Image hashing algorithms are based on 
<a href="https://www.hackerfactor.com/blog/?/archives/529-Kind-of-Like-That.html">Kind of like that</a> and 
<a href="https://hackerfactor.com/blog/index.php%3F/archives/432-Looks-Like-It.html">Looks Like It</a> by Dr. Neal Krawetzy.

# Description

## What is Image hashing ?
Image hashing is the process of using an algorithm (here dhash) to assign a unique hash value to an image.

### Test Image

<img src = "Resources/lake.jpg">

### Generated hash using dhash algorithm: 784806da92483094

## Ahash algorithm 
* Simplest of all image hashing algorithms
* More false positives compared to phash and ahash

**Working**
* Convert image to **grayscale** and resize to **8x8** pixels.
* Compute mean of image array.
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

## How Image hashing works with fast search on Images ?

* Hash value of input images is calculated using dhash algorithm.
* This hash value and it's corresponding image is stored in database.
* **VPTree** or **KD-Tree** can be used to store hashvalues of images on the based of hamming distance between them.
* On searching particular image it's hash value is calculated which is then passed to VPTree, it finds related images based on the hamming distance between calculated hash and stored hash values.

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

--images or -i : Path to source directory of images to index

--tree or -t : Path to vptree file

--hashes or -b : Path to generated image hash file

--algo or -a : Algorithm to use phash, dhash or ahash

```

* For searching an image execute
```
python search.py 

--image or -i : Image to search

--tree or -t : Path to generated VPtree

--hashes or -a : Path of generated hash file

--algo or -a : Algorithm to use phash, dhash or ahash
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
