class Solution {
public:
  bool isPerfectSquare(int num) {
    int left = 0, right = num;
    while (left <= right) {
      int middle = left + ((right - left) >> 1);
      if ((long long)middle * middle == num)
        return true;
      else if ((long long)middle * middle < num)
        left = middle + 1;
      else
        right = middle - 1;
    }
    return false;
  }
};