import datetime
import customtkinter as ctk
from PIL import Image
import os
import shutil
import webbrowser

class Logger:
    def __init__(self, log_file="launcher.log"):
        self.log_file = log_file
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(f"--- Starting launcher: {datetime.datetime.now()}\n")  

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")

class KnifeManager:
    def __init__(self, mdl_folder, cstrike_folder, logger):
        self.mdl_folder = mdl_folder
        self.cstrike_folder = cstrike_folder
        self.logger = logger
        self.available_knives = []
    
    def scan_mdls(self):
        self.logger.log(f"Scanning for knife models in {self.mdl_folder}...")
        for folder_name in os.listdir(self.mdl_folder):
            if folder_name != "!default":
                folder_path = os.path.join(self.mdl_folder, folder_name)
                if os.path.isdir(folder_path):
                    knife_data = {
                        "name": folder_name,
                        "imgpath": None,
                        "mdlpath": None
                    }
                for file in os.listdir(folder_path):
                    if file.endswith(".mdl"):
                        knife_data["mdlpath"] = os.path.join(folder_path, file)
                    elif file.endswith(".png"):
                        knife_data["imgpath"] = os.path.join(folder_path, file)

                self.available_knives.append(knife_data)

        self.logger.log(f"Found {len(self.available_knives)} knife models.")
        return self.available_knives
    
    def apply_mdl(self, mdlpath):
        if mdlpath:
            target_path = os.path.join(self.cstrike_folder, "v_knife.mdl")

            try:
                shutil.copy2(mdlpath, target_path)
                self.logger.log(f"Successfully applied {mdlpath} to {target_path}")
            except Exception as e:
                self.logger.log(f"Error applying model: {e}")
        
        else:
            self.logger.log("No model path provided.")
    
    def apply_default_mdl(self):
        default_mdl_path = os.path.join(self.mdl_folder, "!default", "v_knife.mdl")
        self.apply_mdl(default_mdl_path)
    
class GameLauncher:
    def start_game(self):
        print("Starting game...")
        webbrowser.open("steam://rungameid/10")

class LauncherGUI(ctk.CTk):
    def __init__(self, knife_manager, game_launcher, logger):
        super().__init__()

        self.knife_manager = knife_manager
        self.game_launcher = game_launcher
        self.logger = logger

        self.title("Knife Manager")
        self.geometry("640x480")
        ctk.set_default_color_theme("dark-blue")

        self.current_view = "grid"
        self.selected_knife = None
        self.images = []

        self.knives_grid = None
        self.single_view = None

        self.initialize_app()
    
    def initialize_app(self):
        self.knife_manager.scan_mdls()
        
        for item in self.knife_manager.available_knives:
            if item["imgpath"]:
                pil_img = Image.open(item["imgpath"])
                ctk_img = ctk.CTkImage(light_image=pil_img, size=(150, 150))
                self.images.append(ctk_img)
            else:
                self.images.append(None)

        self.build_bottom_bar()
        self.build_grid_view()
    
    # Drawing functions

    def build_bottom_bar(self):
        self.bottom_bar = ctk.CTkFrame(self, height=50, corner_radius=5)
        self.bottom_bar.pack(side="bottom", fill="x", padx=10, pady=10)

        ctk.CTkButton(self.bottom_bar, text="Apply default mdl", command=self.knife_manager.apply_default_mdl).pack(side="left", padx=10, pady=10)
        
        self.apply_button = ctk.CTkButton(self.bottom_bar, text="Apply model", state="disabled", command=self.on_apply_model)
        self.apply_button.pack(padx=10, pady=10)

        ctk.CTkButton(self.bottom_bar, text="Start CS 1.6", command=self.game_launcher.start_game).pack(side="right", padx=10, pady=10)
    
    def build_grid_view(self):
        self.knives_grid = ctk.CTkScrollableFrame(self, corner_radius=5)
        self.knives_grid.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 0))

        columns = 3
        for i in range(columns):
            self.knives_grid.columnconfigure(i, weight=1)
        
        for index, knifedata in enumerate(self.knife_manager.available_knives):
            row = index // columns
            col = index % columns

            button = ctk.CTkButton(
                master=self.knives_grid,
                image=self.images[index],
                text=knifedata["name"],
                compound="top",
                command=lambda k=knifedata, idx=index: self.on_knife_click(k, idx)
            )
            button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    
    def build_single_view(self, knifedata, index):
        self.single_view = ctk.CTkFrame(self, corner_radius=5)
        self.single_view.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 0))

        pil_img = Image.open(knifedata["imgpath"])
        big_img = ctk.CTkImage(light_image=pil_img, size=(300, 300))

        button = ctk.CTkButton(
                master=self.single_view,
                image=big_img,
                text=knifedata["name"],
                compound="top",
                command=self.on_image_click_return
            )
        button.pack(padx=10, pady=10)
    
    # Event handlers
    
    def on_knife_click(self, knifedata, index):
        self.selected_knife = knifedata
        self.knives_grid.pack_forget()
        self.build_single_view(knifedata, index)
        self.apply_button.configure(state="normal")
    
    def on_image_click_return(self):
        self.single_view.destroy()
        self.knives_grid.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 0))
        self.apply_button.configure(state="disabled")

    def reset_apply_button(self):
        self.apply_button.configure(text="Apply model", state="normal")
    
    def on_apply_model(self):
        self.knife_manager.apply_mdl(self.selected_knife["mdlpath"])
        self.apply_button.configure(text="Model Applied", state="disabled")
        self.after(2000, self.reset_apply_button)
    
    def run(self):
        self.mainloop()

if __name__ == "__main__":
    mdl_folder = r"D:\Other\proj\ultramodeller\mdls"
    cstrike_folder = r"D:\Games\Steam\steamapps\common\Half-Life\cstrike\models"

    logger = Logger()
    knife_manager = KnifeManager(mdl_folder, cstrike_folder, logger)
    game_launcher = GameLauncher()

    gui = LauncherGUI(knife_manager, game_launcher, logger)
    gui.run()
