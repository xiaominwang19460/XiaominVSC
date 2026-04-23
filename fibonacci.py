def fibonacci(n):
    """Generate the first n Fibonacci numbers."""
    fib = []
    a, b = 0, 1
    for _ in range(n):
        fib.append(a)
        a, b = b, a + b
    return fib

# Print the first 10 Fibonacci numbers
numbers = fibonacci(10)
print("First 10 Fibonacci numbers:")
print(numbers)
