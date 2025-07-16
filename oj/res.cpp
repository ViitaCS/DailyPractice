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
  ListNode *reverseKGroup(ListNode *head, int k) {
    if (k == 1 || !head)
      return head;
    ListNode *dummy = new ListNode(0);
    dummy->next = head;
    ListNode *preGroupEnd = dummy;
    while (true) {
      ListNode *curr = preGroupEnd->next;
      ListNode *groupStart = curr;
      int count = 0;
      while (curr && count < k) {
        curr = curr->next;
        count++;
      }
      if (count < k)
        break;
      ListNode *prev = curr;
      ListNode *node = groupStart;
      for (int i = 0; i < k; i++) {
        ListNode *nextNode = node->next;
        node->next = prev;
        prev = node;
        node = nextNode;
      }
      preGroupEnd->next = prev;
      preGroupEnd = groupStart;
    }
    ListNode *newHead = dummy->next;
    delete dummy;
    return newHead;
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
void displayLink(ListNode *head) {
  ListNode *p;
  p = head;
  cout << "head-->";
  while (p != NULL) {
    cout << p->val << "-->";
    p = p->next;
  }
  cout << "tail\n";
}
int main() {
  int k;
  ListNode *head = createByTail();
  cin >> k;
  head = Solution().reverseKGroup(head, k);
  displayLink(head);
  return 0;
}