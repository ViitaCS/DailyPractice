#include <bits/stdc++.h>
using namespace std;

int main() {
  int n, m;
  cin >> n >> m;
  int sum = 0;
  vector<vector<int>> land(n, vector<int>(m, 0));
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
      cin >> land[i][j];
      sum += land[i][j];
    }
  }
  vector<int> x(n, 0);
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
      x[i] += land[i][j];
    }
  }
  vector<int> y(m, 0);
  for (int j = 0; j < m; j++) {
    for (int i = 0; i < n; i++) {
      y[j] += land[i][j];
    }
  }
  int res = INT_MAX;
  int xcut = 0, ycut = 0;
  for (int i = 0; i < n; i++) {
    xcut += x[i];
    res = min(res, abs(sum - xcut - xcut));
  }
  for (int j = 0; j < m; j++) {
    ycut += y[j];
    res = min(res, abs(sum - ycut - ycut));
  }
  cout << res << endl;
  return 0;
}