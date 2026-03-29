import datetime
import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image
import os
import shutil
import webbrowser
import sys
import json
import subprocess

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"cstrike_folder": ""}

def save_config(path):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"cstrike_folder": path}, f, indent=4)

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

class Logger:
    def __init__(self, log_file="launcher.log"):
        self.log_file = log_file
        self.status_label = None
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(f"--- Starting launcher: {datetime.datetime.now()}\n") 

    def set_display(self, label_widget):
        self.status_label = label_widget

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
        
        print(log_msg)

        if self.status_label:
            self.status_label.configure(text=message)

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
            target_path = os.path.normpath(os.path.join(self.cstrike_folder, "v_knife.mdl"))

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
    def __init__(self, cstrike_folder, logger):
        self.cstrike_folder = cstrike_folder
        self.logger = logger


    def start_game(self):
        if not self.cstrike_folder:
            self.logger.log("Error: cstrike folder not set.")
            return
        
        self.logger.log("Starting Counter-Strike 1.6...")

        if "steamapps" in self.cstrike_folder.lower():
            self.logger.log("Detected Steam installation. Attempting to launch via Steam URL...")
            webbrowser.open("steam://rungameid/10")
        else:
            self.logger.log("Detected Non-Steam installation. Attempting to launch via executable...")
            game_root = os.path.dirname(os.path.dirname(self.cstrike_folder))
            
            executables = ['hl.exe', 'cs.exe']
            found_exe = None

            for exe_name in executables:
                path = os.path.join(game_root, exe_name)
                if os.path.exists(path):
                    found_exe = path
                    break
            
            if found_exe:
                self.logger.log(f"Launching Non-Steam from {found_exe}...")
                subprocess.Popen([found_exe, "-game", "cstrike"], cwd=game_root)
            else:
                self.logger.log(f"Error: Executable ({', '.join(executables)}) not found in {game_root}.")


class LauncherGUI(ctk.CTk):
    def __init__(self, knife_manager, game_launcher, logger):
        super().__init__()

        self.knife_manager = knife_manager
        self.game_launcher = game_launcher
        self.logger = logger

        self.title("Knife Manager")
        self.geometry("640x480")
        ctk.set_default_color_theme("themes/marsh.json")

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

        self.bottom_bar.columnconfigure(0, weight=1)
        self.bottom_bar.columnconfigure(1, weight=1)
        self.bottom_bar.columnconfigure(2, weight=1)

        self.status_display = ctk.CTkLabel(
            self.bottom_bar,
            text="System ready.",
            font=("Arial", 12, "italic"),
            text_color="green",
            wraplength=500
        )
        self.status_display.grid(row=0, column=0, columnspan=3, pady=(10, 5), sticky="ew")
        self.logger.set_display(self.status_display)

        btn_default =ctk.CTkButton(
            self.bottom_bar,
            text="Apply default mdl",
            command=self.knife_manager.apply_default_mdl
        )
        btn_default.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        self.apply_button = ctk.CTkButton(
            self.bottom_bar,
            text="Apply model",
            state="disabled",
            command=self.on_apply_model
        )
        self.apply_button.grid(row=1, column=1, padx=20, pady=10, sticky="")

        btn_start = ctk.CTkButton(
            self.bottom_bar,
            text="Start CS 1.6",
            command=self.game_launcher.start_game
        )
        btn_start.grid(row=1, column=2, padx=20, pady=10, sticky="e")
    
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

def find_cstrike_folder(logger):
    config = load_config()
    if not config["cstrike_folder"] or not os.path.exists(config["cstrike_folder"]):
        chosen_dir = filedialog.askdirectory(title="Select your cstrike/models folder")
        if chosen_dir:
            config["cstrike_folder"] = chosen_dir
            save_config(chosen_dir)
        else:
            logger.log("No cstrike folder selected.")
    cstrike_folder = config["cstrike_folder"]
    return cstrike_folder

if __name__ == "__main__":
    logger = Logger()

    mdl_folder = os.path.join(get_base_dir(), "mdls")
    cstrike_folder = find_cstrike_folder(logger)
    
    knife_manager = KnifeManager(mdl_folder, cstrike_folder, logger)
    game_launcher = GameLauncher(cstrike_folder, logger)

    gui = LauncherGUI(knife_manager, game_launcher, logger)
    gui.run()
