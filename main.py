import json
import csv
import os
from datetime import datetime

JFILE = "students.json"
CFILE = "students.csv"
LFILE = "activity_log.txt"


def load_data():
    if not os.path.exists(JFILE):
        return {}
    try:
        with open(JFILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("JSON file error. Original file preserved.")
        return None


def save_data(data):
    with open(JFILE, "w") as f:
        json.dump(data, f, indent=4)


def log(message):
    with open(LFILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")


def add_student(data):
    sid = input("Student ID: ").strip()

    if sid in data:
        print("Student ID already exists.")
        return

    name = input("Name: ")
    dept = input("Department: ")
    marks = {}

    for subject in ["Python", "Maths", "DBMS"]:
        while True:
            try:
                m = float(input(subject + " marks: "))
                if 0 <= m <= 100:
                    marks[subject] = m
                    break
                print("Enter marks between 0 and 100.")
            except ValueError:
                print("Enter numeric marks.")

    data[sid] = {
        "name": name,
        "department": dept,
        "marks": marks
    }

    save_data(data)
    log("Added student " + sid)
    print("Record saved to students.json.")


def search_student(data):
    sid = input("Enter ID: ")
    if sid in data:
        s = data[sid]
        print(f"Name: {s['name']} | Department: {s['department']}")
        for sub, mark in s["marks"].items():
            print(f"{sub}: {mark:g}", end=" | ")
        print()
    else:
        print("Student not found.")


def display_students(data):
    if not data:
        print("No records found.")
    for sid, student in data.items():
        print("\nStudent ID:", sid)
        print("Name:", student["name"])
        print("Department:", student["department"])
        print("Marks:", student["marks"])


def export_csv(data):
    with open(CFILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Department",
                         "Python", "Maths", "DBMS"])
        for sid, s in data.items():
            writer.writerow([
                sid, s["name"], s["department"],
                s["marks"]["Python"],
                s["marks"]["Maths"],
                s["marks"]["DBMS"]
            ])
    log("Exported records to CSV")
    print("CSV export completed:", CFILE)


def view_log():
    try:
        with open(LFILE, "r") as f:
            print("read():", f.read())
        with open(LFILE, "r") as f:
            print("readline():", f.readline())
        with open(LFILE, "r") as f:
            print("readlines():", f.readlines())
    except FileNotFoundError:
        print("Log file not found.")


def text_demo():
    with open("sample.txt", "w") as f:
        f.write("Student Records System\n")
        f.writelines(["File Handling\n", "JSON Example\n"])
    print("Text file created.")


def json_demo(data):
    sid = input("Enter ID: ")
    if sid in data:
        text = json.dumps(data[sid])
        print("JSON string:", text)
        print("Python object:", json.loads(text))
    else:
        print("Student not found.")


def main():
    data = load_data()
    if data is None:
        return

    while True:
        print("""
===== STUDENT RECORDS SYSTEM =====""")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("1. Add student")
            add_student(data)
        elif choice == "2":
            search_student(data)
        elif choice == "3":
            display_students(data)
        elif choice == "4":
            export_csv(data)
        elif choice == "5":
            view_log()
        elif choice == "6":
            json_demo(data)
        elif choice == "7":
            text_demo()
        elif choice == "8":
            print("Thank you!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
