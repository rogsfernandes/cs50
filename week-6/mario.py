from cs50 import get_int


def main():
    height = get_int("Height: ")
    while height < 1 or height > 8:
        height = get_int("Height: ")
    print_pyramid(height)


def print_pyramid(height, original_height=None):
    if original_height == None:
        original_height = height
    if height == 0:
        return

    print_pyramid(height-1, original_height)
    blocks = ""

    # print left pad
    print("".rjust(original_height - height), end="")
    # concatenate blocks
    for i in range(height):
        blocks += "#"
    print(f"{blocks}  {blocks}")


if __name__ == "__main__":
    main()
