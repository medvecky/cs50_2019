// basic vigenere chipher encryption realisation
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

void encryptText(char *plainText, char *key);

bool comandLineArgsValidation(int argc, char **argv);

int main(int argc, char **argv)
{
    // check command line args
    if (!comandLineArgsValidation(argc, argv))
    {
        return 1;
    }

    // get plain text
    string plainText = get_string("plaintext: ");

    // call encryption function
    encryptText(plainText, argv[1]);

    printf("ciphertext: %s\n", plainText);

    return 0;
}

// text encryption
void encryptText(char *plainText, char *key)
{
    // init key params
    int keyIndex = 0;
    int keyLength = strlen(key);

    // actual key
    int k;

    for (int i = 0, l = strlen(plainText); i < l; i++)
    {
        // calculating of actual key value
        if (isupper(key[keyIndex]))
        {
            k = key[keyIndex] - 'A';
        }
        else
        {
            k = key[keyIndex] - 'a';
        }

        // onlu for alphabet characters
        if (isalpha(plainText[i]))
        {
            // for upper case
            if (isupper(plainText[i]))
            {
                plainText[i] = (((plainText[i] - 'A') + k) % 26) + 'A';
            }
            // for lower case
            else if (islower(plainText[i]))
            {
                plainText[i] = (((plainText[i] - 'a') + k) % 26) + 'a';
            }

            // iteration of keys
            if (++keyIndex == keyLength)
            {
                keyIndex = 0;
            }
        }
    }
}

// validation of command line args
bool comandLineArgsValidation(int argc, char **argv)
{
    // check for number of arguments
    if (argc != 2)
    {
        printf("Usage ./vigenere k\n");
        return false;
    }

    // check for arg  conatins only alphabet symblos
    for (int i = 0, l = strlen(argv[1]); i < l; i++)
    {
        if (!isalpha(argv[1][i]))
        {
            printf("Usage ./vigenere k\n");
            return false;
        }
    }
    return true;
}