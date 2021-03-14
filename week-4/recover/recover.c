#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>

typedef uint8_t BYTE;

// Number of bytes that represents the file separated data blocks
const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover <file.raw>\n");
        return 1;
    }

    // declare jpeg header as a four bytes pattern that we need to look for
    BYTE buffer[BLOCK_SIZE];
    FILE *card = fopen(argv[1], "r");
    FILE *image;
    string imagename = malloc(7);
    bool started = false;
    int count = 0;

    if (card)
    {
        while (fread(buffer, BLOCK_SIZE, 1, card))
        {
            // checking if the first four bytes represents the beggining of a new jpg file...
            if (buffer[0] == 0xff &&
                buffer[1] == 0xd8 &&
                buffer[2] == 0xff &&
                (buffer[3] & 0xf0) == 0xe0)
            {
                // create a new file name with zeros and the image number. Example: 012.jpg
                sprintf(imagename, "%03i.jpg", count);
                count++;
                if (started)
                {
                    // close previous file
                    fclose(image);
                }
                else
                {
                    // flag started as true because the first jpg was found
                    started = true;
                }

                // create a new file
                image = fopen(imagename, "w");
                // start writing data to the new file
                fwrite(buffer, BLOCK_SIZE, 1, image);
            }
            else if (started)
            {
                // write another 512 bytes block to the file
                fwrite(buffer, BLOCK_SIZE, 1, image);
            }
        }

        // free the memory used to read/write files
        fclose(card);
        fclose(image);
        free(imagename);

        return 0;
    }
    else
    {
        printf("File doesn't exist\n");
        return 1;
    }
}