#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int startSize;
    int endSize;
    int years = 0;

    do
    {
        startSize = get_int("Start size: ");
    } while (startSize < 9);

    do
    {
        endSize = get_int("End size: ");
    } while (endSize < startSize);

    while (startSize < endSize)
    {
        int born = startSize / 3;
        int die = startSize / 4;
        startSize = startSize + born - die;
        years++;
    }

    printf("Years: %i\n", years);
}