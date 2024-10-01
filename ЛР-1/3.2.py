result = {"attempt": int, "answer": int}


def slow_search(secret: int) -> None:
    """
    Perform a linear search for the secret number.

    The search starts at 0 and increments by 1 until it reaches the secret number.

    The number of attempts and the guessed number are stored in the result dictionary.

    A message is printed to the console with the guessed number and the number of attempts made.

    Aproximate time complexity is O(n), where n is the secret number.
    """
    result["attempt"] = 0

    for guess in range(10000):
        result["attempt"] += 1

        if guess == secret:
            result["answer"] = guess
            break
    
    print("Slow search guessed number: ", str(result["answer"]),
          "after ", str(result["attempt"]), "attempts")


def binary_search(secret: int) -> None:
    """
    Perform a binary search for the secret number.

    The search starts at 0 and increments by half of the remaining range of possible values
    until it reaches the secret number.

    The number of attempts and the guessed number are stored in the result dictionary.

    A message is printed to the console with the guessed number and the number of attempts made.

    Aproximate time complexity is O(log(n)), where n is the secret number.
    """
    min = 0
    max = 10000
    guess = (min + max) // 2
    result["attempt"] = 0
    
    while secret != guess:
        result["attempt"] += 1
        
        if secret > guess:
            min = guess
        else:
            max = guess
        
        guess = (min + max) // 2
    
    result["answer"] = guess
    
    print("Binary search guessed number: ", str(result["answer"]),
          "after ", str(result["attempt"]), "attempts")


def main() -> None:
    slow_search(int(input("Enter a number between 0 and 10000: ")))

    binary_search(int(input("Enter a number between 0 and 10000: ")))


if __name__ == "__main__":
    main()
