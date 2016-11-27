#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int encrypt (int input, int key);
int validInput (int argc, string argv[]);

int main (int argc, string argv[]) {
    //Validate input
    if ( !validInput(argc, argv) ) {
        printf("Usage: ./vigenere k\n");
        return 1;
    }

    printf("plaintext:  ");

    //Assign variables
    string plaintext = get_string();
    int keyLength = strlen(argv[1]);
    int key [keyLength];
    int currKey;
    char currChar;

    //Convert string key to number array
    for (int j = 0; j < keyLength; j++) {
        key[j] = toupper(argv[1][j]) - 65;
    }

    printf("ciphertext: ");

    //Iterate over string
    //i is the char index, k is the key index
    for (int i = 0, k = 0; i < strlen(plaintext); i++) {
        //Assign current character to encode
        //and current key to use
        currChar = plaintext[i];
        currKey = key[k % keyLength];

        //If letter
        if (isalpha(currChar)) {
            //Encrypt, print, and increment key index
            printf("%c", encrypt(currChar, currKey));
            k++;
        } else {
            //Else just print
            printf("%c", currChar);
        }
    }

    printf("\n");

    return 0;
}

int validInput (int argc, string argv[]) {
    //Make sure vigenere is given a key
    if (argc != 2) {
        return 0;
    }

    string input = argv[1];

    //Make sure the key is only letters
    for (int i = 0, n = strlen(input); i < n; i++) {
        if ( !isalpha(input[i]) ) {
            return 0;
        }
    }

    return 1;
}

int encrypt (int input, int key) {
    //Set base number based on if char is upper or lowercase
    int base = input > 96 ? 97 : 65;

    //Zero-index letter, mod through characters, and re-add base for ASCII
    return (input - base + key) % 26 + base;
}
