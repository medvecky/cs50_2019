#include <stdio.h>
#include <cs50.h>

int getNunmberOfDigits(long long cardNumber);

void putCardNumberToArray(int *cardNumberAsArray, int numberOfDigits, long long cardNumber);

void chekcCard(int *cardNumberAsArray, int numberOfDigits);

long long getValidCardNumber();

bool checkControlSum(int *cardNumberAsArray, int numberOfDigits);

void checkCompanyIdentifierAndFormat(int *cardNumberAsArray, int numberOfDigits);

int main(void)
{
    //pointer for array representation of card number
    int *cardNumberAsArray = NULL;

    long long cardNumber = getValidCardNumber();

    //get number of card numbers digits
    int numberOfDigits = getNunmberOfDigits(cardNumber);

    // allocate memory for card number as array representation
    cardNumberAsArray = malloc(numberOfDigits * sizeof(int));

    //put card number digits to array
    putCardNumberToArray(cardNumberAsArray, numberOfDigits, cardNumber);

    chekcCard(cardNumberAsArray, numberOfDigits);

    free(cardNumberAsArray);
    cardNumberAsArray = NULL;

    return 0;
}

// function return number of digits and put card number as array to allocated memory
int getNunmberOfDigits(long long cardNumber)
{
    // tmp copy of number for number of digits calculating
    long long tmp = cardNumber;

    int numberOfDigits = 0;

    // count numbcer of digits in card number
    while (tmp > 0)
    {
        numberOfDigits++;
        tmp /= 10;
    }

    return numberOfDigits;
}

void putCardNumberToArray(int *cardNumberAsArray, int numberOfDigits, long long cardNumber)
{
    for (int i = 0; i < numberOfDigits; i++)
    {
        cardNumberAsArray[i] = cardNumber % 10;
        cardNumber /= 10;
    }
}

// card verification main procedure
void chekcCard(int *cardNumberAsArray, int numberOfDigits)
{
    if (checkControlSum(cardNumberAsArray, numberOfDigits))
    {
        checkCompanyIdentifierAndFormat(cardNumberAsArray, numberOfDigits);
    }
    else
    {
        printf("INVALID\n");
    }
}

// get card number with rude validation
long long getValidCardNumber()
{

    long long cardNumber;

    do
    {
        cardNumber = get_long_long("Number: ");
    }
    while (cardNumber <= 0);

    return cardNumber;
}

// control sum verification procedure
bool checkControlSum(int *cardNumberAsArray, int numberOfDigits)
{
    int controlSum = 0;
    // first part of control sum
    for (int i = 0; i < numberOfDigits; i++)
    {
        int tmp = cardNumberAsArray[i];
        if (i % 2 == 0)
        {
            controlSum += tmp;
        }
        else
        {
            tmp *= 2;
            if (tmp > 9)
            {
                controlSum += tmp % 10;
                controlSum += tmp / 10;
            }
            else
            {
                controlSum += tmp;
            }
        }
    }

    // last number check
    if (controlSum % 10 == 0)
    {
        return true;
    }

    return false;
}

// check company identifiers and valid number of digits
void checkCompanyIdentifierAndFormat(int *cardNumberAsArray, int numberOfDigits)
{
    // 34 37 for AMEX
    if ((cardNumberAsArray[numberOfDigits - 1] == 3) && (cardNumberAsArray[numberOfDigits - 2] == 4 ||
            cardNumberAsArray[numberOfDigits - 2] == 7))
    {
        if (numberOfDigits == 15)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    // check for master card 51 52 53 54
    else if (((cardNumberAsArray[numberOfDigits - 1] == 5) &&
              (cardNumberAsArray[numberOfDigits - 2] == 1 ||
               cardNumberAsArray[numberOfDigits - 2] == 2 ||
               cardNumberAsArray[numberOfDigits - 2] == 3 ||
               cardNumberAsArray[numberOfDigits - 2] == 4 ||
               cardNumberAsArray[numberOfDigits - 2] == 5)))
    {
        if (numberOfDigits == 16)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    // check for visa
    else if (cardNumberAsArray[numberOfDigits - 1] == 4)
    {
        if (numberOfDigits == 16 || numberOfDigits == 13)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
