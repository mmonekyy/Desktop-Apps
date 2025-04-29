import importlib.util
import customtkinter as ctk
from PIL import Image
import os

# Initialize the main application window
app = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme('green')
app.geometry('900x500')
#app.minsize(900,500)
#app.maxsize(900,500)
app.iconbitmap('img/czaszka.ico')
app.title('Menu')

# Configure grid layout
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=20)
app.grid_rowconfigure(0, weight=1)

# Create two frames for the layout
frame_left = ctk.CTkFrame(app)
frame_right = ctk.CTkFrame(app)
frame_right.grid_propagate(False)

# Grid the frames
frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
frame_left.grid_columnconfigure(0, weight=1)
frame_left.grid_rowconfigure(0, weight=1)
frame_left.grid_rowconfigure(1, weight=5)

image_path = 'img/Czaszka.png'
image = Image.open(image_path)
photo = ctk.CTkImage(light_image=image, dark_image=image, size=(150, 150))

label = ctk.CTkLabel(frame_left, image=photo,text='')
label.grid(row=0, column=0, sticky="nsew")

frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

def load_modules(folder):
    modules = {}
    for filename in os.listdir(folder):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            module_path = os.path.join(folder,filename)
            try:
                spec = importlib.util.spec_from_file_location(module_name,module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "main"):
                    modules[module_name] = module.main
            except Exception as e:
                print(f"Nie udało się załadować modułu {module_name}: {e}")
    return modules

modules = load_modules('modules')

print(modules)

scrolbar_left = ctk.CTkScrollableFrame(frame_left,corner_radius=0)
scrolbar_left.grid(row=1, column=0, sticky="nsew")

scrolbar_left.grid_rowconfigure(0, weight=1)
scrolbar_left.grid_columnconfigure(0, weight=1)

def cwelnia(value):
    print(f"Kliknięto przycisk z wartością: {value}")
    if value in modules:
        modules[value](frame_right)

for i, module_name in enumerate(modules.keys()):
    button = ctk.CTkButton(scrolbar_left,text=f"{module_name}",command=lambda value=module_name: cwelnia(value))
    button.grid(row=i, column=0, sticky="nsew",pady=5)

# Run the app
app.mainloop()
