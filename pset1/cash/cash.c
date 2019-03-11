#include <stdio.h>
#include <cs50.h>

double getValidchangeOwed(void);

int main(void)
{
    // total coins counter for result
    int coinsCounter = 0;
    double changeOwed = getValidchangeOwed();
    int intValueOfCoins = changeOwed * 100;

    //temporary result number of 25
    int tmp = intValueOfCoins / 25;
    coinsCounter += tmp;

    // left to issue after issuing 25
    intValueOfCoins %= 25;

    //temporary result number of 10
    tmp = intValueOfCoins / 10;

    coinsCounter += tmp;

    // left to issue after issuing 10
    intValueOfCoins %= 10;

    //temporary result number of 5
    tmp = intValueOfCoins / 5;

    coinsCounter += tmp;

    // left to issue after issuing 5
    intValueOfCoins %= 5;

    coinsCounter += intValueOfCoins;

    printf("%i\n", coinsCounter);
    return 0;
}

double getValidchangeOwed(void)
{
    double changeOwed;
    do
    {
        changeOwed = get_double("Change owed: ");
    }
    while (changeOwed < 0);

    return changeOwed;
}