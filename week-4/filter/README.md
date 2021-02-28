In this exercise the intent is to create filters to images and learn more about how images work on computers. Here we use Bitmap files, so the images need to have this format.

Compile:

`make filter`

Run:

`./filter <filter_type> <input_image.bmp> <output_image.bmp>`

__filter_type__:

`-g` for *grayscale* -> in here each pixel are converted to the avarage of RGB in it. Because all three have the same values, it assumes a gray scale.