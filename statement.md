# Problem Statement

## The Problem
Medication non-adherence is a pervasive issue where individuals forget to take their medications on schedule, leading to missed doses and compromised treatment. Furthermore, polypharmacy—taking multiple medications simultaneously—increases the risk of scheduling doses too close together or combining drugs that have adverse interactions. Existing solutions are often overly complex, require continuous internet connectivity, or compromise user privacy by storing health data on external servers.

## Scope of the Project
This project is scoped as a lightweight, single-user, offline console application. It does not aim to replace professional medical advice or act as a verified pharmacology database. Instead, it provides a reliable, privacy-centric local tool for a user to actively manage their own schedule, record known interaction warnings provided by their doctor, and receive automated schedule conflict alerts. Data is handled entirely in memory during the application session.

## Target Users
- Individuals managing multiple daily prescriptions.
- Caregivers keeping track of a dependent's medication schedule.
- Anyone who frequently forgets their dose timings and needs a simple tracker without the overhead of a full mobile app.

## High-Level Features
- **Medication CRUD Operations:** Add, remove, and list medications with detailed schedules, durations, and food instructions.
- **Fuzzy Search:** Typo-tolerant search capability to find scheduled medicines quickly.
- **Dose Tracking:** Automatically calculate upcoming doses within a 24-hour window and identify past missed doses based on a time buffer.
- **Safety Overlap Detection:** Scan daily schedules to detect and warn if two different medicines are scheduled within an unsafe time buffer (e.g., 30 minutes).
- **Interaction Warnings:** Allow users to log known drug interactions, which the system will use to actively warn the user if both drugs are currently scheduled.
