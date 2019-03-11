// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>
#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: copy n infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // remember factor
    int n = atoi(argv[1]);

    // validate factor
    if (n <= 0 || n > 100)
    {
        fprintf(stderr, "Factor %d is out of range valid value 1 .. 100.\n", n);
        return 1;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 1;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 1;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bfOrig;
    fread(&bfOrig, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER biOrig;
    fread(&biOrig, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bfOrig.bfType != 0x4d42 || bfOrig.bfOffBits != 54 || biOrig.biSize != 40 ||
        biOrig.biBitCount != 24 || biOrig.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 1;
    }

    // out file header params adjusting
    BITMAPFILEHEADER bfNew = bfOrig;
    BITMAPINFOHEADER biNew = biOrig;

    biNew.biWidth *= n;
    biNew.biHeight *= n;

    // determine padding for scanlines
    int paddingNew = (4 - (biNew.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int paddingOrig = (4 - (biOrig.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    biNew.biSizeImage = ((sizeof(RGBTRIPLE) * biNew.biWidth) + paddingNew) * abs(biNew.biHeight);

    bfNew.bfSize =  biNew.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bfNew, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&biNew, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(biOrig.biHeight); i < biHeight; i++)
    {
        // attributes for increased line
        RGBTRIPLE *newLine = NULL;
        newLine = malloc(biNew.biWidth * sizeof(RGBTRIPLE));
        int newLineIndex = 0;

        // iterate over pixels in scanline
        for (int j = 0; j < biOrig.biWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // assemble increased line
            for (int k = 0; k < n; k++)
            {
                newLine[newLineIndex++] = triple;
            }
        }

        // write new line
        for (int z = 0; z < n; z++)
        {
            fwrite(newLine, biNew.biWidth * sizeof(RGBTRIPLE), 1, outptr);
            // add padding if needed
            for (int k = 0; k < paddingNew; k++)
            {
                fputc(0x00, outptr);
            }
        }

        free(newLine);

        // skip over padding, if any
        fseek(inptr, paddingOrig, SEEK_CUR);

    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
