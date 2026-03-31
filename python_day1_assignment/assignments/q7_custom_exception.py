# Q7: Custom Exception Handling
# Create our own custom exception called SalaryTooLowError
# Raise it when salary is less than 10000

# Step 1: Create a custom exception class (inherits from Exception)
class SalaryTooLowError(Exception):
    pass   # No extra code needed, just the class definition is enough

# Step 2: Function to check salary
def check_salary(salary):
    if salary < 10000:
        raise SalaryTooLowError("Salary is too low!")   # Raise our custom error

# Step 3: Use try-except to catch our custom error
salary = 8000

try:
    check_salary(salary)
    print("Salary is valid!")
except SalaryTooLowError as e:
    print("SalaryTooLowError")   # Output the error name
    print("Details:", e)
