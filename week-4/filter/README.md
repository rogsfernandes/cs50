In this exercise the intent is to create filters to images and learn more about how images work on computers. Here we use Bitmap files, so the images need to have this format.

Compile:

`make filter`

Run:

`./filter <filter_type> <input_image.bmp> <output_image.bmp>`

__filter_type__:

`-g` for **grayscale** -> each pixel are transformed to the avarage value of RGB in it. Because all three have the same values, it assumes a gray scale.

`-r` for **reflect** -> each pixel in a image switches position horizontaly, so the first pixel in a row goes to the last pixel position and the last pixel goes to the first position, and so forth.