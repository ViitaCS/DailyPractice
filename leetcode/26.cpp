class Solution {
public:
  int removeDuplicates(vector<int> &nums) {
    int low = 0;
    for (int i = 0; i < nums.size(); i++) {
      if (nums[low] != nums[i]) {
        low++;
        nums[low] = nums[i];
      }
    }
    return low + 1;
  }
};