import os
from abc import ABC, abstractmethod
from datetime import datetime


class Choice():
    def user_choice(self):
        print("\n\t\t\t\tWELCOME TO CAKE&BAKE")
        while True:
            print("1:SIGNUP: press 1\n2.LOGIN: press 2\n3.MANAGAER LOGIN: press 3")
            ch = input("Enter your choice: ")
            if ch == '1':
                return Signup().username  # Sign up a new user
            elif ch == '2':
                l = Login()
                return l.login_user()  # Log in an existing user
            elif ch == '3':
                # Handle manager login logic here
                manager = Manager('product_list.txt')  # Create a Manager object
                manager.menu()
                break
            else:
                print("\n\t\t\tInvalid choice. Please enter 1, 2, or 3.")
                return self.user_choice()


class Signup:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.password2 = ""
        self.email = ""
        self.get_credentials()  # Collect user credentials
        self.create_account()  # Create a new account with the collected credentials

    def get_credentials(self):
        while True:
            # Prompt the user for a username
            self.username = input("Enter your username (should be 6 or more characters): ").strip().lower()
            if len(self.username) < 6:
                print("USERNAME TOO SHORT\nPlease enter a username with 6 or more characters:")
            elif self.username.isdigit():
                print("USERNAME INVALID\nUsername should not contain only digits.")
            else:
                break
        self.password = input("Enter your password: ")
        self.password2 = input("Confirm password: ")
        self.email = input("Enter your email: ")
        datafile = open("database.txt", "a")  # Save the credentials in the database file
        datafile.write(f"{self.username},{self.password}\n")

    def create_account(self):
        file_name = f"{self.username}_info.txt"
        # Check if the username is already taken
        if os.path.exists(file_name):
            print("\n\t\t\tUsername already taken, try new user name")
            self.get_credentials()

        if self.password == self.password2:
            print("YOU HAVE SUCCESSFULLY CREATED YOUR ACCOUNT")

            # Create a new file for the user

            try:
                with open(file_name, "w") as user_file:
                    user_file.write(f"Username: {self.username}\nPassword: {self.password}\nEmail: {self.email}")
            except IOError as e:
                print(f"Failed to create file: {e}")
        else:
            print("\n\t\t\tPASSWORD DOESN'T MATCH")
            # Ask for credentials again if passwords do not match
            self.get_credentials()


class Login():
    def __init__(self):  # creating a function for creating account(login)
        self.username = input("Enter your username: ").strip().lower()
        self.password = input("Enter your password: ")

    def login_user(self):
        l = []  # initializing empty lists to append usernames and passwords to save in txt file
        l2 = []
        # Read the database and store usernames and passwords
        db = open("database.txt", "r")
        for i in db:
            a, b = i.split(",")
            l.append(a)
            l2.append(b)
        data = dict(zip(l, l2))
        now = datetime.now()
        current_date = now.date()
        current_date = str(current_date)
        current_time = now.time()
        current_time = str(current_time)
        # Check if the username exists in the database
        if self.username in data:
            print("login successful")
            file = f"{self.username}_info.txt"
            f = open(file, 'a')  # writing data to file of individual user
            f.write('\n' + 'Account login date : ' + current_date + '\n' + 'Account login time : ' + current_time)
            f.close()
            return self.username
        else:
            print('\n\t\t\tAccount does not exist')
            c = Choice()
            c.user_choice()
            return self.username



# abstract base class for products
class AbstractProduct(ABC):
    def __init__(self, name, price, quantity):
        self._name = name
        self._price = price
        self._quantity = quantity

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def quantity(self):
        return self._quantity

    @abstractmethod
    def get_discounted_price(self):
        pass


# inherit from AbstractProduct class

class Product(AbstractProduct):
    def __init__(self, name, price, quantity):
        super().__init__(name, price, quantity)

    def update_quantity(self, quantity):
        self._quantity += quantity

    def get_discounted_price(self):
        return self._price - (self._price * 0.20)


# The Manager class owns an instance of the ProductManager class.
class Manager:
    def __init__(self, filename):
        self.product_manager = ProductManager(filename)
        while True:
            self.m_user = input("Enter account holder's name: ").strip().lower()
            self.password = input("Enter correct password: ")
            if self.m_user == 'haniya' and self.password == 'itiscomplicated00':
                # self.product_manager.display()
                break
            else:
                print("\n\t\t\tUSERNAME AND PASSWORD SHOULD BE CORRECT TO LOGIN!!!!\n")

    def add_products(self):
        print("\nCurrent Products:")
        self.product_manager.display()
        while True:
            try:
                product_name = input("Enter new product name: ")
                price = float(input("Enter its price: "))
                quantity = int(input("Enter its quantity: "))
            except ValueError:
                print("\n\t\t\tPrice should be a decimal value and Quantity should be an integer and Product name should be a valid Product.\n")
                continue

            if self.product_manager.product_exists(product_name):
                print("This product already exists. Do you want to update its quantity instead?")
                update_choice = input("Type YES to update quantity, otherwise NO: ").strip().lower()
                if update_choice == 'yes':
                    self.product_manager.update_product_quantity(product_name, quantity)
                else:
                    continue
            else:
                self.product_manager.add_product(product_name, price, quantity)
                self.product_manager.update_product_list()

            user = input("Do you want to add more products? Type YES otherwise type NO ").strip().lower()
            if user != 'yes':
                break

    def remove_products(self):
        print("\nCurrent Products:")
        self.product_manager.display()
        while True:
            try:
                product_number = int(input("Enter product number to remove: "))
                self.product_manager.remove_product(product_number)
                self.product_manager.update_product_list()
                user_input = input("Do you want to remove more products? (yes/no): ").strip().lower()
                if user_input != 'yes':
                    break
            except ValueError:
                print("Please enter a valid product number.")

    def add_quantity(self):
        print("\nCurrent Products:")
        self.product_manager.display()
        while True:
            try:
                product_number = int(input("Enter product number to add quantity: "))
                quantity = int(input("Enter quantity to add: "))
                self.product_manager.update_product_quantity_by_number(product_number, quantity)
                break
            except ValueError:
                print("\n\t\t\tPlease enter a valid product number and quantity.")

    def remove_quantity(self):
        print("\nCurrent Products:")
        self.product_manager.display()
        while True:
            try:
                product_number = int(input("Enter product number to remove quantity: "))
                quantity = int(input("Enter quantity to remove: "))
                self.product_manager.update_product_quantity_by_number(product_number, -quantity)
                break
            except ValueError:
                print("\n\t\t\tPlease enter a valid product number and quantity.")

    def show_products(self):
        self.product_manager.display()

    def menu(self):
        while True:
            print("\nManager Menu:")
            print("1. Add Product")
            print("2. Remove Product")
            print("3. Add Product Quantity")
            print("4. Remove Product Quantity")
            print("5. Show Products")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_products()
            elif choice == "2":
                self.remove_products()
            elif choice == "3":
                self.add_quantity()
            elif choice == "4":
                self.remove_quantity()
            elif choice == "5":
                self.show_products()
            elif choice == "6":
                print("GOING TO MAIN MENU")
                break
            else:
                print("Invalid choice. Please try again.")


class ProductManager:
    def __init__(self, filename):
        self.filename = filename
        self.products = {}
        self.load_products()

    def load_products(self):
        try:
            with open(self.filename, 'r') as file:  # read product_list.txt file
                for line in file:
                    if line.strip():
                        product_info = line.strip().split(
                            ", ")  # for example -> Product: Chocolate cake, Price: 1499.0, Quantity: 70
                        product_name = product_info[0].split(": ")[1]  # chocolate cake
                        product_price = float(product_info[1].split(": ")[1])  # 1499.0
                        product_quantity = int(product_info[2].split(": ")[1])  # 100
                        product_number = len(self.products) + 1
                        self.products[product_number] = Product(product_name, product_price,
                                                                product_quantity)  # Aggregates Product instances in a dictionary
        except FileNotFoundError:
            print(f"File '{self.filename}' not found. Initializing with empty product list.")

    def save_products(self):
        with open(self.filename, 'w') as file:
            for key, product in self.products.items():
                file.write(f"Product: {product.name}, Price: {product.price}, Quantity: {product.quantity}\n")

    def product_exists(self, name):
        for product in self.products.values():
            if product.name.lower() == name.lower():
                return True
        return False

    def add_product(self, name, price, quantity):
        product_number = len(self.products) + 1
        self.products[product_number] = Product(name, price, quantity)
        self.save_products()
        print("Product added successfully.")

    def remove_product(self, product_number):
        if product_number in self.products:
            del self.products[product_number]
            self.save_products()
            print("Product removed successfully.")
        else:
            print("Invalid product number.")

    def update_product_quantity(self, name, quantity):
        for product in self.products.values():
            if product.name.lower() == name.lower():
                product.update_quantity(quantity)
                self.save_products()
                print("Product quantity updated successfully.")
                return
        print("Product not found.")

    def update_product_quantity_by_number(self, product_number, quantity):
        if product_number in self.products:
            self.products[product_number].update_quantity(quantity)
            self.save_products()
            print("Product quantity updated successfully.")
        else:
            print("Invalid product number.")

    def update_product_list(self):
        self.save_products()

    def display(self):
        if not self.products:
            print("No products available.")
        else:
            for number, product in self.products.items():
                print(f"{number}. {product.name} - {product.price} - Quantity: {product.quantity}")


# associated with productmanager class
class Cart:
    def __init__(self, username, product_manager):
        self.cart = {}
        self.product_manager = product_manager
        self.username = username
        self.history = History(username)
        self.total = 0

    def remove_from_cart(self):
        if not self.cart:
            print("Your cart is empty. Please add products to the cart before attempting to remove.")
            return

        # Show cart contents with product numbers
        product_numbers,_ = self.show_cart()

        try:
            product_number = int(input('Enter the product number(from the cart) to remove: '))
            if product_number not in product_numbers:
                print("Invalid product number. Please try again.")
                return

            product_name = product_numbers[product_number]
            quantity = int(input('Enter the quantity to remove: '))

            if self.cart[product_name]["quantity"] >= quantity:
                self.cart[product_name]["quantity"] -= quantity
                if self.cart[product_name]["quantity"] == 0:
                    del self.cart[product_name]
                print(f"Removed {quantity} {product_name}(s) from the cart.")

                # Update the product quantity in the product manager
                for product in self.product_manager.products.values():
                    if product.name.lower() == product_name.lower():
                        product.update_quantity(quantity)
                        break

                self.product_manager.update_product_list()
            else:
                print(f"Cannot remove {quantity} {product_name}(s) from the cart. Not enough quantity in the cart.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def show_cart(self):
        self.total = 0
        print("\nYour Shopping Cart:")
        product_numbers = {}
        for idx, (product_name, details) in enumerate(self.cart.items(), start=1):
            product_total = details['price'] * details['quantity']
            print(f"{idx}. {product_name} - {details['quantity']} units - Rs{product_total}")
            self.total += product_total
            product_numbers[idx] = product_name
        total_product_bill = round(self.total, 2)
        print(f"Total Bill : Rs{round(self.total, 2)}")
        return product_numbers, total_product_bill

    def add_to_cart(self, product_number, quantity):

        # try:
        #      product_number = int(product_number)
        #      quantity = int(quantity)
        # except ValueError:
        #      print("Invalid input. Please enter valid numbers for product number and quantity.")
        #      return

        if product_number in self.product_manager.products:
            product = self.product_manager.products[product_number]
            product_name = product.name
            if product.quantity >= quantity:
                if product_name in self.cart:
                    self.cart[product_name]['quantity'] += quantity
                else:
                    self.cart[product_name] = {"price": product.get_discounted_price(), "quantity": quantity}
                product.update_quantity(-quantity)
                print(f"Added {quantity} {product_name}(s) to the cart.")
                self.product_manager.update_product_list()
                _, total_rounded = self.show_cart()
                self.history.add_purchase(product_name, quantity, self.cart[product_name]['price'], total_rounded)
            else:
                print(f"Not enough {product_name} in stock.")
        else:
            print(f"Product number {product_number} does not exist.")

    def checkout(self):
        if not self.cart:
            print("Cart is empty.")

        confirmation = input("Are you sure you want to checkout? (yes/no): ").strip().lower()
        if confirmation != "yes":
            print("Checkout Cancelled")
        while True:
            payment_method = input("Would you like to pay through COD or Debit Card? (COD/Debit Card): ").strip().lower()
            if payment_method == "cod":
                print("Your order has been placed and will be delivered soon.")
                break
            elif payment_method == "debit card":
                debit_no = input("Enter your debit card number (6 digits): ").strip()
                if len(debit_no) == 6 and debit_no.isdigit():
                    print("Payment successful. Your order has been placed and will be delivered soon.")
                    break
                else:
                    print("\n\t\t\tInvalid debit card number. The number should be exactly 6 digits.")
                    continue
            else:
                print("Invalid payment method selected.")

        with open(f"{self.username}_info.txt", 'a') as file:
            file.write(f"\nCheckout Details:\n")
            file.write(f"\nCheckout Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("Purchased Items:\n")
            for product_name, details in self.cart.items():
                file.write(f"{product_name}: {details['quantity']} units - Rs{details['price']} each\n")
            file.write(f"Total Bill: Rs{self.total}\n")
            file.write("------------------------------------------------------\n")

        with open(f"{self.username}_checkout.txt", 'a') as file:
            file.write(f"\nCheckout Details:\n")
            file.write(f"\nCheckout Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("Purchased Items:\n")
            for product_name, details in self.cart.items():
                file.write(f"{product_name}: {details['quantity']} units - Rs{details['price']} each\n")
            file.write(f"Total Bill: Rs{self.total}\n")
            file.write("------------------------------------------------------\n")

        self.cart.clear()
        return print("Checkout complete. Your cart is now empty.")


class History:
    def __init__(self, username):
        self.purchase_history = []
        self.username = username
        self.filename = f'{self.username}_info.txt'

    def add_purchase(self, product_name, quantity, price, total_bill):
        with open(self.filename, 'a') as f:
            f.write(
                f'\n\nCart History:\nProduct name: {product_name}, Quantity: {quantity}, Price: {price}, Total Bill: Rs{total_bill}\n')
        self.purchase_history.append({
            'product_name': product_name,
            'quantity': quantity,
            'price': price,
            'total_bill': total_bill
        })


# associated with product manager class

class WishList:
    def __init__(self, product_manager):
        self.wish_list = set()
        self.product_manager = product_manager

    def add_to_wish_list(self):
        print("\nAvailable Products:")
        self.product_manager.display()

        while True:
            try:
                product_number = int(input("Enter the number of the product to add to your wish list: "))
                if product_number in self.product_manager.products:
                    product_name = self.product_manager.products[product_number].name
                    self.wish_list.add(product_name)
                    print(f"Added {product_name} to the wish list.")
                    break
                else:
                    print(f"Product number {product_number} does not exist.")
            except ValueError:
                print("Invalid input. Please enter a valid product number.")

    def remove_from_wish_list(self):
        if not self.wish_list:
            print("Your wish list is empty.")
            return

        print("\nYour Wish List:")
        for index, product_name in enumerate(self.wish_list, start=1):
            print(f"{index}. {product_name}")

        while True:
            try:
                choice = int(input("Enter the number of the product to remove from your wish list: "))
                if 1 <= choice <= len(self.wish_list):
                    product_name = list(self.wish_list)[choice - 1]
                    self.wish_list.remove(product_name)
                    print(f"Removed {product_name} from the wish list.")
                    break
                else:
                    print("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def show_wish_list(self):
        if not self.wish_list:
            print("Your wish list is empty.")
        else:
            print("\nYour Wish List:")
            for product_name in self.wish_list:
                print(product_name)


class Main:
    def __init__(self, filename, username):  # filename = product_list.txt
        self.product_manager = ProductManager(filename)
        self.username = username
        self.cart = Cart(self.username, self.product_manager)
        self.wish_list = WishList(self.product_manager)
        self.history = History(self.username)  # Initialize History instance

    def main_menu(self):
        while True:
            print("\n1. Display Products")
            print("2. Add to Cart")
            print("3. Remove from Cart")
            print("4. Show Cart")
            print("5. Add to Wish List")
            print("6. Remove from Wish List")
            print("7. View Wish List")
            print("8. Checkout")
            print("9. Show Purchase History")
            print("10. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.product_manager.display()
            elif choice == '2':
                self.product_manager.display()
                while True:
                    try:
                        product_number = int(input("Enter the product number to add to cart: "))

                        if product_number in self.product_manager.products:
                            break
                        else:
                            print(f"Product number {product_number} does not exist.")
                    except ValueError:
                        print("\n\t\t\tInvalid input. Please enter a valid number for product number.")
                while True:

                    try:
                        quantity = int(input("Enter the quantity: "))
                        if quantity <= 0:
                            raise ValueError("\n\t\t\tQuantity must be greater than zero.")
                        break
                    except ValueError:
                        print("\n\t\t\tInvalid input. Please enter a valid number for quantity.")

                product = self.product_manager.products[product_number]
                original_price = product.price
                discounted_price = product.get_discounted_price()
                print(f"Original Price: Rs{original_price}, Discounted Price: Rs{discounted_price}")
                self.cart.add_to_cart(product_number, quantity)


            elif choice == '3':
                self.cart.remove_from_cart()
            elif choice == '4':
                self.cart.show_cart()
            elif choice == '5':
                self.wish_list.add_to_wish_list()
            elif choice == '6':
                self.wish_list.remove_from_wish_list()
            elif choice == '7':
                self.wish_list.show_wish_list()
            elif choice == '8':
                self.cart.checkout()
            elif choice == '9':
                print("YOUR PURCHASE HISTORY")
                try:
                    with open(f"{self.username}_checkout.txt", 'r') as file:
                        print(file.read())
                except FileNotFoundError:
                    print(f"Checkout details not found for {self.username}.")
            elif choice == '10':

                break
            else:
                print('\n\t\t\tInvalid choice. Please enter a number between 1 and 9.')


def main():
    while True:
        c = Choice()
        username = c.user_choice()
        if username:
            m = Main('product_list.txt', username)
            m.main_menu()
        continue_choice = input("Do you want to perform another operation? (yes/no): ").strip().lower()
        if continue_choice != 'yes':
            print('\n\t\t\tThank you for shopping with us!')
            break


if __name__ == "__main__":
    main()
