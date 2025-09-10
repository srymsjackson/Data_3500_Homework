# Homework 2 - Variables, Math, and Output!
# if you click run  on this entire hw2.py file, they are all 
# formatted and spaced out by problem.
# Hope that helps!



# ---HOMEWORK PROBLEM 2.3 (fill in the missing code)---

grade = 91 # declare the value so that the if statement even works

if grade >= 90:
    print('\nCongratulations! Your grade of 91 earns you an A in this course.\n') # value filled in that was missing

# ---HOMEWORK PROBLEM 2.4 (Artithmetic)---

27.5 + 2 # Addition
27.5 - 2 # Subtraction
27.5 * 2 # Multiplication
27.5 / 2 # True Division
27.5 // 2 # Floor Division
27.5 ** 2 # Exponentiation

# ---HOMEWORK PROBLEM 2.5 (Circle area, Diameter and Circumference)---

circle_radius = 2 # Given radius in problem
pi = 3.14159 # makes code smoother tbh

diameter = 2 * circle_radius # 2r
circumference = 2 * pi * circle_radius # 2πr
area = pi * circle_radius ** 2 # πr^2

# Then print each calculation of the circle given:
print("Diameter: " + str(diameter))
print("Circumference: " + str(circumference))
print("Area: " + str(area) + '\n')

# ---HOMEWORK PROBLEM 2.6 (Odd or Even?)---

integer_input = 67 # User inputs an integer 
remainder = integer_input % 2

if remainder == 0: # If the remainder equals 0, it is EVEN.
    print("Your integer is even!\n")
else: # If otherwise, ODD.
    print("Your integer is odd!\n")

# ---HOMEWORK PROBLEM 2.7 (Multiples)---

value1 = 1024 # Value #1 given in problem
value2 = 10 # Value #2 given in problem

mult_of_4 = value1 % 4
mult_of_2 = value2 % 2

if mult_of_4 == 0:
    print(str(value1) + " is a multiple of 4!") # This one will run, but the else block will not.
else:
    print(str(value1) + " isn't a multiple of 4...")
if mult_of_2 == 0:
    print(str(value2) + " is a multiple of 2!\n") # This one will also run, and the else block will not run as well.
else:
    print(str(value2) + " isn't a multiple of 2...")

# ---HOMEWORK PROBLEM 2.8 (Tables pf squares and cubes)---

print("number\tsquare\tcube")
str(print(0, "\t", 0 ** 2, "\t", 0 ** 3)) # Using \t to give that correct spacing
str(print(1, "\t", 1 ** 2, "\t", 1 ** 3))
str(print(2, "\t", 2 ** 2, "\t", 2 ** 3))
str(print(3, "\t", 3 ** 2, "\t", 3 ** 3))
str(print(4, "\t", 4 ** 2, "\t", 4 ** 3))
str(print(5, "\t", 5 ** 2, "\t", 5 ** 3))
print("\n")

#---------------------------------------------------------#
# if you have any questions at all or if I formatted this #
# in an inefficient way, just let me know. Thanks!        #
#---------------------------------------------------------#