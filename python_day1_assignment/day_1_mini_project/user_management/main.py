# main.py
# This is the entry point of the program - run this file to start the app
# It shows the menu and calls the right function based on user choice

from utils import register_user, login_user, view_users, delete_user

def show_menu():
    """Print the main menu options."""
    print("\n=============================")
    print("   User Management System   ")
    print("=============================")
    print("1. Register User")
    print("2. Login")
    print("3. View Users")
    print("4. Delete User")
    print("5. Exit")
    print("=============================")

def main():
    """Main loop - keeps showing menu until user chooses Exit."""
    
    while True:
        show_menu()
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            register_user()
        
        elif choice == "2":
            login_user()
        
        elif choice == "3":
            view_users()
        
        elif choice == "4":
            delete_user()
        
        elif choice == "5":
            print("Goodbye!")
            break   # Exit the while loop and end the program
        
        else:
            print("Invalid choice! Please enter a number between 1 and 5.")


# This is the standard Python way to run main() only when this file is executed directly
if __name__ == "__main__":
    main()
