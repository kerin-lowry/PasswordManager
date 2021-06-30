from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    rand_letters = [random.choice(letters) for letter in range(nr_letters)]
    rand_symbols = [random.choice(symbols) for symbol in range(nr_symbols)]
    rand_numbers = [random.choice(numbers) for number in range(nr_numbers)]
    
    password_list = rand_letters + rand_symbols + rand_numbers
    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
        "email": email,
        "password": password,
        }
    }
    
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")

    else:
        try:
            with open("my_data.json", "r") as file:
                #read old data
                data = json.load(file)
        except FileNotFoundError:
            with open("my_data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            #update old data
            data.update(new_data)
            with open("my_data.json", "w") as file:
                #save updated data
                json.dump(data, file, indent=4)
            messagebox.showinfo(title="Success", message="Your details were successfully saved")
        finally:
            website_entry.delete(0, "end")    
            password_entry.delete(0, "end")
            website_entry.focus()
# ---------------------------- SEARCH FUNCTION ------------------------------- #
def find_password():
    user_entry = website_entry.get().title()
    try:
        with open("my_data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if user_entry in data:
            email = data[user_entry]["email"]
            password = data[user_entry]["password"]
            messagebox.showinfo(title=user_entry, message=f"Email: {email}\n Password: {password}")
            website_entry.delete(0, "end")
        else:
            messagebox.showinfo(title="Error", message=f"No details for the website '{user_entry}' exists")
            website_entry.delete(0, "end")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=30, pady=20)

#create lock logo canvas
canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100,100, image=lock_img)
canvas.grid(column=1, row=0)

#labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

#entries
website_entry = Entry(width=33)
website_entry.grid(column=1, row=1, columnspan=1)
website_entry.focus()

email_entry = Entry(width=52)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(END, "kerin.lowry@yahoo.com")

password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

#buttons
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=1)


window.mainloop()