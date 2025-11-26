class Solution {
public:
  vector<int> searchRange(vector<int> &nums, int target) {
    int left = 0;
    int right = nums.size() - 1;
    int temp = -1;
    int middle = left + ((right - left) >> 1);
    while (left <= right) {
      middle = left + ((right - left) >> 1);
      if (nums[middle] == target) {
        temp = middle;
        break;
      } else if (nums[middle] < target) {
        left = middle + 1;
      } else {
        right = middle - 1;
      }
    }
    if (temp == -1)
      return {-1, -1};
    left = middle;
    right = middle;
    while (left >= 0 && nums[left] == target) {
      left--;
    }
    while (right <= nums.size() - 1 && nums[right] == target) {
      right++;
    }
    return {left + 1, right - 1};
  }
};