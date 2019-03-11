#include <stdio.h>
#include <cs50.h>

int get_valid_integer();
void printBlocks(int numberOfBlocks);

int main(void)
{
    // get valid height value
    int height = get_valid_integer();

    //two inner loops for pyramid drawing
    for (int row = 0; row < height; row++)
    {
        // counter for blocks in left side
        int numberOfBlocks = 0;
        for (int column = 0; column < height; column++)
        {
            // condition to form right pyramid
            if (column < height - row - 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
                numberOfBlocks++;
            }

        }

        // hole in pyramid center
        printf("  ");

        //create rigth side of pyramid
        printBlocks(numberOfBlocks);

        printf("\n");
    }


    return 0;

}

// function to get valid Height value for mario game
int get_valid_integer()
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 0 || height > 23);
    return height;
}

// function for printing blocks
void printBlocks(int numberOfBlocks)
{
    for (int i = 0; i < numberOfBlocks; i++)
    {
        printf("#");
    }
}