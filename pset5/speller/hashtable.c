// implements hashtable's functionality

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "hashtable.h"

// size of hashtable
#define HASH_TABLE_SIZE 65536

// array for hashtable
node *hashTbale[HASH_TABLE_SIZE] = {NULL};

// hash function
int hash(const char *string)
{
    unsigned int hash = 0;
    // using bitwise shift and xor opertaion for hash calculation
    for (int i = 0, n = strlen(string); i < n; i++)
    {
        hash = (hash << 2) ^ string[i];
    }
    return hash % HASH_TABLE_SIZE;
}


// procedure for search in list
int findItemInList(node  **list, const char *string)
{
    for (node *ptr = *list; ptr != NULL; ptr = ptr->next)
    {
        if (strcmp(string, ptr->string) == 0)
        {
            return 1;
        }
    }
    return 0;
}


// add item to linked list
int addNewItemToList(node **list, char *string)
{

    int found = findItemInList(list, string);

    if (!found)
    {
        // Allocate space for number
        node *n = malloc(sizeof(node));
        if (!n)
        {
            return 1;
        }

        // Add number to list
        strncpy(n->string, string, LENGTH);
        n->next = NULL;
        if (*list)
        {
            for (node *ptr = *list; ptr != NULL; ptr = ptr->next)
            {
                if (!ptr->next)
                {
                    ptr->next = n;
                    break;
                }
            }
        }
        else
        {
            *list = n;
        }
    }
    return 0;
}

// add string to hashtable
int addItemToHashTable(char *string)
{
    // index calculates by hash function
    return addNewItemToList(&hashTbale[hash(string)], string);
}

// find item by index
int findItemInHashTbale(const char *string)
{
    return findItemInList(&hashTbale[hash(string)], string);
}

// clear list
void clearList(node **list)
{
    node *ptr = *list;
    while (ptr != NULL)
    {
        node *next = ptr->next;
        free(ptr);
        ptr = next;
    }
}

// free memory
int clearHashTable(void)
{
    // go throw all array items
    for (int i = 0; i < HASH_TABLE_SIZE; i++)
    {
        // if adreess not null clear allocated memory
        if (hashTbale[i] != NULL)
        {
            clearList(&hashTbale[i]);
        }
    }
    return 1;
}

// count items in list
int countListItems(node **list)
{
    int i = 0;
    for (node *ptr = *list; ptr != NULL; ptr = ptr->next)
    {
        i++;
    }
    return i;
}

// count all intems in hash table
int countHashTableItems(void)
{
    int items = 0;
    // go throw all array items
    for (int i = 0; i < HASH_TABLE_SIZE; i++)
    {
        // if adrees not null go throw list and print items
        if (hashTbale[i] != NULL)
        {
            items += countListItems(&hashTbale[i]);
        }
    }

    return items;
}
