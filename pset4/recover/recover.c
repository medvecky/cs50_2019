// extract jpeg files from memory card dump

#include <stdio.h>
#include <stdint.h>

#define BLOCK_SIZE 512
#define FILENAME_LENGTH 8

int main(int argc, char **argv)
{
    // output filename
    char outfileName[FILENAME_LENGTH];
    // buffer for read data
    uint8_t readWriteBuffer[BLOCK_SIZE];

    // extracted jpge counter
    int extratedJpegCounter = 0;

    // pointer for out file
    FILE *outptr = NULL;

    // chaeck for correct args
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // store image name
    char *infile = argv[1];

    // try to open the image file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // main read image loop
    while (fread(readWriteBuffer, 1, BLOCK_SIZE, inptr) == BLOCK_SIZE)
    {
        //find begin of jpeg
        if ((unsigned)readWriteBuffer[0] == 0xff &&
            (unsigned)readWriteBuffer[1] == 0xd8 &&
            (unsigned)readWriteBuffer[2] == 0xff &&
            ((unsigned)readWriteBuffer[3] & 0xf0) == 0xe0)
        {
            // close previous out file if exist
            if (extratedJpegCounter > 0)
            {
                fclose(outptr);
            }
            // increment counter
            extratedJpegCounter++;

            // generate name
            sprintf(outfileName, "%03d.jpg", extratedJpegCounter - 1);

            // open new file writing data
            outptr = fopen(outfileName, "w");
            if (outptr == NULL)
            {
                fprintf(stderr, "Could not open %s.\n", outfileName);
                return 2;
            }
        }

        // write readed data portion to outeput file
        if (outptr != NULL)
        {
            fwrite(readWriteBuffer, BLOCK_SIZE, 1, outptr);
        }
    }

    // close files
    fclose(inptr);

    if (outptr != NULL)
    {
        fclose(outptr);
    }



    return 0;
}