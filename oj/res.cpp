#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
  int digit;
  struct Node *prev;
  struct Node *next;
} Node;

typedef struct {
  Node *head;
  Node *tail;
  int sign;
} BigInt;

Node *createNode(int digit) {
  Node *newNode = (Node *)malloc(sizeof(Node));
  newNode->digit = digit;
  newNode->prev = NULL;
  newNode->next = NULL;
  return newNode;
}

void freeList(Node *head) {
  while (head) {
    Node *temp = head;
    head = head->next;
    free(temp);
  }
}

BigInt parseStringToBigInt(const char *str) {
  BigInt num;
  num.head = NULL;
  num.tail = NULL;
  num.sign = 1;

  int start = 0;
  if (str[0] == '-') {
    num.sign = -1;
    start = 1;
  }

  int len = strlen(str);
  char *cleanStr = (char *)malloc(len + 1);
  int cleanIndex = 0;
  for (int i = start; i < len; i++) {
    if (str[i] != ',')
      cleanStr[cleanIndex++] = str[i];
  }
  cleanStr[cleanIndex] = '\0';
  len = cleanIndex;

  int groupCount = (len + 3) / 4;
  int firstGroupLen = len % 4;
  if (firstGroupLen == 0)
    firstGroupLen = 4;

  char temp[5] = {0};
  strncpy(temp, cleanStr, firstGroupLen);
  num.head = createNode(atoi(temp));
  num.tail = num.head;

  Node *current = num.head;
  for (int i = firstGroupLen; i < len; i += 4) {
    strncpy(temp, &cleanStr[i], 4);
    Node *newNode = createNode(atoi(temp));
    current->next = newNode;
    newNode->prev = current;
    current = newNode;
    num.tail = current;
  }

  free(cleanStr);
  return num;
}

int compareAbs(BigInt a, BigInt b) {

  int lenA = 0, lenB = 0;
  for (Node *p = a.head; p; p = p->next)
    lenA++;
  for (Node *p = b.head; p; p = p->next)
    lenB++;

  if (lenA != lenB)
    return (lenA > lenB) ? 1 : -1;

  Node *pA = a.head, *pB = b.head;
  while (pA) {
    if (pA->digit != pB->digit)
      return (pA->digit > pB->digit) ? 1 : -1;
    pA = pA->next;
    pB = pB->next;
  }
  return 0;
}

BigInt absAdd(BigInt a, BigInt b) {
  BigInt res = {NULL, NULL, 1};
  int carry = 0;
  Node *currA = a.tail, *currB = b.tail;

  while (currA || currB || carry) {
    int sum = carry;
    if (currA) {
      sum += currA->digit;
      currA = currA->prev;
    }
    if (currB) {
      sum += currB->digit;
      currB = currB->prev;
    }

    carry = sum / 10000;
    Node *newNode = createNode(sum % 10000);

    if (!res.head)
      res.head = res.tail = newNode;
    else {
      newNode->next = res.head;
      res.head->prev = newNode;
      res.head = newNode;
    }
  }
  return res;
}

BigInt absSub(BigInt a, BigInt b) {
  BigInt res = {NULL, NULL, 1};
  int borrow = 0;
  Node *currA = a.tail, *currB = b.tail;

  while (currA) {
    int valA = currA->digit - borrow;
    int valB = currB ? currB->digit : 0;
    borrow = 0;

    if (valA < valB) {
      valA += 10000;
      borrow = 1;
    }

    Node *newNode = createNode(valA - valB);
    if (!res.head)
      res.head = res.tail = newNode;
    else {
      newNode->next = res.head;
      res.head->prev = newNode;
      res.head = newNode;
    }

    currA = currA->prev;
    if (currB)
      currB = currB->prev;
  }

  while (res.head != res.tail && res.head->digit == 0) {
    Node *temp = res.head;
    res.head = res.head->next;
    res.head->prev = NULL;
    free(temp);
  }
  return res;
}

BigInt addBigInt(BigInt a, BigInt b) {

  if (a.sign == b.sign) {
    BigInt res = absAdd(a, b);
    res.sign = a.sign;
    return res;
  }

  int cmp = compareAbs(a, b);
  if (cmp == 0) {
    BigInt res = {createNode(0), NULL, 1};
    res.tail = res.head;
    return res;
  }

  if (cmp > 0) { // |a|>|b|
    BigInt res = absSub(a, b);
    res.sign = a.sign;
    return res;
  } else { // |b|>|a|
    BigInt res = absSub(b, a);
    res.sign = b.sign;
    return res;
  }
}

void printFormatted(BigInt num) {
  if (num.sign == -1 && num.head->digit != 0)
    printf("-");

  Node *cur = num.head;
  while (cur) {

    if (cur == num.head)
      printf("%d", cur->digit);
    else
      printf("%04d", cur->digit);

    if (cur->next)
      printf(",");
    cur = cur->next;
  }
  printf("\n");
}

int main() {
  char str1[1000], str2[1000];

  fgets(str1, sizeof(str1), stdin);
  fgets(str2, sizeof(str2), stdin);
  str1[strcspn(str1, "\n")] = '\0';
  str2[strcspn(str2, "\n")] = '\0';

  BigInt num1 = parseStringToBigInt(str1);
  printFormatted(num1);

  BigInt num2 = parseStringToBigInt(str2);
  printFormatted(num2);
  printf("\n");

  BigInt result = addBigInt(num1, num2);
  printFormatted(result);

  freeList(num1.head);
  freeList(num2.head);
  freeList(result.head);

  return 0;
}