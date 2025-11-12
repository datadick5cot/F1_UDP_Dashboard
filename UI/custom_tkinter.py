import customtkinter
from PIL import Image
import os

def button_callback():
    print("button pressed")


customtkinter.set_appearance_mode("Dark")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("DDD")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        #Open Full Screen Mode
        self.attributes("-fullscreen", "True")
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.logo_image = customtkinter.CTkImage(Image.open(current_path + "/DDD_Splash.png"), size=(screen_width, screen_height))
        
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.logo_image, text="")
        self.bg_image_label.grid(row=0, column=0)

if __name__ == "__main__":
    app = App()
    app.mainloop()