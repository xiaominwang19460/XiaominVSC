import random

secret_number = random.randint(1, 1000)

while True:
    guess = input("Guess a number between 1 and 1000: ")
    try:
        guess_int = int(guess)
    except ValueError:
        print("Invalid input. Please enter a integer.")
        continue
    if guess_int == secret_number:
        print("Congratulations!")
        break
    elif guess_int < secret_number:
        print("Too low! Try again.")
    else:
        print("Too high! Try again.")