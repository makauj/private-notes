#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>

/**
 * fizzBuzz - fizzbuzz leetcode function
 */

void fizzBuzz(void)
{
    int i = 1;
/*
    for (i = 1; i <= 100; i++)
    {
        if (i % 15 == 0)
            printf("FizzBuzz\n");
        else if (i % 3 == 0)
            printf("Fizz\n");
        else if (i % 5 == 0)
            printf("Buzz\n");
        else
            printf("%d\n", i);
    }
*/
    while (i <= 100){
        //if (i % 5 == 0 && i % 3 == 0)
        if (i % 15 == 0)
            printf("FizzBuzz\n");
        else if (i % 3 == 0)
            printf("Fizz\n");
        else if (i % 5 == 0)
            printf("Buzz\n");
        else
            printf("%d\n", i);

        i++;
    }
}

int main()
{
    fizzBuzz();
    return 0;
}