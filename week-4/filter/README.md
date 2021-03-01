In this exercise the intent is to create filters to images and learn more about how images work on computers. Here we use Bitmap files, so the images need to have this format.

Compile:

`make filter`

Run:

`./filter <filter_type> <input_image.bmp> <output_image.bmp>`

__filter_type__:

`-g` for **grayscale effect** -> each pixel are transformed to the avarage value of RGB in it. Because all three have the same values, it assumes a gray scale.

`-r` for **reflection effect** -> each pixel in a image switches position horizontaly, so the first pixel in a row goes to the last pixel position and the last pixel goes to the first position, and so forth.

`-b` for **blur effect** -> each pixel changes its RGB values based on the nearest pixels, causing a softening effect on each one.

`-e` for **edge effect** -> the edges are highlighted in this cool effect, based on the Sobel operator which uses the 3x3 matrix of adjacent pixels to determine wether this is an edge or not