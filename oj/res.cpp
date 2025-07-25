#include <iostream>
using namespace std;

struct ListNode 
{
  int val;
  ListNode *next;
  ListNode() : val(0), next(nullptr) {}
  ListNode(int x) : val(x), next(nullptr) {}
  ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution 
{
public:
  ListNode *removeNth(ListNode *head, int n) 
  {
    if (head == nullptr)
      return nullptr;

    ListNode *dummy = new ListNode(0);
    dummy->next = head;
    ListNode *slow = dummy;
    ListNode *fast = dummy;
    int L = n; 
    for (int i = 0; i < n; i++) 
    {
      if (fast == nullptr)
        break;
      fast = fast->next;
      if (i < n - 1) 
      {
        slow = slow->next;
      }
    }
    ListNode *prev1 = slow;   
    ListNode *target1 = fast; 
    ListNode *p = dummy;
    ListNode *current = fast; 
    while (current != nullptr && current->next != nullptr)
    {
      p = p->next;
      current = current->next;
      L++;
    }
    ListNode *prev2 = p;         
    ListNode *target2 = p->next; 
    int pos1 = n;
    int pos2 = L - n + 1;
    if (target1 == target2) 
    {
      prev1->next = target1->next;
    } 
    else 
    {
      if (pos1 < pos2) 
      {
        prev2->next = target2->next;
        prev1->next = prev1->next->next;
      } 
      else 
      {
        prev1->next = target1->next;
        prev2->next = prev2->next->next;
      }
    }
    ListNode *result = dummy->next;
    delete dummy;
    return result;
  }
};

ListNode *createByTail() 
{
  ListNode *head;
  ListNode *p1, *p2;
  int n = 0, num;
  int len;
  cin >> len;
  head = nullptr;
  while (n < len && cin >> num) {
    p1 = new ListNode(num);
    n++;
    if (n == 1)
      head = p1;
    else
      p2->next = p1;
    p2 = p1;
  }
  return head;
}

void displayLink(ListNode *head) 
{
  ListNode *p;
  p = head;
  cout << "head-->";
  while (p != nullptr) {
    cout << p->val << "-->";
    p = p->next;
  }
  cout << "tail\n";
}

int main() 
{
  ListNode *head = createByTail();
  int n;
  cin >> n;
  head = Solution().removeNth(head, n);
  displayLink(head);
  return 0;
}