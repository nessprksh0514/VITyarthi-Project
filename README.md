# Medicine Reminder and Interaction Safety Checker

Hey there! Welcome to my repository. This is my submission for the VITyarthi "Build Your Own Project" flipped course evaluation.

I built a Python-based console application to solve a pretty common problem: forgetting to take medications on time, and the dangers of accidentally scheduling conflicting medicines too close together. 

Since I wanted to keep things lightweight, privacy-friendly, and easy to run without any complex database setups, this entire app runs directly in the terminal and stores everything in memory during your session. 

**Author:** Ness Pankaj Prakash (26BAI10024)

---

## What does it do?

I split the functionality into three main modules:
1. **Medicine Records:** You can add medicines with specific details (dosage, schedule times, duration, food instructions). You can also search your scheduled medicines—I added a fuzzy search feature, so even if you make a typo, it'll usually figure out what you meant.
2. **Reminders & Missed Doses:** It scans your schedule and the current time to tell you what doses you have coming up in the next 24 hours, and yells at you (nicely) if you missed a scheduled dose. 
3. **Safety & Overlap Checks:** This is the cool part. If you schedule two pills within 30 minutes of each other, the app flags an overlap warning. You can also add custom interaction notes (e.g., "Drug A and Drug B cause nausea together"), and it will actively warn you if both are scheduled on the same day.

## Technologies Used
- **Language:** Python 3
- **Libraries:** Just the Python Standard Library (`datetime`, `dataclasses`, `difflib`). No external dependencies or `pip install`s needed!

## How to Install and Run

1. Clone this repository to your local machine.
2. Make sure you have Python 3 installed.
3. Run the entry script from the root folder:
   ```bash
   python main.py
   ```
