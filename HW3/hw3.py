'''
3.4 (Fill in the Missing Code) In the code below
for ***:
    for ***:
        print('@')
    print()

replace the *** so that when you execute the code, it displays two rows, each containing seven @ symbols, as in:

@@@@@@@
@@@@@@@
'''
# the rows
for i in range(2):
    for j in range(7): # Makes 7 "columns" (if you will)
        print('@', end='') # end='' is used in print to avoid moving to the next line after printing '@'
    print() # AND BOOM

'''
3.9 (Separating the Digits in an Integer)
In Exercise 2.11, you wrote a script that separated a 
five-digit integer into its individual digits and displayed them. Reimplement your script to use a 
loop that in each iteration “picks off” one digit (left to right) using the // and % operators, 
then displays that digit.
'''
number = int(input("Enter a five-digit integer: "))
divisor = 10000  # Start with the highest place value for a five-digit number
while divisor >= 1:
    digit = number // divisor  # Get the leftmost digit
    print(digit)  # Display the digit
    number = number % divisor  # Remove the leftmost digit from the number
    divisor //= 10  # Move to the next lower place value

'''
3.11 (Miles Per Gallon)
Drivers are concerned with the mileage obtained by their automobiles. 
One driver has kept track of several tankfuls of gasoline by recording miles driven and gallons 
used for each tankful. Develop a sentinel-controlled-repetition script that prompts the user to 
input the miles driven and gallons used for each tankful. The script should calculate and display 
the miles per gallon obtained for each tankful. After processing all input information, the script 
should calculate and display the combined miles per gallon obtained for all tankfuls (that is, total 
miles driven divided by total gallons used).


Enter the gallons used (-1 to end): 12.8
Enter the miles driven: 287
The miles/gallon for this tank was 22.421875
Enter the gallons used (-1 to end): 10.3
Enter the miles driven: 200
The miles/gallon for this tank was 19.417475
Enter the gallons used (-1 to end): 5
Enter the miles driven: 120
The miles/gallon for this tank was 24.000000
Enter the gallons used (-1 to end): -1
The overall average miles/gallon was 21.601423
'''

total_miles = 0
total_gallons = 0

gallons_used = float(input("Enter the gallons used (-1 to end): "))

while gallons_used != -1:
    miles_driven = float(input("Enter the miles driven: "))
    
    mpg = miles_driven / gallons_used
    print(f"The miles/gallon for this tank was", mpg)
    
    # add to totals
    total_miles += miles_driven
    total_gallons += gallons_used
    
    # ask again
    gallons_used = float(input("Enter the gallons used (-1 to end): "))

# after loop, if any totals exist
if total_gallons > 0:
    overall_mpg = total_miles / total_gallons
    print(f"The overall average miles/gallon was", overall_mpg)
else:
    print("No data entered.")

'''
3.12 (Palindromes) 
A palindrome is a number, word or text phrase that reads the same backwards or forwards. For example, 
each of the following five-digit integers is a palindrome: 12321, 55555, 45554 and 11611. Write a script 
that reads in a five-digit integer and determines whether it's a palindrome. [Hint: Use the // and % operators 
to separate the number into its digits.]
'''

n = int(input("Enter a five-digit integer that is a palindrome: "))

if 10000 <= n <= 99999: # Makes sure the length is 5
    d1 = n // 10000
    d2 = (n // 1000) % 10
    d3 = (n // 100) % 10
    d4 = (n // 10) % 10
    d5 = n % 10

    if d1 == d5 and d2 == d4: # If the first and last are the same AND 2nd and 4th are the same (middle num don't matter)
        print("Awesome Palendrome!")
    else: # if otherwise:
        print("That isn't a palindrome unfortunately.")
else: # In case the length is anything BUT 5:
    print("That ain't a 5-digit number... smh.") # Shame the user.

'''
3.14 (Challenge: Approximating the Mathematical Constant π)
Write a script that computes the value of π from the following infinite series. Print a table that shows 
the value of π approximated by one term of this series, by two terms, by three terms, and so on. How many 
terms of this series do you have to use before you first get 3.14? 3.141? 3.1415? 3.14159?
'''

target_values = [3.14, 3.141, 3.1415, 3.14159] # The values we are searching for, in this case pi
found = {v: None for v in target_values}

sum = 0
pi_approx = 0

for i in range(1, 100000):
    term = ((-1) ** (i+1)) / (2*i - 1)
    sum += term
    pi_approx = 4 * sum

    # print the first few to see that table:
    if i <= 20:
        print("Term", i, ":", pi_approx)

    # Check when approximate pi (pi_approx) hits our target value(s)
    for v in target_values:
        if found[v] is None and round(pi_approx, len(str(v))-2) == v:
            found[v] = i
            print(v, "reached at term", i)

print("\nSummary:")
for v, n in found.items():
    print(f"{v} was first reached at term {n}")

# I used a lot of help from ChatGPT mostly because I did NOT understand the math to this problem. 
# Also that last bit of code was helped too. Such a hard question tbh