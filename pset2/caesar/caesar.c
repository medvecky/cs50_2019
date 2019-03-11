// basic caesar chipher encryption realisation
#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(int argc, char **argv)
{
    // check command line args
    if (argc != 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }

    // get numeric key value
    int k = atoi(argv[1]);

    eprintf("%d\n", k);

    // get plain text
    string plainText = get_string("plaintext: ");

    // text encryption
    for (int i = 0, l = strlen(plainText); i < l; i++)
    {
        // for upper case
        if (plainText[i] >= 65 && plainText[i] <= 90)
        {
            plainText[i] = (((plainText[i] - 65) + k) % 26) + 65;
        }
        // for lower case
        else if (plainText[i] >= 97 && plainText[i] <= 121)
        {
            plainText[i] = (((plainText[i] - 97) + k) % 26) + 97;
        }
    }

    printf("ciphertext: %s\n", plainText);

    return 0;
}