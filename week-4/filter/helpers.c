#include "helpers.h"
#include "stdio.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            int avarage = (image[y][x].rgbtBlue + image[y][x].rgbtGreen + image[y][x].rgbtRed) / 3;
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
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width / 2; x++)
        {
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
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            int minimum_y = (y == 0) ? y : (y - 1);
            int maximum_y = (y == height - 1) ? y : (y + 1);
            int minimum_x = (x == 0) ? x : x - 1;
            int maximum_x = (x == width - 1) ? x : (x + 1);
            int r = 0, g = 0, b = 0, pixels = 0;

            for (int i = minimum_y; i <= maximum_y; i++)
            {
                for (int j = minimum_x; j <= maximum_x; j++)
                {
                    r += image[i][j].rgbtRed;
                    g += image[i][j].rgbtGreen;
                    b += image[i][j].rgbtBlue;
                    pixels++;
                }
            }

            image[y][x].rgbtRed = round(r / pixels);
            image[y][x].rgbtGreen = round(g / pixels);
            image[y][x].rgbtBlue = round(b / pixels);
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            int r = 0, g = 0, b = 0;

            for (int i = (y - 1); i <= = (y + 1); i++)
            {
                if (i == -1 || i == (height - 1))
                {
                    continue;
                }

                for (int j = (x - 1); j <= (x + 1); j++)
                {
                    if (j == -1 || j == (width - 1))
                    {
                        continue;
                    }
                }
            }
        }

        return;
    }
