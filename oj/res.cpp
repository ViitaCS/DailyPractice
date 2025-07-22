#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
  int trap(vector<int> &height) {
    int n = height.size();
    if (n < 3)
      return 0;

    int left = 0, right = n - 1;
    int left_max = 0, right_max = 0;
    int ans = 0;

    while (left < right) 
    {
      if (height[left] < height[right]) 
      {
        if (height[left] >= left_max) 
        {
          left_max = height[left]; 
        } 
        else 
        {
          ans += left_max - height[left];
        }
        left++; 
      }
      else 
      {
        if (height[right] >= right_max) 
        {
          right_max = height[right]; 
        } 
        else 
        {
          ans += right_max - height[right]; 
        }
        right--; 
      }
    }
    return ans;
  }
};

int main() {
  int h;
  vector<int> v;
  while (cin >> h) {
    v.push_back(h);
  }
  int res = Solution().trap(v);
  cout << res << endl;
  return 0;
}