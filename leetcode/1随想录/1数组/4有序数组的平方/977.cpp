class Solution {
public:
  vector<int> sortedSquares(vector<int> &nums) {
    int n = nums.size();
    vector<int> res(n);
    for (int i = 0, j = n - 1, fin = n - 1; i <= j;) {
      if (nums[i] * nums[i] > nums[j] * nums[j]) {
        res[fin] = nums[i] * nums[i];
        i++;
      } else {
        res[fin] = nums[j] * nums[j];
        j--;
      }
      fin--;
    }
    return res;
  }
};