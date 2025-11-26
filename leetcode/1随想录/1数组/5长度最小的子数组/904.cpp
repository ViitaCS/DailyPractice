class Solution {
public:
  int totalFruit(vector<int> &fruits) {
    int n = fruits.size();
    unordered_map<int, int> res;
    int left = 0, ans = 0;
    for (int right = 0; right < n; ++right) {
      ++res[fruits[right]];
      while (res.size() > 2) {
        auto it = res.find(fruits[left]);
        --it->second;
        if (it->second == 0) {
          res.erase(it);
        }
        ++left;
      }
      ans = max(ans, right - left + 1);
    }
    return ans;
  }
};