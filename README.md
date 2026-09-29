# Medicine Reminder and Interaction Safety Checker

Welcome to my repository. This is my original project submission for the VITyarthi "Build Your Own Project" flipped course evaluation.

I have built a Python-based console application to solve a common healthcare challenge: forgetting to take medications on time and preventing the dangers of accidentally scheduling conflicting medicines too close together.

Since this app emphasizes local data control, privacy, and lightweight operations, it runs completely in the terminal environment and safely stores data in memory during your active session.

**Author:** Ness Pankaj Prakash (26BAI10024)

---

## Project Overview
This project provides a robust, command-line medicine scheduler that tracks drug safety parameters, manages temporal notifications, and evaluates dynamic interactions in real-time.

## Features & Functional Modules
Per the course criteria, the application is divided into three distinct functional modules:
*   **Medicine Records Module:** Allows users to input new medications with dosages, durations, and temporal schedules. Includes a custom fuzzy search mechanism to handle spelling errors gracefully.
*   **Reminders & Missed Doses Module:** Actively evaluates system time against the medicine schedule to project upcoming 24-hour doses and generate instant warnings for missed intervals.
*   **Safety & Overlap Checking Module:** Monitors proximity violations (flags schedules inside a tight 30-minute window) and screens inputs against a custom interaction matrix to alert users to toxic combinations.

## Technologies Used
*   **Language:** Python 3 (Object-Oriented Architecture)
*   **Core Libraries Used:** `datetime` (time tracking), `dataclasses` (clean data schemas), `difflib` (fuzzy string matching logic).
*   **Dependencies:** None. Built purely on the Python Standard Library for zero-configuration deployments.

## How to Install and Run

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/nessprksh0514/VITyarthi-Project.git
   ```
2. Navigate into the project root folder:
   ```bash
   cd VITyarthi-Project
   ```
3. Execute the entry point script:
   ```bash
   python main.py
   ```

## Instructions for Testing
To validate the codebase and ensure all core operations function as intended, execute the following evaluation procedures:

### 1. Functional System Testing
Run `python main.py` and input the following test vectors inside the CLI menu interface to check core functionality:
*   **Add Routine:** Choose option `1` to add a medication named `Aspirin`, dosage `100mg`, and set two distinct time intervals (e.g., `08:00`, `20:00`).
*   **Fuzzy Search Validation:** Choose the search action and intentionally spell the query as `Asprin` or `Asprn` to confirm the error-correction routing resolves to the entry.

### 2. Safety Matrix Testing (Edge Cases)
*   **Proximity Violation Check:** Create a secondary medicine entry and explicitly set its administration time to `08:15`. Confirm the system safely catches the conflict and triggers an overlap alert.
