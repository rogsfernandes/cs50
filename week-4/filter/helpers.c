#include "helpers.h"
#include "stdio.h"
#include "math.h"
#include "stdbool.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            int avarage = round((image[y][x].rgbtBlue + image[y][x].rgbtGreen + image[y][x].rgbtRed) / 3.0);
            image[y][x].rgbtBlue = avarage;
            image[y][x].rgbtGreen = avarage;
            image[y][x].rgbtRed = avarage;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // for each vertical point
    for (int y = 0; y < height; y++)
    {
        // and each horizontal point
        for (int x = 0; x < width / 2; x++)
        {
            // swap the positions of the points horizontally
            int right = width - 1 - x;
            RGBTRIPLE aux = image[y][x];
            image[y][x] = image[y][right];
            image[y][right] = aux;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE blurred[height][width];

    // for each vertical point
    for (int y = 0; y < height; y++)
    {
        // and each horizontal point
        for (int x = 0; x < width; x++)
        {
            int minimum_y = (y == 0) ? y : (y - 1);
            int maximum_y = (y == height - 1) ? y : (y + 1);
            int minimum_x = (x == 0) ? x : (x - 1);
            int maximum_x = (x == width - 1) ? x : (x + 1);
            float r = 0.0, g = 0.0, b = 0.0;
            int pixels = 0;

            // for the points surrounding this pixel
            for (int i = minimum_y; i <= maximum_y; i++)
            {
                for (int j = minimum_x; j <= maximum_x; j++)
                {
                    // sum their values
                    r += image[i][j].rgbtRed;
                    g += image[i][j].rgbtGreen;
                    b += image[i][j].rgbtBlue;
                    pixels++;
                }
            }

            // and make the new value be the avarage of the surrounding pixels sum
            blurred[y][x].rgbtRed = round(r / pixels);
            blurred[y][x].rgbtGreen = round(g / pixels);
            blurred[y][x].rgbtBlue = round(b / pixels);
        }
    }

    // copying the blurred image to the original one
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            image[y][x] = blurred[y][x];
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE highlihted[height][width];

    // for each point in y axis
    for (int y = 0; y < height; y++)
    {
        // and for each point in x axis
        for (int x = 0; x < width; x++)
        {
            float red_x = 0.0, green_x = 0.0, blue_x = 0.0;
            float red_y = 0.0, green_y = 0.0, blue_y = 0.0;
            float gx_kernel[3][3] = {{-1.0, 0.0, 1.0},
                                     {-2.0, 0.0, 2.0},
                                     {-1.0, 0.0, 1.0}};
            float gy_kernel[3][3] = {{-1.0, -2.0, -1.0},
                                     {0.0, 0.0, 0.0},
                                     {1.0, 2.0, 1.0}};

            // for each point surrounding this point in vertical
            for (int i = 0; i < 3; i++)
            {
                int pixel_y = y + (i - 1);
                // and each point surrounding this point in horizontal
                for (int j = 0; j < 3; j++)
                {
                    int pixel_x = x + (j - 1);
                    bool is_outside_border =
                        pixel_x == -1 || pixel_x == width ||
                        pixel_y == -1 || pixel_y == height;

                    float red_value = is_outside_border ? 0.0 : image[pixel_y][pixel_x].rgbtRed;
                    float green_value = is_outside_border ? 0.0 : image[pixel_y][pixel_x].rgbtGreen;
                    float blue_value = is_outside_border ? 0.0 : image[pixel_y][pixel_x].rgbtBlue;

                    // computing changes in x axis
                    red_x += (red_value * gx_kernel[i][j]);
                    green_x += (green_value * gx_kernel[i][j]);
                    blue_x += (blue_value * gx_kernel[i][j]);

                    // computing changes in y axis
                    red_y += (red_value * gy_kernel[i][j]);
                    green_y += (green_value * gy_kernel[i][j]);
                    blue_y += (blue_value * gy_kernel[i][j]);
                }
            }

            int r = round(sqrt(pow(red_x, 2.0) + pow(red_y, 2.0)));
            int g = round(sqrt(pow(green_x, 2.0) + pow(green_y, 2.0)));
            int b = round(sqrt(pow(blue_x, 2.0) + pow(blue_y, 2.0)));

            highlihted[y][x].rgbtRed = r > 255 ? 255 : r;
            highlihted[y][x].rgbtGreen = g > 255 ? 255 : g;
            highlihted[y][x].rgbtBlue = b > 255 ? 255 : b;
        }
    }

    // for each vertical point
    for (int y = 0; y < height; y++)
    {
        // and each horizontal point
        for (int x = 0; x < width; x++)
        {
            // copy the value of the pixels with effect applied
            image[y][x] = highlihted[y][x];
        }
    }

    return;
}
