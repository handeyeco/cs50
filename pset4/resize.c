#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main (int argc, char * argv[]) {
    // return if incorrect amount of inputs
    if (argc != 4) {
        fprintf(stderr, "Usage: ./resize resize_by input_file output_file");
        return 1;
    }

    int multiplier = atoi(argv[1]);
    char * input = argv[2];
    char * output = argv[3];

    // return if unable to read input
    FILE * input_file = fopen(input, "r");
    if (input_file == NULL) {
        fprintf(stderr, "Unable to open %s\n", input);
        return 2;
    }

    // return is unable to write output
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

    // Store input file dimensions
    int in_width = bi.biWidth;
    int in_height = abs(bi.biHeight);

    // Increase file dimensions by multiplier
    bi.biWidth *= multiplier;
    bi.biHeight *= multiplier;

    // determine padding for scanlines
    int in_padding = (4 - (in_width * sizeof(RGBTRIPLE)) % 4) % 4;
    int out_padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // Create offset for reiterating over scanlines
    int offset = in_width * sizeof(RGBTRIPLE) + in_padding;

    // Create more data for output header
    bi.biSizeImage = (bi.biWidth * sizeof(RGBTRIPLE) + out_padding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

     // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, output_file);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, output_file);

    // iterate over infile's scanlines
    for (int i = 0; i < in_height; i++) {
        // Write row n times
        for (int m = 0; m < multiplier; m ++) {
            // iterate over pixels in scanline
            for (int j = 0; j < in_width; j++) {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, input_file);

                // write RGB triple to outfile
                for (int k = 0; k < multiplier; k++) {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, output_file);
                }
            }

            // skip over padding, if any
            fseek(input_file, in_padding, SEEK_CUR);

            // then add it back (to demonstrate how)
            for (int k = 0; k < out_padding; k++) {
                fputc(0x00, output_file);
            }

            // Jump back in read file unless it's time to move to next line
            if (m < multiplier - 1) {
                fseek(input_file, -offset , SEEK_CUR);
            }
        }
    }

    // close infile
    fclose(input_file);

    // close outfile
    fclose(output_file);

    // success
    return 0;
}
