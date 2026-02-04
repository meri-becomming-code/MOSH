# Build Guide for MOSH ADA Toolkit

This guide provides step-by-step instructions for setting up your development environment and building the executable on a new Windows computer.

## 1. Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.10+**: Download and install from [python.org](https://www.python.org/downloads/).
    *   **IMPORTANT**: During installation, check the box that says **"Add Python to PATH"**.
2.  **Git** (Optional but recommended): Download from [git-scm.com](https://git-scm.com/downloads) to easily clone the repository.
3.  **Visual Studio Code** (Recommended): A good code editor makes everything easier.

## 2. Setting Up the Environment

1.  **Get the Code**:
    *   If using Git: `git clone https://github.com/meri-becomming-code/mosh.git`
    *   Or download the ZIP from GitHub and extract it to a folder (e.g., `Desktop\mosh`).

2.  **Open the Folder**:
    *   Open a command prompt (cmd) or PowerShell.
    *   Navigate to the folder: `cd Path\To\mosh`

3.  **Create a Virtual Environment** (Recommended):
    *   It keeps your project dependencies separate from your system.
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
    *   *Note: You should see `(venv)` appear at the start of your command line.*

4.  **Install Dependencies**:
    *   Run the following command to install all required libraries:
    ```bash
    pip install -r requirements.txt
    ```
    *   **Install PyInstaller** (Required for building the EXE):
    ```bash
    pip install pyinstaller
    ```

## 3. Building the Executable

There are two ways to build the app. The easiest is using the included batch file.

### Option A: The Easy Way (Batch File)
1.  Double-click `BUILD_WINDOWS.bat` in the project folder.
2.  Wait for the process to finish.
3.  The executable will be in the `dist` folder.

### Option B: The Manual Way (Command Line)
If you need to customize the build or debug errors, run this manually:

1.  Make sure your virtual environment is active (if you used one).
2.  Run the build script:
    ```bash
    python build_app.py
    ```
    *   *Alternatively, you can run PyInstaller directly with the spec file:*
    ```bash
    pyinstaller MOSH_ADA_Toolkit.spec --clean --noconfirm
    ```

## 4. Where is my App?

*   Go to the `dist` folder inside your project directory.
*   You will see `MOSH_ADA_Toolkit.exe`.
*   You can move this file anywhere on your computer (or to a USB drive), and it will run without needing Python installed.

## 5. Troubleshooting (When things go wrong)

**"Python is not recognized as an internal or external command"**
*   You didn't check "Add Python to PATH" during installation. Reinstall Python and make sure to check that box.

**"No module named..." errors**
*   You probably didn't install the dependencies. Run `pip install -r requirements.txt` again.
*   Make sure your virtual environment is activated (`.\venv\Scripts\activate`).

**The EXE opens and instantly closes**
*   This usually means there was an error on startup.
*   Open a command prompt -> drag the EXE into the window -> press Enter.
*   This will run it from the console so you can see the error message.

**"Failed to execute script..."**
*   This is a generic PyInstaller error. Try deleting the `build` and `dist` folders and building again with `--clean`.
*   Ensure `Pillow` is installed: `pip install Pillow`
