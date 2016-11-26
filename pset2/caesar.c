#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int encrypt (int input, int key);

int main (int argc, string argv[]) {
    //Validate input
    if (argc != 2) {
        printf("Usage: ./caesar k\n");
        return 1;
    }

    printf("plaintext:  ");

    //Assign variables
    string plaintext = get_string();
    int key = atoi(argv[1]);
    char curr;

    printf("ciphertext: ");

    //Iterate over string
    for (int i = 0; i < strlen(plaintext); i++) {
        //Assign current char to current var
        curr = plaintext[i];

        //If letter
        if (isalpha(curr)) {
            //Encrypt and print
            printf("%c", encrypt(curr, key));
        } else {
            //Else just print
            printf("%c", curr);
        }
    }

    printf("\n");

    return 0;
}

int encrypt (int input, int key) {
    //Set base number based on if char is upper or lowercase
    int base = input > 96 ? 97 : 65;

    //Zero-index letter, mod through characters, and re-add base for ASCII
    return (input - base + key) % 26 + base;
}
