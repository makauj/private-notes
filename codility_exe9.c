#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int solution(int N)
{
    int maxGap = 0;
    int currentGap = 0;
    bool foundOne = false;

    while(N > 0){
        if (N & 1){
            if (foundOne && currentGap > maxGap){
                maxGap = currentGap;
            }
            foundOne = true;
            currentGap = 0;
        }
        else if (foundOne){
            currentGap++;
        }
        N >>= 1;
    }
    return maxGap;
}
