# Q17: Smart Banking System (OOP + Encapsulation + SRP)
# OOP = Object Oriented Programming
# SRP = Single Responsibility Principle (each class does ONE job)
# Encapsulation = hiding data inside a class using private variables (__)

from datetime import datetime


# ---- Class 1: TransactionLogger (only job = log transactions) ----
class TransactionLogger:
    
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] LOG: {message}")


# ---- Class 2: Account (only job = manage balance) ----
class Account:
    
    def __init__(self, owner, starting_balance):
        self.__owner = owner               # __ makes it private (can't access directly)
        self.__balance = starting_balance  # __ makes it private
        self.__logger = TransactionLogger()  # Logger is used inside Account
    
    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive!")
            return
        self.__balance += amount
        self.__logger.log(f"Deposited {amount}. New balance: {self.__balance}")
    
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive!")
            return
        if amount > self.__balance:
            print("Not enough balance!")
            return
        self.__balance -= amount
        self.__logger.log(f"Withdrew {amount}. New balance: {self.__balance}")
    
    def get_balance(self):
        return self.__balance


# ---- Class 3: SavingsAccount (extends Account) ----
class SavingsAccount(Account):
    pass   # Same as Account for now, can add savings-specific features later


# ---- Test the system ----
acc = SavingsAccount("John", 1000)
acc.deposit(500)
acc.withdraw(200)
print("Balance:", acc.get_balance())
# Output: Balance: 1300
