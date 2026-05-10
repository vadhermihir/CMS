import pandas as pd

# Define the header and student data
students = [
    ['Alice', '101', 88, 92, 85, 265, 'A'],
    ['Bob', '102', 75, 70, 72, 217, 'B'],
    ['Charlie', '103', 95, 98, 94, 287, 'A+'],
    ['David', '104', 60, 65, 58, 183, 'C'],
    ['Eva', '105', 82, 78, 80, 240, 'B+']
]
header = ['Name', 'Roll No', 'Maths', 'Science', 'English', 'Total', 'Grade']

# Create DataFrame
df = pd.DataFrame(students, columns=header)

# Save to CSV using to_csv()
df.to_csv("student_data.csv", index=False)

print("CSV file 'student_data.csv' has been created using to_csv().")
