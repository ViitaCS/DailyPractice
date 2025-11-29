class Solution {
public:
  vector<vector<int>> generateMatrix(int n) {
    vector<vector<int>> matrix(n, vector<int>(n, 0));
    int cur = 1, x = 0, y = 0, offset = 1;
    int loop = n / 2, mid = n / 2;
    int i, j;
    while (loop--) {
      i = x;
      j = y;
      for (j; j < n - offset; j++) {
        matrix[i][j] = cur++;
      }
      for (i; i < n - offset; i++) {
        matrix[i][j] = cur++;
      }
      for (; j > x; j--) {
        matrix[i][j] = cur++;
      }
      for (; i > y; i--) {
        matrix[i][j] = cur++;
      }
      offset++;
      x++;
      y++;
    }
    if (n % 2) {
      matrix[mid][mid] = cur;
    }
    return matrix;
  }
};