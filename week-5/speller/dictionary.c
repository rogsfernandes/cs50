// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table
const unsigned int N = 26 * 26;

// Hash table
node *table[N];
int counter = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hash_value = hash(word);
    if (hash_value < 0 || hash_value > N)
    {
        return false;
    }

    if (table[hash_value] == NULL)
    {
        return false;
    }

    for (node *cursor = table[hash_value]; cursor != NULL; cursor = cursor->next)
    {
        // for each word in this bucket's linked list, compare
        for (int i = 0; i < strlen(word); i++)
        {
            // check if any character is different and, if so, steps out from this comparison
            if (tolower(word[i]) != cursor->word[i])
            {
                break;
            }

            // if the program reached the last char and didn't quited, equal match was found
            if (i == strlen(word) - 1)
            {
                if (strlen(word) == strlen(cursor->word))
                {
                    return true;
                }
            }
        }
    }

    return false;
}

// Hashes word to a number based on the first two letters
unsigned int hash(const char *word)
{
    // gets the index of first letter
    char first = tolower(word[0]);
    int first_idx = first - 'a';
    int second_idx = 0;
    int multiplier = 0;

    if (strlen(word) > 1)
    {
        char second = tolower(word[1]);
        second_idx = second - 'a';
    }

    // for each letter, we jump 25 positions to count aa, ab, ac (...) for example
    if (first_idx > 0)
    {
        multiplier = (first_idx * 25);
    }

    // this leads to idx 0 = aa and idx 675 = zz
    return first_idx + multiplier + second_idx;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // initializes hash table
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // reads dictionary file
    FILE *file = fopen(dictionary, "r");

    // if file is NULL, return false indicating an error happened
    if (file == NULL)
    {
        return false;
    }

    // allocate memory in a buffer to read from the file
    char *buffer = malloc(LENGTH + 1);

    // read each word from file and store in hash table
    while (fscanf(file, "%s", buffer) == 1)
    {
        // allocates memory for the new node in the linked list
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        // copy the word from dictionary into the node
        strcpy(n->word, buffer);
        // increase the words counter
        counter++;
        // initializes the next pointer with NULL value
        n->next = NULL;
        // computes the hash number
        int hash_number = hash(buffer);

        // if this is the first node in this hash table bucket,
        // insert it in the first position of the linked list(0)
        if (table[hash_number] == NULL)
        {
            table[hash_number] = n;
        }
        else
        {
            // navigates the linked list to find the last element, and then links it to the new one
            for (node *cursor = table[hash_number]; cursor != NULL; cursor = cursor->next)
            {
                if (cursor->next == NULL)
                {
                    cursor->next = n;
                    break;
                }
            }
        }
    }

    free(buffer);
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            node *tmp = malloc(sizeof(node));
            for (node *cursor = table[i]; cursor != NULL; cursor = cursor->next)
            {
                free(tmp);
                tmp = cursor;
            }
            free(tmp);
        }
    }

    return true;
}
