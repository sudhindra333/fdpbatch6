import streamlit as st
import sqlite3
import pandas as pd

# Page configuration
st.set_page_config(page_title="Student Management App", layout="wide")

# Database initialization
DATABASE = "students.db"

def init_database():
    """Create database and table if they don't exist."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            grade TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# CRUD Functions
def insert_student(name, email, phone, grade):
    """Add a new student record."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, email, phone, grade) VALUES (?, ?, ?, ?)",
        (name, email, phone, grade)
    )
    conn.commit()
    conn.close()

def view_students():
    """Fetch all student records."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_student_by_id(student_id):
    """Fetch a specific student by ID."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_student(student_id, name, email, phone, grade):
    """Update an existing student record."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET name = ?, email = ?, phone = ?, grade = ? WHERE id = ?",
        (name, email, phone, grade, student_id)
    )
    conn.commit()
    conn.close()

def delete_student(student_id):
    """Delete a student record."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

# Initialize database on app startup
init_database()

# Streamlit UI
st.title("📚 Student Management System")
st.write("Manage student records with ease using SQLite database")

# Sidebar navigation
operation = st.sidebar.radio("Select Operation", ["Create", "Read", "Update", "Delete"])

# CREATE Operation
if operation == "Create":
    st.header("➕ Add New Student")
    with st.form("add_student_form"):
        name = st.text_input("Student Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        grade = st.text_input("Grade/Class")
        submit_btn = st.form_submit_button("Add Student")
        
        if submit_btn:
            if name and email and phone and grade:
                insert_student(name, email, phone, grade)
                st.success(f"✅ Student '{name}' added successfully!")
            else:
                st.error("⚠️ Please fill all fields!")

# READ Operation
elif operation == "Read":
    st.header("📖 View All Students")
    students = view_students()
    
    if students:
        df = pd.DataFrame(students, columns=["ID", "Name", "Email", "Phone", "Grade"])
        st.dataframe(df, use_container_width=True)
        st.info(f"Total Students: {len(students)}")
    else:
        st.warning("No student records found.")

# UPDATE Operation
elif operation == "Update":
    st.header("✏️ Update Student Record")
    students = view_students()
    
    if students:
        student_ids = [s[0] for s in students]
        student_names = [f"ID {s[0]} - {s[1]}" for s in students]
        
        selected = st.selectbox("Select Student to Update", student_names)
        selected_id = int(selected.split()[1])
        
        student = get_student_by_id(selected_id)
        
        with st.form("update_student_form"):
            name = st.text_input("Student Name", value=student[1])
            email = st.text_input("Email Address", value=student[2])
            phone = st.text_input("Phone Number", value=student[3])
            grade = st.text_input("Grade/Class", value=student[4])
            submit_btn = st.form_submit_button("Update Student")
            
            if submit_btn:
                if name and email and phone and grade:
                    update_student(selected_id, name, email, phone, grade)
                    st.success(f"✅ Student '{name}' updated successfully!")
                else:
                    st.error("⚠️ Please fill all fields!")
    else:
        st.warning("No student records found.")

# DELETE Operation
elif operation == "Delete":
    st.header("🗑️ Delete Student Record")
    students = view_students()
    
    if students:
        student_names = [f"ID {s[0]} - {s[1]}" for s in students]
        selected = st.selectbox("Select Student to Delete", student_names)
        selected_id = int(selected.split()[1])
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("❌ Delete Student", key="delete_btn"):
                delete_student(selected_id)
                st.success("✅ Student deleted successfully!")
                st.rerun()
        
        with col2:
            st.button("Cancel", key="cancel_btn")
    else:
        st.warning("No student records found.")

# Footer
st.divider()
st.caption("💡 Student Management App - Built with Streamlit & SQLite3")