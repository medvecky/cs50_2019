#define _XOPEN_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <cs50.h>
#include <string.h>

void possiblePasswodsGenerator(int numberOfSymbols, char *hash, char *salt);

// possible characters for passwords
const char *charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
// buffer for passwords
char buffer[50];

int main(int argc, char **argv)
{
    char salt[3];

    if (argc != 2)
    {
        printf("Usage: ./crack hash\n");
        return 1;
    }

    //init salt
    for (int i = 0; i < 3; i++)
    {
        salt[i] = argv[1][i];
    }
    salt[2] = '\0';

    // generate and check passwords
    for (int i = 0; i < 5; i++)
    {
        possiblePasswodsGenerator(i, argv[1], salt);
    }

    return 0;
}

// passwords generator
void possiblePasswodsGenerator(int numberOfSymbols, char *hash, char *salt)
{
    const char *charset_ptr = charset;
    if (numberOfSymbols == -1)
    {
        if (strcmp(hash, crypt(buffer, salt)) == 0)
        {
            printf("%s\n", buffer);
            exit(0);
        }
    }
    else
    {
        // recursive possible symbols enumeration
        while ((buffer[numberOfSymbols] = *charset_ptr++))
        {
            possiblePasswodsGenerator(numberOfSymbols - 1, hash, salt);
        }
    }
}