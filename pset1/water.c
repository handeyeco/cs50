#include <stdio.h>
#include <cs50.h>

int main (void)
{
    int n;
    printf("How long was your shower? (In minutes)\n");
    n = GetInt();
    n = (n * 192) / 16;
    printf("That's %i bottles of water!\n", n);
}
