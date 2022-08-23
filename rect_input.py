

import tkinter as tk
import tkinter.messagebox as msgbox
from typing import ItemsView, List
from PIL import ImageGrab, ImageTk



class GUI(tk.Tk):
    def __init__(self, ticker_list):
        super().__init__()
        self.ticker_list = ticker_list
        self.rect_coor = None
        self.label_input_diag = None
        self.selected_label = None
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
        self.label_input_diag = LabelInput(self.ticker_list)
        self.label_input_diag.master.mainloop()
        if self.label_input_diag.label is not None:
            self.selected_label = self.label_input_diag.label
            self.rect_coor = bbox
            is_yes = msgbox.askyesnocancel(title="Please confirm", message="Are you sure about this ticker?")
            if is_yes:

                self.canvas.destroy()
                self.destroy()
            elif is_yes is None:
                self.selected_label = None
                self.rect_coor = None
                self.canvas.destroy()
                self.destroy()
            else:
                pass
        else:
            retry = msgbox.askretrycancel(title="Retry?", message="Do you want to Retry?")
            if retry:
                pass
            else:
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
    def __init__(self, tickernames:List):
        # super().__init__()

        self.master = tk.Tk()
        self.master.title("Please select ticker name.")
        self.label = None
        tk.Label(self.master, 
                text="Ticker Name: ").grid(row=0)
        # tk.Label(master, 
        #          text="Last Name").grid(row=1)

        # items_var = tk.StringVar(items)
        # items = ["AAPL", "MSFT", "NQ"]
        self.variable = tk.StringVar(self.master)
        self.variable.set(tickernames[0])
        self.e1 = tk.OptionMenu(self.master, self.variable, *tickernames)
        self.e1.grid(row=0, column=1)
        # self.e1.pack()
        # items = ["AAPL", "MSFT", "NQ"]
        # for i, item in enumerate(items):
        #     self.e1.insert(i, item)
        # e2 = tk.Entry(master)

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
        label_value = self.variable.get().strip()
        if label_value != "":
            self.label = label_value
            self.master.destroy()
            self.master.quit()
            # return label_value

class GETRect:
    def __init__(self, ticker_list) -> None:
        
        self.root = GUI(ticker_list)
        self.rect_list = []

    def start(self):
        self.root.mainloop()
        if self.root.rect_coor is None or self.root.selected_label is None:
            return None
        # for label, bound in zip(self.root.selected_label, selected_label):
        left, top, right, bottom = self.root.rect_coor
        width = right - left
        height = bottom - top
        box = {
            "label": self.root.selected_label,
            "bound": [left, top, width, height]
        }
        # boxes.append(box)
        return box


if __name__ == "__main__":
    ticker_list = ["AAPL", "MSFT", "NQ"]
    dd= GETRect(ticker_list)
    dd.start()
