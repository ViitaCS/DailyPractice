#include <cs50.h>
#include <stdio.h>

void print(int cur, int height);

int main(void)
{
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8); // 输入检查

    for (int i = 0; i < h; i++) // 决定打印的行数
    {
        print(i, h);
    }
}
// 根据高度逐行打印
void print(int cur, int height)
{
    for (int i = height; i > cur + 1; i--)
    {
        printf(" ");
    }
    for (int i = 0; i <= cur; i++)
    {
        printf("#");
    }
    printf("  ");
    for (int i = 0; i <= cur; i++)
    {
        printf("#");
    }
    printf("\n");
}
