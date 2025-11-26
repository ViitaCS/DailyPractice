class Solution {
public:
  int mySqrt(int x) {
    int left = 0, right = x, res = -1;
    while (left <= right) {
      int middle = left + ((right - left) >> 1);
      if ((long long)middle * middle <= x) {
        res = middle;
        left = middle + 1;
      } else
        right = middle - 1;
    }
    return res;
  }
};