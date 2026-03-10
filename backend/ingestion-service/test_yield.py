"""
Test to understand yield behavior
"""

def my_function():
    print("A")
    yield 1
    print("B")
    yield 2
    print("C")

print("Creating generator...")
gen = my_function()

print("\nCalling next() first time:")
x = next(gen)
print(f"Got value: {x}")

print("\nCalling next() second time:")
y = next(gen)
print(f"Got value: {y}")

print("\nCalling next() third time:")
try:
    z = next(gen)
    print(f"Got value: {z}")
except StopIteration:
    print("Generator exhausted - no more yields!")
