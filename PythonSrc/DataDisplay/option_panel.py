"""An option panel for Tkinter interface"""

from tkinter import ttk
import os
from PIL import Image, ImageTk


class OptionPanel(ttk.Frame):

    """An option panel for the Tkinter interface for the project"""

    icon_image = None
    visible = True
    combo_mode = None

    def __init__(self,parent):
        super().__init__(parent,padding=10)
        self.setup_layout()
        self.make_icon()
        self.make_mode_label()

    def setup_layout(self):

        """Sets up the layout of this panel"""
        # Options panel style
        option_style = ttk.Style()
        option_style.configure("Option.TFrame",background="darkblue")

        # Configuring settings for layout
        self.configure(style="Option.TFrame")
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.rowconfigure(3,weight=1)
        self.rowconfigure(4,weight=1)
        self.rowconfigure(5,weight=1)

    def make_icon(self) -> None:

        """Make the icon displayed on the options panel"""

        this_dir = os.path.dirname(os.path.abspath(__file__))
        logo_img_loc = os.path.join(this_dir,"../Assets","LinkedInFinal2025.png")
        pil_img = Image.open(logo_img_loc)
        resized_pil = pil_img.resize((100,100),Image.Resampling.LANCZOS)
        self.icon_image = ImageTk.PhotoImage(resized_pil)

        logo_label = ttk.Label(master=self,
                               anchor="w",
                               image=self.icon_image)
        logo_label.grid(row=0,column=0,sticky="nw")

    def make_mode_label(self) -> None:

        """Make the label for the combo box of the time modes"""

        mode_option_label = ttk.Label(master=self,
                                      text="How would you like to view your data?",
                                      anchor="center",wraplength=500)
        mode_option_label.grid(row=1,column=0,sticky="nsew")

    def make_combo_mode_box(self,mode) -> None:

        """
        Make the combo box for the mode to use
        This can be weekly, monthly or yearly
        """

        combo_mode = ttk.Combobox(master=self,textvariable=mode)
        combo_mode.configure(values=("Weekly","Monthly","Yearly"),state="readonly")
        combo_mode.set("Weekly")

        return combo_mode

    def make_retrieve_button(self,command) -> None:

        """Make the button that retrieves the data"""

        retrieve_button = ttk.Button(master=self,text="Go",command=command)
        retrieve_button.grid(row=4,column=0,ipadx=20,ipady=50)

        return retrieve_button
