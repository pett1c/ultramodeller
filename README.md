<div align="center">

# 🔪 Ultramodeller – CS 1.6 Knife Model Manager

![ultramodeller_screenshot](https://files.catbox.moe/rlza1t.png)

[![python version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![release](https://img.shields.io/badge/release-v1.0.0-success.svg)](https://github.com/pett1c/ultramodeller/releases)
[![license: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*a simple and quick graphical launcher for managing knife models in counter-strike 1.6.*

</div>

---

## 📖 ・ about the project
**Ultramodeller** is a lightweight application designed to free you from manually copying `.mdl` files once and for all. The program offers a user-friendly visual interface for viewing and installing custom knife skins (it works with both Steam and non-Steam versions of the game).

## 🔑 ・ key features
* **visual gallery:** Preview knives right in the app before installing them.
* **one-click installation:** Forget about searching for the `cstrike/models` folder. The program handles everything automatically.
* **smart launch:** Automatic game version detection (launch via Steam or directly via `hl.exe` or `cs.exe`).
* **safe rollback:** Instantly revert to the classic knife model with the `Apply default mdl` button.
* **built-in logging:** Display operation status directly in the app interface.

---

## 🎮 ・ installation and usage (for players)

1. go to the **[Releases](https://github.com/pett1c/ultramodeller/releases)** page and download the latest version of `ultramodeller_1.X.X_setup.exe`.
2. install the program in a location of your choice.
3. when you first launch the application, it will ask you to specify the path to your `cstrike\models` folder (for example: `C:\Games\Counter-Strike 1.6\cstrike\models` or `...\Steam\steamapps\common\Half-Life\cstrike\models`).
4. select the knife you like from the gallery and click **Apply model**.
5. click **Start CS 1.6** and enjoy the game!

### 🛠️ ・ how to add my own skins?
the program automatically scans the `mdls` folder located in the application's root directory. to add a new knife:
1. create a new folder inside `mdls` (for example, `mdls/my_karambit/`).
2. place the model file there and name it exactly `v_knife.mdl`.
3. place a preview image there as well (in `.png` format).
4. restart the application — the new knife will automatically appear in the grid!

in the future, i plan to implement an editor for easy uploading skins to the app from within the app, support for other image formats, and support for `p_knife.mdl` & `w_knife.mdl` models and sounds.

---

## 💻 ・ installation and usage (for developers)

if you want to modify the program or compile it yourself:

### requirements
* Python 3.10 or later
* Dependencies listed in `requirements.txt`

### local launch
```bash
# Clone a repository
git clone [https://github.com/pett1c/ultramodeller.git](https://github.com/pett1c/ultramodeller.git)
cd YOUR_REPOSITORY

# install dependencies
pip install -r requirements.txt

# launch the app
python main.py
```

### compiling to .exe
**PyInstaller** is used to build the application into a single executable file:
```bash
pyinstaller --noconsole --onefile --collect-all customtkinter main.py

# or

python -m PyInstaller --noconsole --onefile --collect-all customtkinter main.py
```

the finished `.exe` file will appear in the `dist/` folder.
**IMPORTANT!** copy the `mdls/` folder to the `dist/` for the executable to work correctly.

---

## 🛣️ ・ roadmap
* expanding the model collection (a parser using a whitelist of websites may be created for simplicity).
* creating, viewing, editing, and deleting **(CRUD)** folders for knives & the ability to favorite individual models/folders.
* settings, such as configuring the path to models directly within the app `(cstrike_folder, mdl_folder)`, and other settings.
* a full-featured editor for creating, viewing, editing, and deleting **(CRUD)** models directly within the app.

## 📄 ・ license
this project is distributed under the **MIT** License. for details, see the **[LICENSE](https://github.com/pett1c/ultramodeller/blob/main/LICENSE)** file.
