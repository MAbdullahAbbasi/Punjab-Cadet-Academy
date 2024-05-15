from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///academy_data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Stud(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    father = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    classNo = db.Column(db.Integer, nullable = False)
    subjects = db.Column(db.String(500), nullable = False)
    phone = db.Column(db.String(200), nullable = False)
    date_admission = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"{self.sno} - {self.name} - {self.father} - {self.classNo} - {self.phone}"

class Tea(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    classNo = db.Column(db.Integer, nullable = False)
    subjects = db.Column(db.String(500), nullable = False)
    phone = db.Column(db.String(200), nullable = False)
    date_admission = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"{self.sno} - {self.name} - {self.classNo} - {self.phone}"

class Stud_fee(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    classNo = db.Column(db.Integer, nullable = False)
    status = db.Column(db.String(20), nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    date_admission = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"{self.sno} - {self.name} - {self.classNo}"

class Tea_Sal(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    classNo = db.Column(db.Integer, nullable = False)
    status = db.Column(db.String(20), nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    date_admission = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"{self.sno} - {self.name} - {self.classNo}"

class Std_Att(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    classNo = db.Column(db.Integer, nullable = False)
    attend = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"{self.sno} - {self.name}"

class Tea_Att(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    attend = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"{self.sno} - {self.name}"

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/students")
def students():
    return render_template('StudentsManagement/students.html')

@app.route("/teachers")
def teachers():
    return render_template('TeachersManagement/teachers.html')

@app.route("/finance")
def finance():
    return render_template('FinanceManagement/finance.html')

@app.route("/attendance")
def attendance():
    return render_template("AttendanceManagement/attendance.html")

@app.route("/std_fin")
def finance_std():
    return render_template('FinanceManagement/students_fee.html')

@app.route("/tea_fin")
def finance_tea():
    return render_template('FinanceManagement/teachers_fin.html')

@app.route("/view_std")
def view():
    allStds = Stud.query.all()
    allStds = sorted(allStds, key=lambda x: x.classNo)
    return render_template('StudentsManagement/view_std.html', allStds = allStds)

@app.route("/view_tea")
def view_tea():
    allTea = Tea.query.all()
    allTea = sorted(allTea, key=lambda x: x.sno)
    return render_template('TeachersManagement/view_tea.html', allTea = allTea)

@app.route("/add_std")
def add_std():
    return render_template('StudentsManagement/add_std.html')

@app.route("/add_tea")
def add_tea():
    return render_template('TeachersManagement/add_tea.html')

@app.route("/add", methods = ['POST'])
def add():
    current_datetime = datetime.now().time()
    sno = current_datetime.strftime("%H%M%S")
    name = request.form['name']
    father = request.form['fathername']
    email = request.form['email']
    classNo = request.form['class']
    subjects = request.form.getlist('subjects')
    subjects = ', '.join(subjects)
    phone = request.form['number']
    date_admission = datetime.now().date()


    addStudent = Stud(sno = sno, name = name , father = father, email = email, classNo = classNo,subjects = subjects,  phone = phone, date_admission = date_admission)
    student_fee = Stud_fee(sno = sno, name = name, classNo=classNo, status = 'Unpaid', amount = 0, date_admission = date_admission)
    std_attendance = Std_Att(sno = sno, name = name, classNo=classNo, attend = 'Absent')
    db.session.add(addStudent)
    db.session.add(student_fee)
    db.session.add(std_attendance)
    db.session.commit()

    return redirect('/add_std')

@app.route("/upd_std/<int:sno>")
def update(sno):
    upd = Stud.query.filter_by(sno = sno).first()
    return render_template("StudentsManagement/update_std.html", upd = upd)

@app.route("/update/<int:sno>", methods = ['POST'])
def update_student(sno):
    name = request.form['name']
    father = request.form['fathername']
    email = request.form['email']
    classNo = request.form['class']
    subjects = request.form.getlist('subjects')
    subjects = ', '.join(subjects)
    phone = request.form['number']
    
    upd = Stud.query.filter_by(sno = sno).first()

    upd.name = name
    upd.father = father
    upd.email = email
    upd.classNo=classNo
    upd.subjects=subjects
    upd.phone = phone

    upd1 = Stud_fee.query.filter_by(sno = sno).first()
    upd1.name = name
    upd1.classNo=classNo

    db.session.add(upd)
    db.session.add(upd1)
    db.session.commit()

    return redirect("/view_std")

@app.route("/del_std/<int:sno>")
def delete(sno):
    delete = Stud.query.filter_by(sno = sno).first()
    delete_data = Stud_fee.query.filter_by(sno = sno).first()

    db.session.delete(delete)
    db.session.delete(delete_data)
    db.session.commit()
    return redirect("/view_std")
    
@app.route("/add_teacher", methods = ['POST'])
def add_teacher():
    current_datetime = datetime.now().time()
    sno = current_datetime.strftime("%H%M%S")
    name = request.form['name']
    email = request.form['email']
    classNo = request.form.getlist('class')
    classNo = ', '.join(classNo)
    subjects = request.form.getlist('subjects')
    subjects = ', '.join(subjects)
    phone = request.form['number']
    date_admission = datetime.now().date()


    addTeacher = Tea(sno = sno, name = name , email = email, classNo = classNo, subjects = subjects,  phone = phone, date_admission = date_admission)
    teacher_sal = Tea_Sal(sno = sno, name = name, classNo=classNo, status = 'Unpaid', amount = 0, date_admission = date_admission)
    teacher_att = Tea_Att(sno = sno, name = name, attend = 'Absent')
    
    db.session.add(addTeacher)
    db.session.add(teacher_sal)
    db.session.add(teacher_att)

    db.session.commit()

    return redirect('/add_tea')

@app.route("/upd_tea/<int:sno>")
def update_teach(sno):
    upd = Tea.query.filter_by(sno = sno).first()
    return render_template("TeachersManagement/update_tea.html", upd = upd)

@app.route("/update_teacher/<int:sno>", methods = ['POST'])
def update_teacher(sno):
    name = request.form['name']
    email = request.form['email']
    classNo = request.form.getlist('class')
    classNo = ', '.join(classNo)
    subjects = request.form.getlist('subjects')
    subjects = ', '.join(subjects)
    phone = request.form['number']
    
    upd = Tea.query.filter_by(sno = sno).first()
    upd1 = Tea_Sal.query.filter_by(sno = sno).first()

    upd.name = name
    upd1.name = name

    upd.email = email
    upd.classNo=classNo
    upd1.classNo=classNo

    upd.subjects=subjects
    upd.phone = phone

    db.session.add(upd)
    db.session.add(upd1)

    db.session.commit()

    return redirect("/view_tea")

@app.route("/del_tea/<int:sno>")
def delete_teacher(sno):
    delete = Tea.query.filter_by(sno = sno).first()
    delete1 = Tea_Sal.query.filter_by(sno = sno).first()

    db.session.delete(delete)
    db.session.delete(delete1)
    db.session.commit()
    return redirect("/view_tea")

@app.route("/students_fee_record")
def std_fee_record():
    allStds = Stud_fee.query.all()
    allStds = sorted(allStds, key=lambda x: x.classNo)
    return render_template('FinanceManagement/students_fee_record.html', allStds = allStds)

@app.route("/std_fee/<int:sno>")
def std_fee(sno):
    selected_std = Stud_fee.query.filter_by(sno = sno).first()
    return render_template('FinanceManagement/students_fee.html', selected_std = selected_std)

@app.route("/teachers_salary")
def tea_salary():
    allTeas = Tea_Sal.query.all()
    allTeas = sorted(allTeas, key=lambda x: x.sno)
    return render_template('FinanceManagement/teachers_salary.html', allTeas = allTeas)

@app.route("/teachers_salary_record")
def tea_salary_record():
    allTeas = Tea_Sal.query.all()
    allTeas = sorted(allTeas, key=lambda x: x.sno)
    return render_template('FinanceManagement/teachers_salary_record.html', allTeas = allTeas)

@app.route("/tea_sal/<int:sno>")
def tea_sal(sno):
    selected_tea = Tea_Sal.query.filter_by(sno = sno).first()
    return render_template('FinanceManagement/teachers_salary.html', selected_tea = selected_tea)

@app.route("/std_fee_edit/<int:sno>", methods = ['POST'])
def std_fee_edit(sno):
    status = request.form[f'fee_status{sno}']
    amount = request.form['amount']
    
    upd = Stud_fee.query.filter_by(sno = sno).first()
    upd.status = status
    upd.amount=amount


    db.session.add(upd)
    db.session.commit()

    return redirect('/students_fee_record')

@app.route("/tea_sal_edit/<int:sno>", methods = ['POST'])
def tea_sal_edit(sno):
    status = request.form[f'fee_status{sno}']
    amount = request.form['amount']
    
    upd = Tea_Sal.query.filter_by(sno = sno).first()
    upd.status = status
    upd.amount=amount


    db.session.add(upd)
    db.session.commit()

    return redirect('/teachers_salary_record')

@app.route("/clear_std_fee")
def clear_std_fee():
    download_std_data()
    Stud_fee.query.update({Stud_fee.status: 'Unpaid'})
    Stud_fee.query.update({Stud_fee.amount: 0})
    db.session.commit()
    return redirect('/students_fee_record')

@app.route("/clear_tea_sal")
def clear_tea_sal():
    download_tea_data()
    Tea_Sal.query.update({Stud_fee.status: 'Unpaid'})
    Tea_Sal.query.update({Stud_fee.amount: 0})
    db.session.commit()
    return redirect('/teachers_salary_record')

def download_std_data():
    all_fees = Stud_fee.query.all()

    data = [['Roll No', 'Name', 'Class', 'Status', 'Amount']]
    for fee in all_fees:
        data.append([fee.sno, fee.name, fee.classNo, fee.status, fee.amount])

    month_name = datetime.now().month    
    pdf = f'student_fees_report_{month_name}.pdf'
    folder_path = 'templates/StudentsFiles'
    pdf_filename = os.path.join(folder_path, pdf)
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    table = Table(data)

    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)
    doc.build([table])

    return pdf_filename

def download_tea_data():
    all_fees = Tea_Sal.query.all()

    data = [['Roll No', 'Name', 'Class', 'Status', 'Amount']]
    for fee in all_fees:
        data.append([fee.sno, fee.name, fee.classNo, fee.status, fee.amount])

    month_name = datetime.now().month    
    folder_path = 'templates/TeachersFiles'
    pdf= f'teacher_salary_report_{month_name}.pdf'
    pdf_filename = os.path.join(folder_path, pdf)
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    table = Table(data)

    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)
    doc.build([table])

    return pdf_filename

@app.route("/std_prev_record")
def std_prev_record():
    folder_path = 'templates/StudentsFiles'

    # Read all PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    return render_template("/FinanceManagement/std_previous_record.html", pdf_files = pdf_files)

@app.route('/pdf_files_students/<path:filename>')
def view_students_pdf(filename):
    folder_path = 'templates/StudentsFiles'
    return send_from_directory(folder_path, filename)

@app.route("/tea_prev_record")
def tea_prev_record():
    folder_path = 'templates/TeachersFiles'

    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    return render_template("/FinanceManagement/teacher_previous_record.html", pdf_files = pdf_files)

@app.route('/pdf_files_teachers/<path:filename>')
def view_teachers_pdf(filename):
    folder_path = 'templates/TeachersFiles'
    return send_from_directory(folder_path, filename)

@app.route("/students_attendance_classes")
def students_attendance_classes():
    return render_template('AttendanceManagement/std_classes.html')

@app.route("/nine_class_attendance")
def nine_class_attendance():
    allStds = Std_Att.query.filter_by(classNo=9).all()
    allStds = sorted(allStds, key=lambda x: x.sno)
    return render_template('AttendanceManagement/nine_class_attendance.html', allStds = allStds)

@app.route("/ten_class_attendance")
def ten_class_attendance():
    allStds = Std_Att.query.filter_by(classNo=10).all()
    allStds = sorted(allStds, key=lambda x: x.sno)
    return render_template('AttendanceManagement/ten_class_attendance.html', allStds = allStds)

@app.route("/eleven_class_attendance")
def eleven_class_attendance():
    allStds = Std_Att.query.filter_by(classNo=11).all()
    allStds = sorted(allStds, key=lambda x: x.sno)
    return render_template('AttendanceManagement/eleven_class_attendance.html', allStds = allStds)

@app.route("/twelve_class_attendance")
def twelve_class_attendance():
    allStds = Std_Att.query.filter_by(classNo=12).all()
    allStds = sorted(allStds, key=lambda x: x.sno)
    return render_template('AttendanceManagement/twelve_class_attendance.html', allStds = allStds)

@app.route("/teachers_attendance")
def teachers_attendance():
    allTeas = Tea_Att.query.all()
    allTeas = sorted(allTeas, key=lambda x: x.sno)
    return render_template('AttendanceManagement/teachers_attendance.html', allTeas = allTeas)

@app.route("/tea_att_edit/<int:sno>", methods = ['POST'])
def tea_att_edit(sno):
    status = request.form[f'att_status{sno}']
    
    upd = Tea_Att.query.filter_by(sno = sno).first()
    upd.status = status

    db.session.add(upd)
    db.session.commit()

    return redirect('/teachers_attendance')


if __name__ == "__main__":
    app.run(debug=True)