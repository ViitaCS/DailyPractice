class Solution {
public:
  int searchInsert(vector<int> &nums, int target) {
    int left = 0;
    int right = nums.size() - 1;
    while (left <= right) {
      int middle = left + ((right - left) >> 1);
      if (nums[middle] == target)
        return middle;
      else if (nums[middle] < target)
        left = middle + 1;
      else
        right = middle - 1;
    }
    return right + 1;
  }
};