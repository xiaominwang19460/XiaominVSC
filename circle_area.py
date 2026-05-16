import math


def main():
    try:
        radius_input = input("Enter the circle radius: ")
        radius = float(radius_input)
    except ValueError:
        print("Invalid radius. Please enter a numeric value.")
        return

    if radius < 0:
        print("Radius cannot be negative.")
        return

    area = math.pi * radius ** 2
    print(f"The area of a circle with radius {radius} is {area}")


if __name__ == "__main__":
    main()
