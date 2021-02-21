// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;
typedef uint8_t BYTE;

void copy_header(FILE *input, FILE *output);
void copy_content_with_factor(FILE *input, FILE *output, float factor);

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    copy_header(input, output);
    copy_content_with_factor(input, output, factor);

    // Close files
    fclose(input);
    fclose(output);
}

void copy_header(FILE *input, FILE *output)
{
    // Read header from input file and copy it to output file
    BYTE header[HEADER_SIZE];

    fread(header, HEADER_SIZE, 1, input);
    fwrite(header, HEADER_SIZE, 1, output);
}

void copy_content_with_factor(FILE *input, FILE *output, float factor)
{
    int16_t buffer;

    // Read each audio sample and write updated value to the output
    while (fread(&buffer, sizeof(int16_t), 1, input))
    {
        // multiply sample by factor to change volume
        buffer *= factor;
        fwrite(&buffer, sizeof(int16_t), 1, output);
    }
}