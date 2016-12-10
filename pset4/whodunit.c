#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main (int argc, char * argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: ./whodunit input_file output_file\n");
        return 1;
    }

    char * input = argv[1];
    char * output = argv[2];

    FILE * input_file = fopen(input, "r");
    if (input_file == NULL) {
        fprintf(stderr, "Unable to open %s\n", input);
        return 2;
    }

    FILE * output_file = fopen(output, "w");
    if (input_file == NULL) {
        fclose(input_file);
        fprintf(stderr, "Unable to write to %s\n", output);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, input_file);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, input_file);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(output_file);
        fclose(input_file);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, output_file);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, output_file);

    // determine padding for scanlines
    int padding =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from input
            fread(&triple, sizeof(RGBTRIPLE), 1, input_file);

            if (triple.rgbtBlue == 0xFF && triple.rgbtGreen == 0xFF && triple.rgbtRed == 0xFF) {
                triple.rgbtBlue  = 0x00;
                triple.rgbtGreen = 0x00;
                triple.rgbtRed   = 0xFF;
            }

            // write RGB triple to output
            fwrite(&triple, sizeof(RGBTRIPLE), 1, output_file);
        }

        // skip over padding, if any
        fseek(input_file, padding, SEEK_CUR);

        // then add it back (to demonstrate how)
        for (int k = 0; k < padding; k++)
        {
            fputc(0x00, output_file);
        }
    }

    // close infile
    fclose(input_file);

    // close outfile
    fclose(output_file);

    // success
    return 0;
}
