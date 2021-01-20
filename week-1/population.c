#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int start_size;
    int end_size;
    int years = 0;

    do
    {
        start_size = get_int("Start size: ");
    } while (start_size < 9);

    do
    {
        end_size = get_int("End size: ");
    } while (end_size < start_size);

    while (start_size < end_size)
    {
        int born = start_size / 3;
        int die = start_size / 4;
        start_size = start_size + born - die;
        years++;
    }

    printf("Years: %i\n", years);
}