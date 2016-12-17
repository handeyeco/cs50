/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

int trie_size = 0;

// The base of the trie
node* trie;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // Set cursor to beginning of trie
    node* point = trie;

    // Iterate over chars in word
    for (int idx = 0, length = strlen(word); idx < length; idx++) {
        // Grab letter
        int letter = word[idx];

        // Convert letter to lowercase
        if (letter >= 64 && letter <= 90) {
            letter += 32;
        }
        // Convert letter to array index value
        if (letter >= 97 && letter <= 122) {
            letter -= 97;
        } else {
            // For apostrophe
            letter = 26;
        }

        if (point->inner_array[letter] == NULL) {
            return false;
        } else {
            point = point->inner_array[letter];
        }

    }

    return point->is_word;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // Try to open dictionary and break if it fails
    FILE* doc = fopen(dictionary, "r");
    if (doc == NULL) {
        printf("Unable to open dictionary.\n");
        return false;
    }

    // initialize trie with null values
    trie = calloc(1, sizeof(node));

    node* point = trie;

    for (int letter = fgetc(doc); letter != EOF; letter = fgetc(doc)) {
        if (letter != '\n') {
            // Convert letter to lowercase
            if (letter >= 64 && letter <= 90) {
                letter += 32;
            }
            // Convert letter to array index value
            if (letter >= 97 && letter <= 122) {
                letter -= 97;
            } else {
                // For apostrophe
                letter = 26;
            }

            // If there is not a node, create one
            if (point->inner_array[letter] == NULL) {
                point->inner_array[letter] = calloc(1, sizeof(node));
            }

            // Move cursor to point at new node
            point = point->inner_array[letter];
        } else {
            // When finished with a word, set node to recognize word
            point->is_word = true;

            // Reset cursor
            point = trie;

            // Increment size
            trie_size++;
        }
    }

    // In the end, close file
    fclose(doc);

    // And signal success
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // Return size incremented during load
    return trie_size;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    unloader(trie);

    return true;
}

void unloader(node* current) {
    for (int i = 0; i < ALPHA; i++) {
        if (current->inner_array[i] != NULL) {
            unloader(current->inner_array[i]);
        }
    }

    free(current);
}
