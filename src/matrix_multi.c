#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 256

void matrix_multiply(int A[N][N], int B[N][N], int C[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            C[i][j] = 0;
            for (int k = 0; k < N; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main() {
    static int A[N][N], B[N][N], C[N][N];

    // Initialize matrices
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i][j] = i + j;
            B[i][j] = i - j;
        }
    }

    clock_t start = clock();
    matrix_multiply(A, B, C);
    clock_t end = clock();

    printf("Matrix multiplication completed\n");
    printf("Time: %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result checksum: %d\n", C[N/2][N/2]);

    return 0;
}
