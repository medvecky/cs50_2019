// declares hashtable's functionality

// max word length based on dictionary.h declaration
#include "dictionary.h"

// struct for one string
typedef struct node
{
    char string[LENGTH];
    struct node *next;
}
node;

