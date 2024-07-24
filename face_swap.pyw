import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import glob
import cv2
import insightface
from insightface.app import FaceAnalysis

PARAMS = {
    "bg": "#587B7F",
    "fg": "#ffffff",
    "font": "-family {Arial Rounded MT Bold} -size 24",
    "highlightbackground": "#d9d9d9",
    "highlightcolor": "black",
}
HIGHLIGHTS = {
    "highlightbackground": "#d9d9d9",
    "highlightcolor": "black",
}

# Store the paths for images and folders
class PathMemory:
    def __init__(self):
        self.first_image = None
        self.source_images = None
        self.destination_folder = None

path_memory = PathMemory()

class Menu:
    def __init__(self, top=None):
        top.geometry("380x400+750+184")
        top.minsize(380, 400)
        top.maxsize(400, 400)
        top.title("Face Swapping")
        top.configure(background="#587B7F")
        top.configure(**HIGHLIGHTS)

        self.top = top
        
        self.Label1 = tk.Label(self.top)
        self.Label1.configure(**PARAMS)
        self.Label1.place(relx=0.274, rely=0.085, height=41, width=314)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(anchor='w')
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(text='''Face-Swap''')
        
        button_y_positions = [0.31, 0.46, 0.62, 0.78]  # Increased space between buttons

        self.Button1 = tk.Button(self.top)
        self.Button1.configure(**HIGHLIGHTS)
        self.Button1.place(relx=0.5, rely=button_y_positions[0], height=44, width=256, anchor='center')  # Adjusted position and width
        self.Button1.configure(activebackground="#7b7979")
        self.Button1.configure(activeforeground="black")
        self.Button1.configure(background="#B36C24")
        self.Button1.configure(command=self.select_first_image)
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font="-family {Arial Rounded MT Bold} -size 14")
        self.Button1.configure(foreground="#ffffff")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Select Default Image''')

        self.Button2 = tk.Button(self.top)
        self.Button2.configure(**HIGHLIGHTS)
        self.Button2.place(relx=0.5, rely=button_y_positions[1], height=44, width=256, anchor='center')  # Adjusted position and width
        self.Button2.configure(activebackground="#7b7979")
        self.Button2.configure(activeforeground="black")
        self.Button2.configure(background="#B36C24")
        self.Button2.configure(command=self.select_source_images)
        self.Button2.configure(compound='left')
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font="-family {Arial Rounded MT Bold} -size 14")
        self.Button2.configure(foreground="#ffffff")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Select Source Images''')

        self.Button3 = tk.Button(self.top)
        self.Button3.configure(**HIGHLIGHTS)
        self.Button3.place(relx=0.5, rely=button_y_positions[2], height=44, width=256, anchor='center')  # Adjusted position and width
        self.Button3.configure(activebackground="#7b7979")
        self.Button3.configure(activeforeground="black")
        self.Button3.configure(background="#A7631E")
        self.Button3.configure(command=self.select_destination_folder)
        self.Button3.configure(compound='left')
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(font="-family {Arial Rounded MT Bold} -size 14")
        self.Button3.configure(foreground="#ffffff")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='''Select Destination Path''')

        self.Button4 = tk.Button(self.top)
        self.Button4.configure(**HIGHLIGHTS)
        self.Button4.place(relx=0.5, rely=button_y_positions[3], height=44, width=256, anchor='center')  # Adjusted position and width
        self.Button4.configure(activebackground="#7b7979")
        self.Button4.configure(activeforeground="black")
        self.Button4.configure(background="#A7631E", state=tk.DISABLED, fg='gray')  # Set initial state to disabled and gray
        self.Button4.configure(command=self.all_swap)
        self.Button4.configure(compound='left')
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(font="-family {Arial Rounded MT Bold} -size 14")
        self.Button4.configure(foreground="#ffffff")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(text='''All Swap''')

    def check_all_set(self):
        if path_memory.first_image and path_memory.source_images and path_memory.destination_folder:
            self.Button4.configure(state=tk.NORMAL, background="#1E90FF", foreground="#ffffff")  # Enable and set to blue
        else:
            self.Button4.configure(state=tk.DISABLED, background="#A7631E", foreground="gray")  # Keep disabled and gray

    def select_first_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")])
        if file_path:
            path_memory.first_image = file_path
            messagebox.showinfo("Information", f"Default image selected: {file_path}")
        self.check_all_set()

    def select_source_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")])
        if file_paths:
            path_memory.source_images = file_paths
            messagebox.showinfo("Information", f"Source images selected: {len(file_paths)} images")
        self.check_all_set()

    def select_destination_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            path_memory.destination_folder = folder_path
            messagebox.showinfo("Information", f"Destination folder selected: {folder_path}")
        self.check_all_set()

    def all_swap(self):
        if not path_memory.first_image or not path_memory.source_images or not path_memory.destination_folder:
            messagebox.showwarning("Warning", "Please select all paths before proceeding.")
            return

        app = FaceAnalysis(name='buffalo_l')
        app.prepare(ctx_id=0, det_size=(640, 640))
        swapper = insightface.model_zoo.get_model('neurons_weigths/inswapper_128.onnx', download=False, download_zip=False)

        img1 = cv2.imread(path_memory.first_image)
        face1 = app.get(img1)[0]

        for i, img2_fn in enumerate(path_memory.source_images):
            img2 = cv2.imread(img2_fn)
            faces = app.get(img2)
            img2_ = img2.copy()

            for face in faces:
                img2_ = swapper.get(img2_, face, face1, paste_back=True)

            save_path = os.path.join(path_memory.destination_folder, f"{i+1:04d}.png")
            cv2.imwrite(save_path, img2_)

        messagebox.showinfo("Information", "All images have been processed and saved.")

if __name__ == '__main__':
    root = tk.Tk()
    app = Menu(root)
    root.mainloop()
