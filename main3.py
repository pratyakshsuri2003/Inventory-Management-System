import mysql.connector
from sqlalchemy import create_engine
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

root = Tk()
root.title("Inventory Management System")
root.geometry("1080x720")
root.configure(bg='light blue')  
my_tree = ttk.Treeview(root)
storeName = "Inventory Management System"

db = mysql.connector.connect(host='localhost',
                            database='inventory_management_env',
                            username='root',
                            password='@Dslr16expert')

MyCursor = db.cursor()

def reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup

def insert(name, price, quantity):
    MyCursor = db.cursor()
    MyCursor.execute('''CREATE TABLE IF NOT EXISTS 
    inventory( itemId INT AUTO_INCREMENT PRIMARY KEY, itemName VARCHAR(20), itemPrice INT, itemQuantity INT, totalPurchaseAmount INT);''')

    MyCursor.execute("INSERT INTO inventory (itemName, itemPrice, itemQuantity) VALUES (%s, %s, %s)", (name, price, quantity))
    db.commit()

def delete(data):
    MyCursor = db.cursor()
    MyCursor.execute("DELETE FROM inventory WHERE itemId = '" + str(data) + "'")
    db.commit()

def update(name, price, quantity, itemId):
    MyCursor = db.cursor()

    MyCursor.execute('''CREATE TABLE IF NOT EXISTS 
        inventory( itemId INT AUTO_INCREMENT PRIMARY KEY, 
                   itemName VARCHAR(20), 
                   itemPrice INT, 
                   itemQuantity INT, 
                   totalPurchaseAmount INT)''')

    sql = "UPDATE inventory SET itemName = %s, itemPrice = %s, itemQuantity = %s WHERE itemId = %s"
    values = (name, price, quantity, itemId)
    MyCursor.execute(sql, values)
    db.commit()

def read():
    MyCursor = db.cursor()
    MyCursor.execute("SELECT * FROM inventory")
    results = MyCursor.fetchall()
    db.commit()
    return results

def refresh_tree_view():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read()):
        my_tree.insert(parent='', index='end', iid=result[0], text="", values=(result), tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE')
    my_tree.grid(row=1, column=5, columnspan=4, padx=120, pady=20, sticky='ns', rowspan=150)  

def insert_data():
    itemName = str(entryName.get())
    itemPrice = str(entryPrice.get())  
    itemQuantity = str(entryQuantity.get()) 

    # name can contain anything like numbers, characters etc.
    if itemName.strip() == "":
        messagebox.showerror("Input Error", "Please check the field as it can't be empty!")
    elif itemPrice.strip() == "":
        messagebox.showerror("Input Error", "Please check the field as it can't be empty!")
    elif itemQuantity.strip() == "":
        messagebox.showerror("Input Error", "Please check the field as it can't be empty!")
    elif not itemPrice.strip().isdigit():   # for preventing sqli attempts by hackers
        messagebox.showerror("Input Error", "Price must be a number")
    elif not itemQuantity.strip().isdigit(): 
        messagebox.showerror("Input Error", "Quantity must be a number")
    else:
        insert(itemName, int(itemPrice), int(itemQuantity))

    refresh_tree_view()

def delete_data():
    selected_item = my_tree.selection()[0]
    deleteData = str(my_tree.item(selected_item)['values'][0])
    delete(deleteData)

    refresh_tree_view()

def update_data():
    selected_item = my_tree.selection()[0]
    update_item_id = my_tree.item(selected_item)['values'][0]
    update(entryName.get(), entryPrice.get(), entryQuantity.get(), update_item_id)

    refresh_tree()

def refresh_tree():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read()):
        my_tree.insert(parent='', index='end', iid=result[0], text="", values=(result), tag="orow")  

titleLabel = Label(root, text=storeName, font=('Arial bold', 30), bd=2, fg='black')  
titleLabel.grid(row=0, column=1, columnspan=70, padx=50, pady=10)  

nameLabel = Label(root, text="Name", font=('Arial bold', 15))
priceLabel = Label(root, text="Price", font=('Arial bold', 15))
quantityLabel = Label(root, text="Quantity", font=('Arial bold', 15))

nameLabel.grid(row=2, column=0, padx=10, pady=(50,10))
priceLabel.grid(row=3, column=0, padx=10, pady=10)
quantityLabel.grid(row=4, column=0, padx=10, pady=10)

entryName = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryPrice = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryQuantity = Entry(root, width=25, bd=5, font=('Arial bold', 15))

entryName.grid(row=2, column=1, columnspan=3, padx=5, pady=(50,5))
entryPrice.grid(row=3, column=1, columnspan=3, padx=5, pady=5)
entryQuantity.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

buttonEnter = Button(
    root, text="Insert", padx=5, pady=5, width=5,
    bd=3, font=('Arial', 15), bg="white", command=insert_data)  
buttonEnter.grid(row=5, column=1, columnspan=1, pady=10) 

buttonUpdate = Button(
    root, text="Update", padx=5, pady=5, width=5,
    bd=3, font=('Arial', 15), bg="white", command=update_data) 
buttonUpdate.grid(row=5, column=2, columnspan=1, pady=10) 

buttonDelete = Button(
    root, text="Delete", padx=5, pady=5, width=5,
    bd=3, font=('Arial', 15), bg="white", command=delete_data) 
buttonDelete.grid(row=5, column=3, columnspan=1, pady=10)  

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial bold', 15))

my_tree['columns'] = ("ID", "Name", "Price", "Quantity", "Total_Amount")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=50)
my_tree.column("Name", anchor=W, width=350)
my_tree.column("Price", anchor=W, width=100)
my_tree.column("Quantity", anchor=W, width=100)
my_tree.column("Total_Amount", anchor=W, width=150)

my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Price", text="Price", anchor=W)
my_tree.heading("Quantity", text="Quantity", anchor=W)
my_tree.heading("Total_Amount", text="Total Amount", anchor=W)


for data in my_tree.get_children():
    my_tree.delete(data)

for result in reverse(read()):
    my_tree.insert(parent='', index='end', values=(result), tag="orow")

my_tree.tag_configure('orow', background='white', font=('times-new-roman', 12))
my_tree.config(height=25)
my_tree.grid(row=1, column=5, columnspan=4, rowspan=100, padx=120, pady=50, sticky='ns')

root.mainloop()
