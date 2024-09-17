import json
from pynput import keyboard
import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Button, Entry, Label

def on_enter(e):
    e.widget['background'] = '#9F5A37'  

def on_leave(e):
    e.widget['background'] = '#7F4E2F' 

def load_macros_from_file():
    try:
        with open('macros.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    
def save_macros(macros):
    with open('macros.json', 'w') as file:
        json.dump(macros, file, indent=4)

def add_macro():
    add_window = Toplevel(root)
    add_window.title("Adicionar macro")
    add_window.configure(bg='#2B1B17')  
    Label(add_window, text="Título da Macro:", bg='#2B1B17', fg='#F5DEB3', font=('Courier New', 12, 'bold')).pack(pady=5)
    title_entry = Entry(add_window, width=50, bg='#7F4E2F', fg='#F5DEB3', font=('Courier New', 12, 'bold'))
    title_entry.pack(pady=5)
    
    Label(add_window, text="Texto da macro:", bg='#2B1B17', fg='#F5DEB3', font=('Courier New', 12, 'bold')).pack(pady=5)
    text_entry = Text(add_window, wrap=tk.WORD, width=50, height=10, bg='#2B1B17', fg='#F5DEB3', font=('Segoe UI', 12, 'bold'), insertbackground='#F5DEB3')
    text_entry.pack(pady=5)

    def save_new_macro():
        key = title_entry.get().strip()
        value = text_entry.get(1.0, tk.END).strip()
        if key and value:
            macros[key] = value
            save_macros(macros)
            update_listbox()
            add_window.destroy()
        else:
            messagebox.showerror("Erro", "Nenhum dos dois campos pode estar vazio")

    save_button = Button(add_window, text="Salvar", command=save_new_macro, bg='#7F4E2F', fg='#F5DEB3', font=('Segoe UI', 12, 'bold'))
    save_button.pack(pady=5)
    save_button.bind("<Enter>", on_enter)
    save_button.bind("<Leave>", on_leave)

def edit_macro():
    key = listbox.get(tk.ACTIVE)
    if key:
        edit_window = Toplevel(root)
        edit_window.title(f"Editando a macro {key}")
        edit_window.configure(bg='#2B1B17')  

        edit_text = Text(edit_window, wrap=tk.WORD, width=50, height=15, bg='#2B1B17', fg='#F5DEB3', font=('Courier New', 12, 'bold'), insertbackground='#F5DEB3')
        edit_text.pack(fill=tk.BOTH, expand=True)
        edit_text.insert(tk.END, macros[key])

        def save_edit():
            macros[key] = edit_text.get(1.0, tk.END).strip()
            save_macros(macros)
            update_listbox()
            edit_window.destroy()
        
        save_button = Button(edit_window, text="Salvar", command=save_edit, bg='#7F4E2F', fg='#F5DEB3', font=('Courier New', 12, 'bold'))
        save_button.pack(pady=5)
        save_button.bind("<Enter>", on_enter)
        save_button.bind("<Leave>", on_leave)

def delete_macro():
    key = listbox.get(tk.ACTIVE)
    if key:
        confirm = messagebox.askyesno("Confimando: ", "Tem certeza que deseja deletar a macro?")
        if confirm:
            del macros[key]
            save_macros(macros)
            update_listbox()

def update_listbox():
    listbox.delete(0, tk.END)
    for key in macros:
        listbox.insert(tk.END, key)

def show_macro_content(event):
    selected_macro = listbox.get(tk.ACTIVE)
    if selected_macro:
        text_display.delete(1.0, tk.END)
        text_display.insert(tk.END, macros[selected_macro])

def handle_shift_enter(event):
    text_display.insert(tk.INSERT, "\n")
    return "break"

with open('macros.json', 'r') as file:
    macros = json.load(file)

current_input = ''
typing_delay = 0

def on_press(key):
    global current_input
    try:
        if hasattr(key, 'char') and key.char is not None: 
            current_input += key.char
        elif key == keyboard.Key.space:
            current_input += ' '
        elif key == keyboard.Key.backspace:
            current_input = current_input[:-1]
        elif key == keyboard.Key.enter:
            current_input = ''

        if '#' in current_input:
            for macro in macros:
                if f'#{macro}' in current_input:
                    replace_text(macros[macro])
                    current_input = ''

    except AttributeError:
        pass  

def replace_text(text):
    controller = keyboard.Controller()

    # Apaga o texto atual
    for _ in range(len(current_input)):
        controller.press(keyboard.Key.backspace)
        controller.release(keyboard.Key.backspace)

    # Insere o novo texto
    for c in text:
        if c == '\n':
            # Simula Shift + Enter
            controller.press(keyboard.Key.shift)
            controller.press(keyboard.Key.enter)
            controller.release(keyboard.Key.enter)
            controller.release(keyboard.Key.shift)
        else:
            controller.press(c)
            controller.release(c)


root = tk.Tk()
root.title("Gerenciador de Macros")
root.configure(bg='#2B1B17')  
macros = load_macros_from_file()
listbox = tk.Listbox(root, bg='#2B1B17', fg='#F5DEB3', font=('Courier New', 12, 'bold'), selectbackground='#7F4E2F', selectforeground='#F5DEB3')
listbox.pack(fill=tk.BOTH, expand=True) 
listbox.bind("<<ListboxSelect>>", show_macro_content)

text_display = tk.Text(root, height=10, wrap=tk.WORD, bg='#2B1B17', fg='#F5DEB3', font=('Courier New', 12, 'bold'), insertbackground='#F5DEB3')
text_display.pack(fill=tk.BOTH, expand=True)

text_display.bind("<Shift-Return>", handle_shift_enter)

btn_add = tk.Button(root, text="Adicionar Macro", command=add_macro, bg='#7F4E2F', fg='#F5DEB3', font=('Courier New', 12, 'bold'))
btn_add.pack(fill=tk.X)
btn_add.bind("<Enter>", on_enter)
btn_add.bind("<Leave>", on_leave)

btn_edit = tk.Button(root, text="Editar Macro", command=edit_macro, bg='#7F4E2F', fg='#F5DEB3', font=('Courier New', 12, 'bold'))
btn_edit.pack(fill=tk.X)
btn_edit.bind("<Enter>", on_enter)
btn_edit.bind("<Leave>", on_leave)

btn_delete = tk.Button(root, text="Deletar Macro", command=delete_macro, bg='#7F4E2F', fg='#F5DEB3', font=('Courier New', 12, 'bold'))
btn_delete.pack(fill=tk.X)
btn_delete.bind("<Enter>", on_enter)
btn_delete.bind("<Leave>", on_leave)

footer = Label(root, text="por Mariana P. (ou Esmeralda)", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg='#2B1B17', fg='#F5DEB3', font=('Courier New', 12, 'bold'))
footer.pack(side="bottom", fill=tk.X)

update_listbox()

listener = keyboard.Listener(on_press=on_press)
listener.start()

root.mainloop()

listener.stop()
