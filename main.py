import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import os

CSV_FILE = "students.csv"

STUDY_MATERIALS = {
    "Maths": [
        "NCERT Maths Chapter PDFs",
        "Khan Academy - Algebra & Arithmetic",
        "TopperLearning Maths Basics"
    ],
    "Science": [
        "NCERT Science Textbook (Physics/Chemistry/Bio)",
        "Crash Course Science (YouTube)",
        "BYJU'S Science Concept Videos"
    ],
    "English": [
        "Basic Grammar - Wren & Martin PDF",
        "British Council English Learning Website",
        "Vocabulary practice on Quizlet"
    ],
    "History": [
        "NCERT History Notes",
        "Unacademy - History Basics",
        "Simple History (YouTube)"
    ],
    "Computer": [
        "Code.org basics",
        "Python for beginners (FreeCodeCamp)",
        "NCERT Computer Basics PDFs"
    ]
}

# DATA PREPROCESSING
def data_preprocess(df):
    subjects = ["Maths", "Science", "English", "History", "Computer"]
    # replacing null entries
    df[subjects] = df[subjects].T.fillna(df[subjects].mean(axis=1)).T
    # removing duplicates
    df.drop_duplicates(inplace=True)
    save_data(df)

# LOAD CSV
def load_data():
    if not os.path.exists(CSV_FILE):
        print("CSV file not found!")
        return None
    return pd.read_csv(CSV_FILE)

def save_data(df):
    df.to_csv(CSV_FILE, index=False)


# LOADING ANIMATION
def loading(text):
    print(text)
    for i in range(10):
        print("█" * (i+1) + "░" * (9-i), f"{(i+1)*10}%")
        time.sleep(0.04)


# BADGE SYSTEM
def assign_badge(student):
    total = student[["Maths","Science","English","History","Computer"]].sum()
    avg = total / 5

    if avg >= 90: return "🏆 Top Performer"
    elif avg >= 80: return "🎖 Consistent Performer"
    elif avg >= 70: return "📘 Improving Student"
    else: return "⚠ Needs Support"


# GET STUDY MATERIAL
def get_study_material(student_row):
    weak_subjects = {}

    for subject in ["Maths", "Science", "English", "History", "Computer"]:
        score = student_row[subject]

        if score < 60:
            weak_subjects[subject] = STUDY_MATERIALS[subject]

    return weak_subjects


# ADD NEW STUDENT
def add_student(df):
    print("\nADD NEW STUDENT")
    name = input("Name: ")

    marks = {}
    for subject in ["Maths","Science","English","History","Computer"]:
        marks[subject] = int(input(f"{subject} Marks: "))

    comp = int(input("Assignments Completed: "))
    due = int(input("Assignments Due: "))

    df.loc[len(df)] = [name] + list(marks.values()) + [comp, due]
    save_data(df)
    print("\nStudent Added Successfully!\n")


# HEATMAP
def show_heatmap(df):
    loading("\nGenerating Heatmap...")
    plt.imshow(df.iloc[:,1:6], cmap="viridis")
    plt.colorbar()
    plt.xticks(range(5), df.columns[1:6], rotation=90)
    plt.yticks(range(len(df)), df["Name"], fontsize=9, rotation=0)
    plt.title("Student Performance Heatmap")
    plt.tight_layout()
    plt.show()


# RADAR CHART
def radar_chart(student):
    loading("\nGenerating Radar Chart...")
    categories = ["Maths","Science","English","History","Computer"]
    values = [student[c] for c in categories]
    values += values[:1]

    angles = np.linspace(0, 2*np.pi, len(categories)+1)

    plt.figure(figsize=(6,6))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.3)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    plt.title(f"Skill Radar - {student['Name']}")
    plt.show()


# TRENDLINE
def show_trendline(df):
    loading("\nGenerating Trendline...")
    subjects = ["Maths","Science","English","History","Computer"]
    avg = df[subjects].mean()

    plt.plot(subjects, avg, marker='o')
    plt.title("Class Performance Trendline")
    plt.grid(True)
    plt.show()


# SUBJECT COMPARISON
def subject_comparison(df):
    loading("\nGenerating Subject Comparison...")
    subjects = ["Maths","Science","English","History","Computer"]
    avg = df[subjects].mean()

    plt.bar(subjects, avg)
    plt.title("Subject-Wise Class Averages")
    plt.ylabel("Marks")
    plt.show()


# RANK LIST
def ranklist(df):
    df["Total"] = df[["Maths","Science","English","History","Computer"]].sum(axis=1)
    ranked = df.sort_values(by="Total", ascending=False)

    print("\n🏆 TOP STUDENTS 🏆")
    print(ranked[["Name","Total"]].head())


# STUDENT MODE
def student_mode(df):
    name = input("Enter your name: ")

    if name not in df["Name"].values:
        print("Student not found!")
        return

    student = df[df["Name"] == name].iloc[0]
    weak_subs = get_study_material(student)

    print("\nYour Performance:")
    print(student)
    # warning on assignments that are to be due
    if student["Assignments_Due"] != 0:
        print(f"\nNO. OF INCOMPLETE ASSIGNMENTS: {student['Assignments_Due']}")
    else:
        print("\nALL ASSIGNEMNTS COMPLETED")

    radar_chart(student)

    if not weak_subs:
        print(f"\n🎉 {name} has no weak subjects! Great performance.")
    else:
        print(f"\n📘 Study material for weak subjects ({name}):")
        for subject, materials in weak_subs.items():
            print(f"\n--> {subject}:")
            for m in materials:
                print(f"   • {m}")

    badge = assign_badge(student)
    print("\nYour Badge:", badge)

# ----------------------------------
# TEACHER MODE
# ----------------------------------
def teacher_mode(df):
    while True:
        print("""
-----------------------------
        TEACHER MENU
-----------------------------
1. Add Student
2. View Heatmap
3. Radar Chart (any student)
4. Class Trendline
5. Subject Comparison
6. Rank List
0. Exit
-----------------------------
""")

        ch = input("Choice: ")

        if ch == "1":
            add_student(df)
        elif ch == "2":
            show_heatmap(df)
        elif ch == "3":
            name = input("Enter student name: ")
            if name in df["Name"].values:
                radar_chart(df[df["Name"]==name].iloc[0])
        elif ch == "4":
            show_trendline(df)
        elif ch == "5":
            subject_comparison(df)
        elif ch == "6":
            ranklist(df)
        elif ch == "0":
            break
        else:
            print("Invalid choice.")


# ----------------------------------
# MAIN MENU
# ----------------------------------
def main():
    df = load_data()
    if df is None: return

    data_preprocess(df)

    print("""
-----------------------------
   STUDENT REPORT SYSTEM
-----------------------------
1. Teacher Login
2. Student Login
0. Exit
-----------------------------
""")

    user = input("Choice: ")

    if user == "1":
        pwd = input("Enter teacher password: ")
        if pwd == "admin123":
            teacher_mode(df)
        else:
            print("Wrong password!")
    elif user == "2":
        student_mode(df)
    else:
        print("Goodbye!")

main()
