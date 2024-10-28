# Sorting Algorithms (The Big O)

## Introduction
In computer science, sorting is a fundamental concept. It involves arranging data in a particular order.

## Concepts

### Big O notation

This is a powerful tool used in computer science to describe the time/space complexity of algorithms.

#### Understanding Big O notation

Big O is a way of expressing the upper bound of an algorithm's time complexity. Big O, also refered to as "Order of" is used to analyze the worst-case situation of an algorithm.

It is important to note that Big O only describes the asymptotic behaviour of a function, not its exact value.
Big O notation can be used to compare the efficiency of different algorithms or data structures.

**Definition of Big-O Notation**
given two functions `f(n)` and `g(n)`, we can say `f(n)` is `O(g(n))` if constants `c > 0` and n~0~ >= 0 exist, such that `f(n) <= c*g(n)` for all n >= n~0~.
Simply put, `f(n)` is `O(g(n))` if `f(n)` does not grow faster than `c*g(n)` for all n >= n~0~ where `c` and n~0~ are constants.


The C programming language has several algoriths that can be used for this purpose.
These are:

## 1. Selection Sort

This is a simple comparison-based algorithm.
```c
#include <stdio.h>

void selectionSort(int arr[], int n) {
    int i, j, min_idx;
    for (i = 0; i < n-1; i++) {
        min_idx = i;
        for (j = i+1; j < n; j++) {
            if (arr[j] < arr[min_idx])
                min_idx = j;
        }
        int temp = arr[min_idx];
        arr[min_idx] = arr[i];
        arr[i] = temp;
    }
}

void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main() {
    int arr[] = {64, 25, 12, 22, 11};
    int n = sizeof(arr)/sizeof(arr[0]);
    selectionSort(arr, n);
    printf("Sorted array: \n");
    printArray(arr, n);
    return 0;
}

```

```python
def selection_sort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

# Example usage
my_array = [64, 25, 12, 22, 11]
sorted_array = selection_sort(my_array)
print("Sorted array:", sorted_array)

```

## Insertion sort

Insertion sort work in a similar way to how we sort playing cards in our hands.
We begin be splitting the the array into sorted and unsorted regions. We then pick elements from the unsorted region and placing them into the appropriate position in the sorted region.
The final array is built one item at a time.
This sorting algorithm is not as efficient as quicksort on larger lists.

```c
#include <stdio.h>

void insertionSort(int array[], int size)
{
    int key, j, step;

    for (step = 1; step < size; step++)
    {
        key = array[step];
        j = step - 1;

        /**
         * Compare key with each element on the left of it until an element
         * smaller than it is found.
         * For descending order, change key<array[j] to key>array[j].
        */
        while (key < array[j] && j >= 0)
        {
            array[j + 1] = array[j];
            --j;
        }
        array[j + 1] = key;
    }
}
```

## Selection Sort

This is a simple comparison based algorithm tht divides the input list in two.
One is a sorted sublist of items is built up fro left to right to one side of the list (left side), and a sublist of the remaining unsorted items that occupy the rest of the list.



## Bubble Sort

This is, arguably, the simplest sorting algorith. It works by repeatedly swapping adjascent elements if they are in the wrong order. This make it very inefficient for large datasets due to its rather high time complexity in both average and worst-case scenarios.

**Process**
Sort the array using multiple passes. The max element goes to the end after the first pass then the second largest goes to the second last position in the next pass and so on.
Each pass only processes elements that haven't been sorted yet and moves them to their correct position.
In a pass, we compare all adjascent elements and swap if larger element is before a smaller element. Reapeat this process until the data is sorted.


```c
#include <stdbool.h>
#include <stdio.h>

void swap(int* xp, int* yp){
    int temp = *xp;
    *xp = *yp;
    *yp = temp;
}

/* An optimized version of Bubble Sort */
void bubbleSort(int arr[], int n){
    int i, j;
    bool swapped;
    for (i = 0; i < n - 1; i++) {
        swapped = false;
        for (j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(&arr[j], &arr[j + 1]);
                swapped = true;
            }
        }

        /**
         * If no two elements were swapped by inner loop,
         * then break
         */
        if (swapped == false)
            break;
    }
}
```

### Cocktail Sort

This is a variation of bubble sort that helps improve its performance/efficiency in large data sets.
This algorithm traverses through the data set in both directions alternatively. It does not go through the unnecessary iterations.
The basic idea of the cocktail sort is:
- Start at the beginning of the array and compare each adjascent pair of elements. Swap them if they are in the wrong order
- Do this for each position in the array.
- Move in the opposite direction from the end of the array to the beginning and compare each adjacent pair of elements and swapping them if necessary. Do this for each position in the negative direction until you reach the beginning of the array.
- Repeat this process until the array is sorted.

**Advantages**
1. More efficient than bubble sort
2. Easy to understand and implement for smaller data sets. Also good for learning purposes

**Disadvantages**
1. It has a worst-case time complexity of `O(n^2)`. This is slow for large data sets or partialy sorted data sets
2. Needs additional bookkeeping to track start and end indices.
3. Algorithim has poorer memory management than other algorithms.


## Counting Sort

This is a non-comparison-based sorting algorithm that is efficient when sorting a range of values that is not significantly larger than the number of elements to be sorted. It operates by counting the occurences of each distinct element in the input array and then using this count to determine the sorted position of each element.

### how it works
1. find the maximum element (max) in the array
2. Initialize the array of length `max + 1` with all elements 0. This array is used for sorting the count of the elements in the array.
3. 