#include <stdio.h>
#include <cs50.h>
#include <math.h>

float GetPositiveFloat (void);

int main (void)
{
  int amount = round(GetPositiveFloat() * 100);
  int count = 0;
  int coins = 0;

//   printf("Amount: %f\n", round(amount * 100));

  while (count + 25 <= amount) {
      count += 25;
      coins++;
    //   printf("Quarter: %i\n", count);
  }

  while (count + 10 <= amount) {
      count += 10;
      coins++;
    //   printf("Dime: %i\n", count);
  }

  while (count + 5 <= amount) {
      count += 5;
      coins++;
    //   printf("Nickel: %i\n", count);
  }

  while (count + 1 <= amount) {
      count += 1;
      coins++;
    //   printf("Penny: %i\n", count);
  }

  printf("%i\n", coins);

}

float GetPositiveFloat (void)
{
    float amount;

    do {
        printf("How much money you need?\n");
        amount = GetFloat();
    } while (amount < 0);

    return amount;

}
