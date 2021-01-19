#include <stdio.h>
#include <cs50.h>

void pyramid(int h, int total);

int main(void)
{
    int h = get_int("Height: ");
    while (h < 1 || h > 8)
    {
        h = get_int("Height: ");
    }
    pyramid(h, h);
}

void pyramid(int h, int total)
{
    if (h == 0)
        return;

    pyramid(h - 1, total);

    for (int i = 1; i <= total - h; i++)
    {
        printf(" ");
    }

    for (int i = 1; i <= h; i++)
    {
        printf("#");
    }

    printf("  ");

    for (int i = 1; i <= h; i++)
    {
        printf("#");
    }
    printf("\n");
}