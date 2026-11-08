r"""Find exam dates for the courses listed in a registration PDF.

Install the PDF text extractor once if needed:
    pip install PyPDF2

Example:
    python find_exam_dates.py ^
        "D:\downloads\FINAL EXAM TIMETABLE 2026-2027.1.pdf" ^
        "C:\Users\chuko\OneDrive\Documents\research methods\Report_639276532871416381.pdf"
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from PyPDF2 import PdfReader


DATE_PATTERN = re.compile(
    r"\b(?P<weekday>Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s*,?\s*"
    r"(?P<date>\d{1,2}-\d{2}-\d{4})"
)
COURSE_PATTERN = re.compile(r"\b[A-Z]{3,5}\d{3}[A-Z]?\b")
TIME_PATTERN = re.compile(
    r"(?P<start>\d{1,2}:\d{2}\s+[AP]M)\s+"
    r"(?P<end>\d{1,2}:\d{2}\s+[AP]M)"
)


@dataclass(frozen=True)
class Exam:
    course_code: str
    date: str
    weekday: str
    start: str
    end: str
    details: str


def pdf_text(path: Path) -> str:
    """Return all extractable text from a PDF."""
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def registration_courses(path: Path) -> set[str]:
    """Find course codes in the student's registration PDF."""
    return set(COURSE_PATTERN.findall(pdf_text(path)))


def timetable_exams(path: Path, wanted_courses: set[str]) -> list[Exam]:
    """Find timetable rows whose course code is in wanted_courses."""
    exams: list[Exam] = []
    current_date: tuple[str, str] | None = None

    for raw_line in pdf_text(path).splitlines():
        line = " ".join(raw_line.split())
        date_match = DATE_PATTERN.search(line)
        if date_match:
            current_date = (
                date_match.group("weekday"),
                date_match.group("date"),
            )

        if current_date is None:
            continue

        course_match = COURSE_PATTERN.search(line)
        time_match = TIME_PATTERN.search(line)
        if not course_match or not time_match:
            continue

        course_code = course_match.group()
        if course_code not in wanted_courses:
            continue

        # Remove the date and time prefix so the remaining text is easy to read.
        details = line[time_match.end() :].strip()
        exams.append(
            Exam(
                course_code=course_code,
                date=current_date[1],
                weekday=current_date[0],
                start=time_match.group("start"),
                end=time_match.group("end"),
                details=details,
            )
        )

    return exams


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find exam dates for courses listed in a registration PDF."
    )
    parser.add_argument("timetable_pdf", type=Path)
    parser.add_argument("registration_pdf", type=Path)
    parser.add_argument(
        "--course",
        dest="extra_courses",
        action="append",
        default=[],
        help="Also search for a course code not listed in the registration PDF.",
    )
    args = parser.parse_args()

    wanted_courses = registration_courses(args.registration_pdf)
    wanted_courses.update(course.upper() for course in args.extra_courses)
    exams = timetable_exams(args.timetable_pdf, wanted_courses)
    found_courses = {exam.course_code for exam in exams}

    print("Exam dates")
    print("==========")
    for exam in exams:
        print(
            f"{exam.course_code}: {exam.weekday}, {exam.date} "
            f"({exam.start}-{exam.end}) - {exam.details}"
        )

    missing = sorted(wanted_courses - found_courses)
    if missing:
        print("\nNot found in timetable: " + ", ".join(missing))


if __name__ == "__main__":
    main()
