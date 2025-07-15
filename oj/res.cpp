#include <cstddef>
#include <iostream>
#include <vector>
using namespace std;

struct ListNode {
  int val;
  ListNode *next;
  ListNode() : val(0), next(NULL) {}
  ListNode(int x) : val(x), next(NULL) {}
  ListNode(int x, ListNode *next) : val(x), next(next) {}
};
class Solution {
public:
  vector<ListNode *> splitListToParts(ListNode *root, int k) {
    int count = 0;
    ListNode *cur = root;
    while (cur) {
      count++;
      cur = cur->next;
    }

    int m = count / k;
    int n = count % k;
    vector<ListNode *> result(k, nullptr);
    cur = root;
    for (int i = 0; i < k && cur; i++) {
      result[i] = cur;
      int ex = m + (i < n ? 1 : 0);
      for (int j = 0; j < ex - 1; j++) {
        cur = cur->next;
      }
      ListNode *next = cur->next;
      cur->next = nullptr;
      cur = next;
    }
    return result;
  }
};
ListNode *createByTail() {
  ListNode *head;
  ListNode *p1, *p2;
  int n = 0, num;
  int len;
  cin >> len;
  head = NULL;
  while (n < len && cin >> num) {
    p1 = new ListNode(num);
    n = n + 1;
    if (n == 1)
      head = p1;
    else
      p2->next = p1;
    p2 = p1;
  }
  return head;
}
void display(vector<ListNode *> lnVec) {
  for (size_t i = 0; i < lnVec.size(); i++) {
    ListNode *p;
    p = lnVec[i];
    cout << "head-->";
    while (p != NULL) {
      cout << p->val << "-->";
      p = p->next;
    }
    cout << "tail\n";
  }
}
int main() {
  vector<int> G;
  int k;
  ListNode *head = createByTail();
  cin >> k;
  vector<ListNode *> lnVec = Solution().splitListToParts(head, k);
  display(lnVec);
  return 0;
}