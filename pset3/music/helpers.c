// Helper functions for music
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>
#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    // correct fraction check
    if (strlen(fraction) != 3)
    {
        printf("Invalid fraction.\n");
        return -1;
    }

    // parse and calculate the number of eighths
    if (fraction[2] == '8')
    {
        return (int)(fraction[0] - '0');
    }
    else
    {
        return 8 / (int)(fraction[2] - '0');
    }
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    int n = 0;
    // octave shift handling
    if (strlen(note) == 2)
    {
        n = 12 * ((int)(note[1] - '0') - 4);
    }
    else
    {
        // handling # and b if present
        n = 12 * ((int)(note[2] - '0') - 4);
        if (note[1] == '#')
        {
            n++;
        }
        else if (note[1] == 'b')
        {
            n--;
        }
    }

    // in octave note shift
    switch (note[0])
    {
        case 'B' :
            n += 2;
            break;
        case 'A' :
            break;
        case 'G' :
            n -= 2;
            break;
        case 'F' :
            n -= 4;
            break;
        case 'E' :
            n -= 5;
            break;
        case 'D' :
            n -= 7;
            break;
        case 'C' :
            n -= 9;
    }

    // final requency calculation
    int f = round(pow((double)2, (double)((double)n / 12)) * 440);
    return f;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (s[0] == '\0')
    {
        return true;
    }

    return false;
}
