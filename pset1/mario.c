#include <stdio.h>
#include <cs50.h>

int GetPositiveInt(void);

int main (void)
{
    int height = GetPositiveInt();

    for (int lines = 1; lines <= height; lines++) {
        for (int squares = 0; squares <= height; squares++) {
            if (squares >= (height - lines)) {
                printf("#");
            } else {
                printf(" ");
            }
        }
        printf("\n");
    }
}

int GetPositiveInt (void)
{
    int n;
    do
    {
        printf("How big do you want it?\n");
        n = GetInt();
    }
    while (n < 0 || n > 23);
    return n;
}
