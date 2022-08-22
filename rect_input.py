

import tkinter as tk
import tkinter.messagebox as msgbox
from PIL import ImageGrab, ImageTk



class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.rect_coor = []
        self.label_input_diag = None
        self.labels_list = []
        self.withdraw()
        self.attributes('-fullscreen', True)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both",expand=True)

        image = ImageGrab.grab()
        self.image = ImageTk.PhotoImage(image)
        self.photo = self.canvas.create_image(0,0,image=self.image,anchor="nw")

        self.x, self.y = 0, 0
        self.rect, self.start_x, self.start_y = None, None, None
        self.deiconify()

        self.canvas.tag_bind(self.photo,"<ButtonPress-1>", self.on_button_press)
        self.canvas.tag_bind(self.photo,"<B1-Motion>", self.on_move_press)
        self.canvas.tag_bind(self.photo,"<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        bbox = self.canvas.bbox(self.rect)
        # GET_Rect.rect_list.append(bbox)
        print(bbox)
        self.label_input_diag = LabelInput()
        self.label_input_diag.master.mainloop()
        print("label_input_diag.label = ", self.label_input_diag.label)
        if self.label_input_diag.label is not None:
            self.labels_list.append(self.label_input_diag.label)
            self.rect_coor.append(bbox)
        is_continue = msgbox.askquestion(title="Please confirm", message="Do you want to continue?")
        print(is_continue)
        if is_continue == msgbox.NO:
            self.canvas.destroy()
            self.destroy()

        # self.withdraw()
        # self.new_image = ImageTk.PhotoImage(ImageGrab.grab(bbox))
        # self.attributes('-fullscreen', False)
        # self.title("Image grabbed")
        # if len(GET_Rect.rect_list) >= 3:
            # self.canvas.destroy()
            # self.destroy()
        # self.deiconify()
        # tk.Label(self,image=self.new_image).pack()


class LabelInput():
    def __init__(self):
        # super().__init__()

        self.master = tk.Tk()
        self.label = None
        tk.Label(self.master, 
                text="First Name").grid(row=0)
        # tk.Label(master, 
        #          text="Last Name").grid(row=1)

        self.e1 = tk.Entry(self.master)
        # e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        # e2.grid(row=1, column=1)

        tk.Button(self.master, 
                text='Cancel', 
                command=self.exit_diag).grid(row=3, 
                                            column=0, 
                                            sticky=tk.W, 
                                            pady=4)
        tk.Button(self.master, 
                text='Confirm', command=self.show_entry_fields).grid(row=3, 
                                                            column=1, 
                                                            sticky=tk.W, 
                                                            pady=4)
                                                        
    def exit_diag(self):
        self.master.destroy()
        self.master.quit()
    
    def show_entry_fields(self):
        label_value = self.e1.get().strip()
        print("First Name: %s" % (label_value))
        if label_value != "":
            print("hello")
            self.label = label_value
            self.master.destroy()
            self.master.quit()
            # return label_value

class GETRect:
    def __init__(self) -> None:
        
        self.root = GUI()
        self.rect_list = []

    def start(self):
        self.root.mainloop()
        print("box coordinates: ", self.root.rect_coor)
        print("labels values: ", self.root.labels_list)
        boxes = []
        for label, bound in zip(self.root.labels_list, self.root.rect_coor):
            left, top, right, bottom = bound
            width = right - left
            height = bottom - top
            box = {
                "label": label,
                "bound": [left, top, width, height]
            }
            boxes.append(box)
        return boxes



if __name__ == "__main__":
    dd= GETRect()
    dd.start()
