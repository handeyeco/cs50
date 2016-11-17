#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int isLetter (char c);

int main (void)
{
    //Get string input from user
    string name = GetString();

    //Loop over every char in input string
    for (int i = 0, n = strlen(name); i < n; i++)
    {
        //Create a var for the current and previous char
        char now = name[i];
        char then = name[i - 1];

        //If the previous char is not a letter
        //And the current one is, we can assume it's part of the initial
        if ( (isLetter(then) != 1) && isLetter(now) )
        {
            //Convert lowercase to uppercase
            if (now > 96)
            {
                now = toupper(now);
            }

            //Print initial char
            printf("%c", now);
        }
    }

    //End initials with new line
    printf("\n");
}

//Take a char and determine if it's a letter of some sort
int isLetter (char c)
{
    //Check to see if it's an uppercase or lowercase letter
    if ( (c > 64 && c < 91) || (c > 96 && c < 123) )
    {
        //If so return truthy
        return 1;
    }

    //Else return falsey
    return 0;
}
