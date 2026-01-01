#include <stdio.h>
/**
 * solution: Finds the single unpaired element in an array where every other element
 * occurs exactly twice.
 * 
 * @A - input array of integers.
 * @N - number of elements in the array A.
 *
 * This function uses the XOR operation to cancel out paired elements:
 *   - For any integer x, x ^ x == 0 (a value XORed with itself is 0).
 *   - For any integer x, x ^ 0 == x (XOR with 0 leaves the value unchanged).
 *
 * By XORing all elements together, every number that appears twice cancels
 * out to 0, and only the value that appears once remains. That remaining
 * value is returned as the result.
 *
 * Returns: the unpaired element.
 **/
int solution(int A[], int N) {
    int result = 0;
    for (int i = 0; i < N; i++) {
        result ^= A[i];
    }
    return result;
}
