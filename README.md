# Etrian Odyssey 2 Untold Grimoire Editor

## Running
### Windows
Run the `eo2u_grimoire_editor.exe` file from the `dist/` folder. Make sure that the `skill_data/` folder is in the same directory as the executable file, otherwise it will not run.

### Mac/Linux
Requirements:
- Python 3
- Basic command line usage

Download the code from this repository navigate to the directory and using the terminal. From there, run the commands below
```
pip install -r requirements.txt
python eo2u_grimoire_editor.py
```

The first command installs the packages necessary to run the program. The second one runs the program.

## How to Use
TODO: Fill me in

## Build/Debug

Requirements:
- Python 3
- The packages from `requirements.txt`

To run the program locally, please follow the instructions to run on a Mac/Linux computer.

To build the `.exe` file locally, install [pyinstaller](https://pyinstaller.org/en/stable/) and run the following command
```
python -m eel eo2u_grimoire_editor.py web --onefile
```
This will generate an executable file in the `dist/` directory (`eo2u_grimoire_editor.exe`). Make sure that the `skill_data/` folder is in the same directory as the executable file, otherwise it will not run.
