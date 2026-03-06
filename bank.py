# ============================================
#        BANK MANAGEMENT SYSTEM
#        Uses Basic Python + OOP Concepts
# ============================================

# ---------------------------
# CLASS : BankAccount
# ---------------------------


class BankAccount:

    # __init__ is called automatically when we create a new account
    # self means "this account"
    def __init__(self, account_number, name, password, balance=0):
        self.account_number = account_number
        self.name = name
        self.password = password
        self.balance = balance
        self.transactions = []   # stores history of deposits/withdrawals

    # Method to deposit money
    def deposit(self, amount):
        if amount <= 0:
            print("  ❌ Amount must be greater than 0.")
            return
        self.balance += amount
        self.transactions.append(f"Deposited : +₹{amount}")
        print(f"  ✅ ₹{amount} deposited successfully!")
        print(f"  💰 New Balance: ₹{self.balance}")

    # Method to withdraw money
    def withdraw(self, amount):
        if amount <= 0:
            print("  ❌ Amount must be greater than 0.")
            return
        if amount > self.balance:
            print("  ❌ Not enough balance!")
            print(f"  💰 Available Balance: ₹{self.balance}")
            return
        self.balance -= amount
        self.transactions.append(f"Withdrawn  : -₹{amount}")
        print(f"  ✅ ₹{amount} withdrawn successfully!")
        print(f"  💰 Remaining Balance: ₹{self.balance}")

    # Method to check balance
    def check_balance(self):
        print(f"  💰 Account Balance: ₹{self.balance}")

    # Method to show all transactions
    def show_transactions(self):
        if len(self.transactions) == 0:
            print("  📭 No transactions yet.")
        else:
            print(f"  📋 Transaction History for {self.name}:")
            print("  " + "-" * 30)
            for t in self.transactions:
                print(f"  {t}")
            print("  " + "-" * 30)

    # Method to show account details
    def show_details(self):
        print(f"""
  ┌─────────────────────────────────┐
  │  Account Number : {self.account_number}
  │  Account Holder : {self.name}
  │  Balance        : ₹{self.balance}
  └─────────────────────────────────┘""")


# ---------------------------
# CLASS : Bank
# ---------------------------
# Bank class manages all accounts.
# It stores a list of BankAccount objects.

class Bank:

    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.accounts = []          # list to store all accounts
        self.next_account_number = 1001   # auto account number starting from 1001

    # Create a new account
    def create_account(self):
        print("\n  === Create New Account ===")
        name = input("  Enter your name       : ").strip()
        password = input("  Set a password        : ").strip()

        if name == "" or password == "":
            print("  ❌ Name and password cannot be empty.")
            return

        opening_balance = input("  Opening balance (₹)  : ").strip()

        # Check if opening balance is a valid number
        if not opening_balance.isdigit():
            print("  ❌ Please enter a valid amount.")
            return

        opening_balance = int(opening_balance)

        # Create a new BankAccount object
        new_account = BankAccount(self.next_account_number, name, password, opening_balance)

        # Add it to our list of accounts
        self.accounts.append(new_account)

        print(f"\n  ✅ Account created successfully!")
        print(f"  📌 Your Account Number : {self.next_account_number}")
        print(f"  📌 Keep this number safe to login.\n")

        # Increase account number for next person
        self.next_account_number += 1

    # Find an account by account number
    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None   # if not found, return None

    # Login to an account
    def login(self):
        print("\n  === Login to Your Account ===")
        acc_input = input("  Enter Account Number : ").strip()

        if not acc_input.isdigit():
            print("  ❌ Invalid account number.")
            return None

        acc_number = int(acc_input)
        account = self.find_account(acc_number)

        if account is None:
            print("  ❌ Account not found.")
            return None

        password = input("  Enter Password       : ").strip()

        if account.password != password:
            print("  ❌ Wrong password.")
            return None

        print(f"\n  ✅ Welcome, {account.name}!")
        return account   # return the account if login is successful

    # Show all accounts (admin feature)
    def show_all_accounts(self):
        if len(self.accounts) == 0:
            print("\n  📭 No accounts found in the bank.")
            return

        print(f"\n  === All Accounts in {self.bank_name} ===")
        print("  " + "-" * 45)
        print(f"  {'Acc No':<10} {'Name':<20} {'Balance':>10}")
        print("  " + "-" * 45)
        for account in self.accounts:
            print(f"  {account.account_number:<10} {account.name:<20} ₹{account.balance:>8}")
        print("  " + "-" * 45)

    # Transfer money between two accounts
    def transfer_money(self, from_account):
        print("\n  === Transfer Money ===")
        to_acc_input = input("  Enter recipient Account Number : ").strip()

        if not to_acc_input.isdigit():
            print("  ❌ Invalid account number.")
            return

        to_acc_number = int(to_acc_input)

        if to_acc_number == from_account.account_number:
            print("  ❌ You cannot transfer to your own account.")
            return

        to_account = self.find_account(to_acc_number)

        if to_account is None:
            print("  ❌ Recipient account not found.")
            return

        amount_input = input("  Enter amount to transfer (₹) : ").strip()

        if not amount_input.isdigit():
            print("  ❌ Please enter a valid amount.")
            return

        amount = int(amount_input)

        if amount <= 0:
            print("  ❌ Amount must be greater than 0.")
            return

        if amount > from_account.balance:
            print("  ❌ Not enough balance to transfer.")
            return

        # Deduct from sender, add to receiver
        from_account.balance -= amount
        to_account.balance += amount

        from_account.transactions.append(f"Transferred: -₹{amount} to Acc {to_acc_number}")
        to_account.transactions.append(f"Received   : +₹{amount} from Acc {from_account.account_number}")

        print(f"  ✅ ₹{amount} transferred to {to_account.name} successfully!")
        print(f"  💰 Your new balance: ₹{from_account.balance}")

    # Delete an account
    def delete_account(self, account):
        confirm = input(f"\n  ⚠️  Are you sure you want to delete your account? (yes/no) : ").strip()
        if confirm.lower() == "yes":
            self.accounts.remove(account)
            print("  ✅ Account deleted successfully.")
            return True
        else:
            print("  Cancelled.")
            return False

    # Change password
    def change_password(self, account):
        print("\n  === Change Password ===")
        old_pass = input("  Enter current password : ").strip()
        if old_pass != account.password:
            print("  ❌ Wrong password.")
            return
        new_pass = input("  Enter new password     : ").strip()
        confirm  = input("  Confirm new password   : ").strip()
        if new_pass != confirm:
            print("  ❌ Passwords do not match.")
            return
        account.password = new_pass
        print("  ✅ Password changed successfully!")


# ---------------------------
# MENUS
# ---------------------------

def account_menu(bank, account):
    # This menu appears after a user logs in
    while True:
        print(f"""
  ====================================
    Welcome, {account.name}
  ====================================
  1. Check Balance
  2. Deposit Money
  3. Withdraw Money
  4. Transfer Money
  5. View Transactions
  6. View Account Details
  7. Change Password
  8. Delete Account
  0. Logout
  ------------------------------------""")

        choice = input("  Choose an option : ").strip()

        if choice == "1":
            account.check_balance()

        elif choice == "2":
            amount = input("  Enter deposit amount (₹) : ").strip()
            if amount.isdigit():
                account.deposit(int(amount))
            else:
                print("  ❌ Please enter a valid number.")

        elif choice == "3":
            amount = input("  Enter withdrawal amount (₹) : ").strip()
            if amount.isdigit():
                account.withdraw(int(amount))
            else:
                print("  ❌ Please enter a valid number.")

        elif choice == "4":
            bank.transfer_money(account)

        elif choice == "5":
            account.show_transactions()

        elif choice == "6":
            account.show_details()

        elif choice == "7":
            bank.change_password(account)

        elif choice == "8":
            deleted = bank.delete_account(account)
            if deleted:
                break   # go back to main menu after deletion

        elif choice == "0":
            print(f"\n  👋 Goodbye, {account.name}! Logged out.\n")
            break

        else:
            print("  ⚠️  Invalid option. Please try again.")


def main_menu(bank):
    # This is the starting menu everyone sees
    while True:
        print(f"""
  ╔══════════════════════════════════╗
  ║   🏦  {bank.bank_name:<28}      ║
  ╠══════════════════════════════════╣
  ║  1. Create New Account           ║
  ║  2. Login to Account             ║
  ║  3. View All Accounts (Admin)    ║
  ║  0. Exit                         ║
  ╚══════════════════════════════════╝""")

        choice = input("  Choose an option : ").strip()

        if choice == "1":
            bank.create_account()

        elif choice == "2":
            account = bank.login()
            if account is not None:
                account_menu(bank, account)

        elif choice == "3":
            bank.show_all_accounts()

        elif choice == "0":
            print("\n  👋 Thank you for using our bank. Goodbye!\n")
            break

        else:
            print("  ⚠️  Invalid option. Please try again.")


# ---------------------------
# START THE PROGRAM
# ---------------------------

# Create a Bank object
my_bank = Bank("Python National Bank")

# Start the main menu
main_menu(my_bank)