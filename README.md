# 🚄 IRCTC-QuickBook

Ultra-fast, GUI-driven automation tool for booking Indian Railways tickets via IRCTC. Designed for speed, modularity, and headless benchmarking.

---

## ⚡ Features

- 🖥️ GUI-based booking with CustomTkinter
- 🧠 Intelligent autofill from config
- 🏃 Headless mode (`--no-gui`) for automation and testing

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/krishvadas/IRCTC-QuickBook.git
cd IRCTC-QuickBook
```
Run ```start.bat``` if you're on windows, ```start.sh``` if you're on linux

#### Jump to Step 4

OR
### 2. Manually create and activate virtual environment
If you're on windows
```bash
python -m venv .venv
.venv/scripts/activate
```
If you're on linux
```bash 
python3 -m venv .venv
source venv/bin/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure your booking details
Copy the template and fill in your credentials:

```bash
cp config.template.json config.json
```
Edit config.json with your IRCTC login, passenger info, and travel details if you are not using GUI.

## 🚀 Run the App
### GUI Mode
```bash
python main.py
```
### No GUI
``` bash
python main.py --no-gui
```
## 📜 License
MIT License © 2025 Krishvadas

# 🤝 Contributions
Pull requests welcome! For major changes, open an issue first to discuss what you’d like to improve.


---