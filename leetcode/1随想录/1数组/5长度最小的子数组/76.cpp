class Solution {
public:
  string minWindow(string s, string t) {
    vector<int> hash(128, 0); // 哈希表记录字符需求及窗口频次
    for (char c : t)
      hash[c]--; // 将t中字符需求标记为负数
    int sLen = s.length(), tLen = t.length();
    int count = 0;
    int minLen = sLen + 1;
    int subLeft = -1;
    for (int i = 0, j = 0; j < sLen; j++) {
      char c = s[j];
      if (hash[c] < 0)
        count++; // 当前字符是t中的所需字符，且未达需求
      hash[c]++; // 更新窗口中字符频次
      // 收缩窗口：移除冗余字符（频次超过需求或非t字符）
      while (i < j && hash[s[i]] > 0) {
        hash[s[i]]--;
        i++;
      }
      // 更新最小窗口
      if (count == tLen && j - i + 1 < minLen) {
        minLen = j - i + 1;
        subLeft = i;
      }
    }
    return subLeft >= 0 ? s.substr(subLeft, minLen) : "";
  }
};