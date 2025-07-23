#include <iostream>
#include <queue>
#include <vector>
using namespace std;

class Solution {
public:
  vector<vector<int>> kSmallestPairs(vector<int> &nums1, vector<int> &nums2,int k) 
  {
    if (nums1.empty() || nums2.empty() || k == 0)
      return {};
    auto cmp = [&](const pair<int, int> &a, const pair<int, int> &b) 
    {
      return nums1[a.first] + nums2[a.second] >
             nums1[b.first] + nums2[b.second];
    };
    priority_queue<pair<int, int>, vector<pair<int, int>>, decltype(cmp)> pq(cmp);
    int m = nums1.size();
    for (int i = 0; i < min(m, k); ++i) 
    {
      pq.push({i, 0});
    }
    vector<vector<int>> res;
    while (k > 0 && !pq.empty()) 
    {
      auto top = pq.top();
      int i = top.first;
      int j = top.second;
      pq.pop();
      res.push_back({nums1[i], nums2[j]});
      k--;
      if (j + 1 < nums2.size()) 
      {
        pq.push({i, j + 1});
      }
    }
    return res;
  }
};

int main() {
  int n, m, data, k;
  vector<int> nums1, nums2;
  cin >> n;
  for (int i = 0; i < n; ++i) 
  {
    cin >> data;
    nums1.push_back(data);
  }
  cin >> m;
  for (int i = 0; i < m; ++i) 
  {
    cin >> data;
    nums2.push_back(data);
  }
  cin >> k;
  vector<vector<int>> res = Solution().kSmallestPairs(nums1, nums2, k);
  for (int i = 0; i < res.size(); ++i)
  {
    if (i > 0)
      cout << " ";
    cout << res[i][0] + res[i][1];
  }
  return 0;
}