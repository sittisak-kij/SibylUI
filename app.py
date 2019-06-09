from flask import Flask, render_template, jsonify, request
from CourseEnrollments import CourseEnrollments
import pandas as pd
import numpy as np

app = Flask(__name__)

ce = CourseEnrollments()
tmp = ce.getCourseEnrollments()
course_matrix = pd.read_csv("data/course_matrix.csv", header=0, engine='python', sep=',')
student_matrix = pd.read_csv("data/student_matrix.csv", header=0, engine='python', sep=',')
student_bias = pd.read_csv("data/student_bias.csv", header=None, names=['StudentCode', 'bias'], engine='python',
                           sep=',')
course_bias = pd.read_csv("data/course_bias.csv", header=None, names=['CourseCode', 'bias'], engine='python', sep=',')
with open('data/mu.txt') as f:
    mu = float(f.readline().strip())

def mf(studentcode, coursecode):
    try:
        w = student_matrix.loc[student_matrix['StudentCode'] == int(studentcode)].iloc[:, 1:].values  # 1 x K
        u = course_matrix.loc[course_matrix['CourseCode'] == coursecode].iloc[:, 1:].values  # 1 x K

        b = student_bias.loc[student_bias['StudentCode'] == int(studentcode)].bias.values
        c = course_bias.loc[course_bias['CourseCode'] == coursecode].bias.values

        print("Student matrix 1xK of", studentcode, w)
        print("Course matrix 1xK of", coursecode, u)
        print("Student bias:", b, "Course bias:", c)
        grade = w.dot(u.T) + b + c + mu
        return grade[0][0]
    except (KeyError, IndexError):
        return -1


def mf_noprint(studentcode, coursecode):
    try:
        w = student_matrix.loc[student_matrix['StudentCode'] == int(studentcode)].iloc[:, 1:].values  # 1 x K
        u = course_matrix.loc[course_matrix['CourseCode'] == coursecode].iloc[:, 1:].values  # 1 x K

        b = student_bias.loc[student_bias['StudentCode'] == int(studentcode)].bias.values
        c = course_bias.loc[course_bias['CourseCode'] == coursecode].bias.values

        grade = w.dot(u.T) + b + c + mu
        return grade[0][0]
    except (KeyError, IndexError):
        return -1


def rmse(predicted_ls, actual_ls):
    sum = 0.
    N = len(predicted_ls)
    for i in range(N):
        sum += (predicted_ls[i] - actual_ls[i]) ** 2
    return (sum / float(N)) ** .5


def findMeanCourse(coursecode):
    try:
        studyrecords = ce.getStudygrade()
        meangrade = studyrecords.loc[studyrecords['CourseCode'] == coursecode]['NumericGrade'].mean()
        mediangrade = studyrecords.loc[studyrecords['CourseCode'] == coursecode]['NumericGrade'].median()
        modegrade = studyrecords.loc[studyrecords['CourseCode'] == coursecode]['NumericGrade'].mode().tolist()
        if str(meangrade) == 'nan':
            meangrade = -1.0
        if str(mediangrade) == 'nan':
            mediangrade = -1.0
        if len(modegrade) < 1:
            modegrade = [-1.0]
        return [meangrade, mediangrade, modegrade]
    except KeyError:
        return [-1, -1, -1]

def findActualGrade(studentcode, coursecode):
    try:
        studyrecords = ce.getStudygrade()
        studyrecords = studyrecords.loc[studyrecords['StudentCode'] == studentcode]
        actualgrade = studyrecords.loc[studyrecords['CourseCode'] == coursecode]['NumericGrade'].max()
        if str(actualgrade) == 'nan':
            return -1
        return actualgrade
    except KeyError:
        return -1

def predict(studentcode, curriculumId):
    curriculum_courses = ce.getCurriculumCoursesOfStudentByCurriculumId(curriculumId)
    general_ls = curriculum_courses['General']
    core_ls = curriculum_courses['Core']
    elective_ls = curriculum_courses['Elective']
    all_ls = curriculum_courses['All']
    course_df = ce.course_df

    predicted_ls = []
    actual_ls = []

    generalCourses = []
    coreCourses = []
    electiveCourses = []

    print("Mean grades of all courses from all students:", mu)
    print()
    if len(general_ls) > 0:
        print("///// GENERAL COURSES /////")
        for course in general_ls:
            predicted_grade = mf(studentcode, course)
            actual_grade = findActualGrade(studentcode, course)
            course_name = course_df.loc[course_df['CourseCode'] == course].NameEN.values[0]
            if actual_grade != -1:
                predicted_ls.append(predicted_grade)
                actual_ls.append(actual_grade)
            generalCourses.append({
                'CourseCode': course,
                'CourseName': course_name,
                'RequiredGrade': general_ls[course],
                'PredictedGrade': "%.2f" % predicted_grade,
                'ActualGrade': actual_grade,
                'Credit': course_df.loc[course_df['CourseCode'] == course].Credit.values[0],
                'Type': 'General'
            })
            # print("Course Code: ", course, "Course Name: ", course_name, " Require grade: ", general_ls[course])
            stat = findMeanCourse(course)
            # print("Mean: ", "%.2f" % stat[0], "Median: ", "%.2f" % stat[1], "Mode: ", stat[2])
            # print("Predicted grade: ", "%.2f" % predicted_grade, " Actual grade: ", actual_grade)
            # print()

    if len(core_ls) > 0:
        # print("///// CORE COURSES /////")
        for course in core_ls:
            predicted_grade = mf(studentcode, course)
            actual_grade = findActualGrade(studentcode, course)
            course_name = course_df.loc[course_df['CourseCode'] == course].NameEN.values[0]
            if actual_grade != -1:
                predicted_ls.append(predicted_grade)
                actual_ls.append(actual_grade)

            coreCourses.append({
                'CourseCode': course,
                'CourseName': course_name,
                'RequiredGrade': core_ls[course],
                'PredictedGrade': "%.2f" % predicted_grade,
                'ActualGrade': actual_grade,
                'Credit': course_df.loc[course_df['CourseCode'] == course].Credit.values[0],
                'Type': 'Core'
            })
            # print("Course Code: ", course, "Course Name: ", course_name, " Require grade: ", core_ls[course])
            stat = findMeanCourse(course)
            # print("Mean: ", "%.2f" % stat[0], "Median: ", "%.2f" % stat[1], "Mode: ", stat[2])
            # print("Predicted grade: ", "%.2f" % predicted_grade, " Actual grade: ", actual_grade)
            # print()

    if len(elective_ls) > 0:
        # print("///// ELECTIVE COURSES /////")
        for course in elective_ls:
            predicted_grade = mf(studentcode, course)
            actual_grade = findActualGrade(studentcode, course)
            course_name = course_df.loc[course_df['CourseCode'] == course].NameEN.values[0]
            if actual_grade != -1:
                predicted_ls.append(predicted_grade)
                actual_ls.append(actual_grade)

            coreCourses.append({
                'CourseCode': course,
                'CourseName': course_name,
                'RequiredGrade': elective_ls[course],
                'PredictedGrade': "%.2f" % predicted_grade,
                'ActualGrade': actual_grade,
                'Credit': course_df.loc[course_df['CourseCode'] == course].Credit.values[0],
                'Type': 'Elective'
            })
            # print("Course Code: ", course, "Course Name: ", course_name, " Require grade: ", elective_ls[course])
            stat = findMeanCourse(course)
            # print("Mean: ", "%.2f" % stat[0], "Median: ", "%.2f" % stat[1], "Mode: ", stat[2])
            # print("Predicted grade: ", "%.2f" % predicted_grade, " Actual grade: ", actual_grade)
            # print()

    # if len(predicted_ls) > 0:
    #     print("RMSE:", str(rmse(predicted_ls, actual_ls)))
    #     print("---------------")

    data = {
        'General': generalCourses,
        'Core': coreCourses,
        'Elective': electiveCourses
    }

    return data

@app.route('/student', methods=['GET', 'POST'])
def getStudent():
    if request.method == 'POST':
        id = request.data.decode("utf-8")
        student_df = ce.student_df
        student = pd.DataFrame([])
        if id in student_df['StudentCode'].values:
            student = student_df.loc[student_df['StudentCode'] == id]
            studentData = {
                'GPA': student.CurrentGPA.values[0],
                'Credits': student.CurrentCredit.values[0]
            }
            predictedData = predict(student.StudentCode.values[0], student.CurriculumId.values[0])
            return jsonify({
                'StudentData': studentData,
                'PredictedData': predictedData
            })
        return '404'

    if request.method == 'GET':
        data = {
            'name': 'kij',
            'etc': 'wow'
        }

        data2 = {
            'name': 'fern',
            'etc': 'wow'
        }
        datas = [data, data2]
        return jsonify(datas)
    # name = {}
    # for key, value in request.form.items():
    #     name[ key ] = value
    #
    # customer_obj = customer_class.Customer()
    # results = customer_obj.search_customer( name )

    return jsonify('none')

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
