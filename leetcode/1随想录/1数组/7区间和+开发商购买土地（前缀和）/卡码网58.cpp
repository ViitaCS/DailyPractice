#include <bits/stdc++.h>
using namespace std;

int main() {
  int n, a, b, s;
  cin >> n;
  vector<int> res(n);
  vector<int> sum(n);
  cin >> res[0];
  sum[0] = res[0];
  for (int i = 1; i < n; i++) {
    cin >> res[i];
    sum[i] = sum[i - 1] + res[i];
  }
  while (cin >> a >> b) {
    if (a == 0)
      s = sum[b];
    else
      s = sum[b] - sum[a - 1];
    cout << s << endl;
  }
  return 0;
}