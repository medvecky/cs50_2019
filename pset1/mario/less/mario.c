#include <stdio.h>
#include <cs50.h>

int get_valid_integer();

int main(void)
{
    // get valid height value
    int height = get_valid_integer();

    //two inner loops for pyramid drawing
    for (int row = 0; row < height; row++)
    {
        for (int column = 0; column <= height; column++)
        {
            // condition to form right pyramid
            if (column < height - 1 - row)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
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