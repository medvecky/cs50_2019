// Implements a dictionary's functionality
#define _GNU_SOURCE
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "dictionary.h"

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // convert word to lowes case
    int len = strlen(word);
    char *wordLower = malloc(len + 1);
    int i;
    for (i = 0; i < len; i++)
    {
        wordLower[i] = tolower(word[i]);
    }
    wordLower[i++] = '\0';

    // find word in hashtable
    if (findItemInHashTbale(wordLower))
    {
        free(wordLower);
        return true;
    }
    free(wordLower);
    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // variables for getline
    char *line = NULL;
    size_t len = 0;
    size_t read;

    // open dicionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return false;
    }

    // read file line by line and put to hash table
    while ((read = getline(&line, &len, file)) != -1)
    {
        line[strlen(line) - 1] = '\0';
        addItemToHashTable(line);
    }

    // free memory after string
    free(line);
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return countHashTableItems();
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    if (clearHashTable() == 1)
    {
        return true;
    }
    return false;
}
