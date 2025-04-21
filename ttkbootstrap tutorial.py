# DOCS:
# https://ttkbootstrap.readthedocs.io/en/latest/gettingstarted/tutorial/

import ttkbootstrap as ttk

# window 
window = ttk.Window(themename = "journal")
window.title("ttk demo")
window.geometry("400x300")

label = ttk.Label(window, text = "Label")
label.pack(pady = 10)

button1 = ttk.Button(window, text = "Red", bootstyle = "danger-outline")
button1.pack(pady = 10)

button2 = ttk.Button(window, text = "Warning", bootstyle = "warning")
button2.pack(pady = 10)

button3 = ttk.Button(window, text = "Green", bootstyle = "success")
button3.pack(pady = 10)

# run
window.mainloop()