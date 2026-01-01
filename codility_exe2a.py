
def solution(A, K):
    N = len(A)
    if N == 0:
        return A
    
    if K % N == 0:
        return A
    
    if K > N:
        K = K % N
    return A[-K:] + A[:-K]

# Example usage:
if __name__ == "__main__":
    A = [3, 8, 9, 7, 6]
    K = 3
    result1 = solution(A, K)
    print(result1)
    A = [0, 0, 1, 0, 0]
    K = 4
    result2 = solution(A, K)
    print(result2)
    A = [1, 2, 3, 4]
    K = 5
    result3 = solution(A, K)
    print(result3)