# Exam Date Finder

This script reads:

1. A university exam timetable PDF.
2. A student registration/certificate PDF containing the registered course codes.

It then prints each matching unit's full course title, exam day, date, time,
and venue.

## Requirements

- Python 3.9 or newer
- `PyPDF2`

Install the dependency from PowerShell:

```powershell
python -m pip install PyPDF2
```

## Usage

Run the script with the timetable PDF first and the registration PDF second:

```powershell
python .\find_exam_dates.py `
  "D:\downloads\FINAL EXAM TIMETABLE 2026-2027.1.pdf" `
  "C:\Users\chuko\OneDrive\Documents\research methods\Report_639276532871416381.pdf"
```

The script extracts the course codes from the registration PDF and searches
for those codes in the timetable. The output includes the exam date, time,
full timetable row, and venue.

## Searching for an additional unit

To search for a unit that is not present in the registration PDF, add one or
more `--course` options. For example, to include **COSC403 - Real Time
Systems**:

```powershell
python .\find_exam_dates.py `
  "D:\downloads\FINAL EXAM TIMETABLE 2026-2027.1.pdf" `
  "C:\Users\chuko\OneDrive\Documents\research methods\Report_639276532871416381.pdf" `
  --course COSC403
```

## Current result for COSC403

In the timetable used for this project, **COSC403 - Real Time Systems** is
scheduled for **Friday, 27 November 2026, 7:00 AM-10:00 AM**, at the **Main
Auditorium**.
