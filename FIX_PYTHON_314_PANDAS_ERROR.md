# Fix — Python 3.14 Ke Sath pandas Install Error

## Wajah
`pandas==2.2.3` (jo requirements.txt mein hai) Python 3.14 ke liye
precompiled file (wheel) nahi rakhti, is liye pip source se build karne ki
koshish karta hai aur Visual Studio Build Tools na hone ki wajah se fail
ho jata hai.

**Fix:** Python 3.12 install karke usi se project ki `.venv` banayein.
Python 3.14 uninstall karne ki zaroorat nahi — dono ek saath reh sakte
hain, hum sirf project ke liye 3.12 use karenge.

---

## Step 1 — Python 3.12 Install Karein

1. [python.org/downloads/release/python-31210](https://www.python.org/downloads/release/python-31210/)
   par jaayein (ya python.org par "Downloads" → "Windows" → 3.12.x wala
   version dhoondh lein).
2. Neeche scroll karke **"Windows installer (64-bit)"** download karein.
3. Installer chalayein:
   - Neeche **"Add python.exe to PATH"** checkbox tick karein.
   - **"Install Now"** dabayein.

---

## Step 2 — Purani `.venv` Folder Delete Karein

Command Prompt mein project folder ke andar (yaani jahan `.venv` bani
thi):

1. Pehle virtual environment se bahar niklein:
   ```
   deactivate
   ```
2. Purani `.venv` folder delete karein — File Explorer mein project
   folder kholein, `.venv` folder par right-click → **Delete**.

---

## Step 3 — Python 3.12 Se Nayi `.venv` Banayein

Windows mein jab multiple Python versions installed hon, to **`py`
launcher** se specific version choose ki ja sakti hai. Command Prompt
mein (project folder ke andar):

```
py -3.12 -m venv .venv
```

Yeh confirm karta hai ke `.venv` khaas Python 3.12 se bane, 3.14 se nahi.

Agar yeh error de `Python 3.12 not found`, to check karein kaunse versions
installed hain:
```
py --list
```
Isse ek list milegi (jaisay `-V:3.12`, `-V:3.14`) — usi ke mutabiq command
adjust kar lein.

---

## Step 4 — Activate Karein Aur Confirm Karein

```
.venv\Scripts\activate
python --version
```

Ab yeh dikhna chahiye: `Python 3.12.x` (3.14 nahi).

---

## Step 5 — Dobara Install Karein

```
pip install -r requirements.txt
```

Ab `pandas` bina kisi masle ke install ho jani chahiye, kyunke 3.12 ke
liye precompiled wheel available hai.

---

## Agar Phir Bhi Masla Aaye

Agar `py -3.12` command hi na chale (matlab installer ne `py` launcher
theek se register nahi kiya), to seedha 3.12 ka full path use karein.
Normally yeh hota hai:
```
C:\Users\Time is MONEY\AppData\Local\Programs\Python\Python312\python.exe -m venv .venv
```
(Exact path installer ke location par depend karta hai — File Explorer
mein `AppData\Local\Programs\Python\` folder check kar ke confirm kar
sakte hain.)
