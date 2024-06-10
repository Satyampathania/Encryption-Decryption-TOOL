import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key


def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, 'rb') as key_file:
        return key_file.read()


# Load or generate the key for encryption and decryption
key = load_key()
cipher_suite = Fernet(key)


def encrypt_text(plain_text):
    encrypted_text = cipher_suite.encrypt(plain_text.encode())
    return encrypted_text.decode()


def decrypt_text(encrypted_text):
    try:
        decrypted_text = cipher_suite.decrypt(encrypted_text.encode())
        return decrypted_text.decode()
    except Exception as e:
        return f"Decryption failed: {str(e)}"


def show_text_in_window(title, text):
    text_window = tk.Toplevel()
    text_window.title(title)

    text_box = tk.Text(text_window, wrap='word', width=60, height=10)
    text_box.pack(padx=10, pady=10)
    text_box.insert('1.0', text)
    text_box.config(state='disabled')

    copy_button = tk.Button(text_window, text="Copy to Clipboard", command=lambda: copy_to_clipboard(text))
    copy_button.pack(pady=5)


def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Copied", "Text has been copied to clipboard")


def main():
    global root
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    action = simpledialog.askstring("Input",
                                    "Do you want to encrypt or decrypt the text? (enter 'encrypt' or 'decrypt')")

    if action:
        if action.lower() == 'encrypt':
            plain_text = simpledialog.askstring("Input", "Enter the text to encrypt:")
            if plain_text:
                encrypted_text = encrypt_text(plain_text)
                show_text_in_window("Encrypted Text", encrypted_text)

        elif action.lower() == 'decrypt':
            encrypted_text = simpledialog.askstring("Input", "Enter the text to decrypt:")
            if encrypted_text:
                decrypted_text = decrypt_text(encrypted_text)
                show_text_in_window("Decrypted Text", decrypted_text)
        else:
            messagebox.showerror("Error", "Invalid action. Please enter 'encrypt' or 'decrypt'.")
    else:
        messagebox.showerror("Error", "No action specified. Please enter 'encrypt' or 'decrypt'.")


if __name__ == "__main__":
    main()
    root.mainloop()  # Start the main event loop
