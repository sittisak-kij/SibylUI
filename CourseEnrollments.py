import pandas as pd
import numpy as np
import time
import sys


class CourseEnrollments:
    course_ids = pd.read_csv("data/course_ids.csv", sep=',', header=0, usecols=['Id', 'Code'],
                             dtype={'Id': np.int, 'Code': str}, encoding='utf-8')
    course_df = pd.read_csv("data/course.csv", sep=',', header=0,
                            usecols=['CourseCode', 'FacultyCode', 'DepartmentCode', 'NameEN', 'IsValid', 'Credit'],
                            dtype={'CourseCode': str, 'FacultyCode': str, 'DepartmentCode': str, 'NameEN': str,
                                   'IsValid': bool, 'Credit': str}, encoding='utf-8')
    student_df = pd.read_csv("data/student.csv", sep=',', header=None, usecols=[0, 19, 20],
                             names=['StudentCode', 'CurrentGPA', 'CurrentCredit'],
                             dtype={'StudentCode': str, 'CurrentGPA': np.float64, 'CurrentCredit': np.float64},
                             encoding='utf-8')
    studygrade_df = pd.read_csv("data/studygrade.csv", sep=',', header=None, usecols=[0, 1, 2, 4, 5, 6],
                                names=['Year', 'Semester', 'StudentCode', 'CourseCode', 'SectionNumber', 'FinalGrade'],
                                dtype={'Year': np.int, 'Semester': np.int, 'StudentCode': str, 'CourseCode': str,
                                       'SectionNumber': np.int, 'FinalGrade': str}, encoding='utf-8')
    sectiondetail_df = pd.read_csv("data/sectiondetail.csv", sep=',', header=None, usecols=[0, 1, 2, 3, 9],
                                   names=['Year', 'Semester', 'CourseCode', 'SectionNumber', 'InstructorCode'],
                                   dtype={'Year': np.int, 'Semester': np.int, 'CourseCode': str,
                                          'SectionNumber': np.int, 'InstructorCode': str}, encoding='utf-8')
    instructor_df = pd.read_csv("data/instructor.csv", sep=',', header=None, usecols=[0, 1, 2],
                                names=['InstructorCode', 'FirstNameEN', 'LastNameEN'],
                                dtype={'InstructorCode': str, 'FirstNameEN': str, 'LastNameEN': str}, encoding='utf-8')
    coursegroup_df = pd.read_csv("data/coursegroup.csv", sep=',', header=0, usecols=[0, 3, 6],
                                 names=['CourseGroupId', 'CurriculumId', 'CourseType'],
                                 dtype={'CourseGroupId': np.int, 'CurriculumId': str, 'CourseType': str})
    curriculumcourse_df = pd.read_csv("data/CurriculumCourse.csv", sep=',', header=0,
                                      usecols=['CourseGroupId', 'CourseId', 'IsRequired', 'RequiredGrade'],
                                      dtype={'CourseGroupId': np.int, 'CourseId': np.int, 'IsRequired': bool,
                                             'RequiredGrade': str})
    student_curriculum = pd.read_csv("data/Student_Curriculum.csv", sep=',', header=0,
                                     dtype={'Batch': np.int, 'StudentCode': str, 'FacultyCode': str,
                                            'DepartmentCode': str, 'CurriculumId': str},
                                     names=['Batch', 'StudentCode', 'FacultyCode', 'DepartmentCode', 'CurriculumId'])
    curriculum = pd.read_csv("data/Curriculum.csv", sep=',', usecols=[0, 2], names=['CurriculumId', 'CurriculumName'],
                             dtype={'CurriculumId': str, 'CurriculumName': str})
    fkp_df = pd.read_csv("data/academicrecord.csv", sep=',', header=0, encoding='utf-8',
                         dtype={'Year': np.int, 'Semester': np.int, 'StudentCode': str, 'CourseCode': str,
                                'SectionNumber': np.int, 'FinalGrade': str})
    fkp_students = pd.read_csv("data/fkp_students.csv", sep=',', header=0, encoding='utf-8',
                               dtype={'StudentCode': str, 'CurrentGPA': np.float64, 'CurrentCredit': np.float64})
    eng_courses = []
    eng_sectiondetail_df = pd.Series([])

    # generate grade dict to map letters with numbers
    grade_dict = {'A': 4.00, 'A-': 3.75, \
                  'B+': 3.25, 'B': 3.00, 'B-': 2.75, \
                  'C+': 2.25, 'C': 2.00, 'C-': 1.75, \
                  'D': 1.00, 'F': 0.00, 'WP': 0.00, 'W': -1}

    grade_dict_reverse = dict(map(reversed, grade_dict.items()))

    def __init__(self):
        print("Start constructing CourseEnrollments...")
        self.studygrade_df = self.studygrade_df.append(self.fkp_df)

        self.student_df = self.student_df.append(self.fkp_students)

        self.course_ids.columns = ['CourseId', 'CourseCode']
        self.course_df['CourseCode'] = self.course_df['CourseCode'].apply(lambda x: x.strip())
        self.course_df = self.course_df.merge(self.course_ids, how='left', on='CourseCode')

        self.studygrade_df['CourseCode'] = self.studygrade_df['CourseCode'].apply(lambda x: x.strip())
        self.studygrade_df = self.studygrade_df.merge(self.course_ids, how='left', on='CourseCode')

        # Map student with curriculum
        self.student_df = self.student_df.merge(self.student_curriculum, on="StudentCode", how='left')
        self.student_df = self.student_df.merge(self.curriculum, how='left', on="CurriculumId")

        # insert studentId and courseid to studygrade
        self.student_df['StudentId'] = range(self.student_df.StudentCode.nunique())
        self.studygrade_df = self.studygrade_df.merge(self.student_df, on="StudentCode", how='left')

        print("Done constructing CouseEnrollment")

    def getStudygrade(self):
        return self.studygrade_df

    def getCurriculumCoursesOfStudentByCurriculumId(self, curriculumId):
        coursegroups = self.coursegroup_df
        curr_courses = self.curriculumcourse_df
        curr_courses = curr_courses.merge(coursegroups, how='left', on='CourseGroupId')
        coursegroups = coursegroups.loc[coursegroups['CurriculumId'] == curriculumId]['CourseGroupId'].tolist()
        curr_courses = curr_courses.loc[curr_courses['CourseGroupId'].isin(coursegroups)]

        curr_courses = curr_courses.merge(self.course_df, how='left', on='CourseId')
        curr_courses = curr_courses.drop(columns=['FacultyCode', 'DepartmentCode'])

        curriculum = {}
        curriculum['General'] = {}
        curriculum['Core'] = {}
        curriculum['Elective'] = {}
        curriculum['All'] = {}

        for index, row in curr_courses.iterrows():
            ctype = row['CourseType']
            cname = row['CourseCode']
            cgrade = row['RequiredGrade']
            curriculum[ctype][cname] = cgrade
            curriculum['All'][cname] = cgrade

        # return type,coursecode -> requiregrade
        return curriculum

    def getCourseEnrollments(self):

        '''
        This course enrollment is unique by StudentCode and CourseCode.
        We do not concern about other attributes related to the enrollments (such as instructors, year, semester, student's data)
        '''
        f = open("data/englishcourses.txt", "r")
        self.eng_courses = f.read().splitlines()
        f.close()

        print("Remove unused rows...")
        # keep studygrade with grades A,B,C,D,F and keep WP for English courses only
        self.studygrade_df = self.studygrade_df[self.studygrade_df['FinalGrade'].isin(self.grade_dict)]
        indexes = self.studygrade_df[(self.studygrade_df['FinalGrade'] == 'WP') & (
            ~self.studygrade_df['CourseCode'].isin(self.eng_courses))].index
        self.studygrade_df = self.studygrade_df.drop(indexes)

        print("Convert letter grades to numeric...")
        # insert numeric grade into the studygrade dataframe
        self.studygrade_df['NumericGrade'] = self.studygrade_df['FinalGrade'].map(self.grade_dict)

        # create tmp_df to store preprocessed_df
        tmp_df = self.studygrade_df.copy()
        tmp_df = tmp_df[pd.notnull(tmp_df['FinalGrade'])]

        tmp_df1 = tmp_df.groupby('CourseCode')['FinalGrade'].count().astype(float).reset_index(name='TotalEnrollments')
        tmp_df2 = tmp_df.groupby('CourseCode')['FinalGrade'].apply(
            lambda x: x[x == 'W'].count().astype(float)).reset_index(name='TotalWithdraw')
        tmp_df = tmp_df.merge(tmp_df1, how='left', on='CourseCode')
        tmp_df = tmp_df.merge(tmp_df2, how='left', on='CourseCode')
        tmp_df['CourseWithdrawRate'] = tmp_df['TotalWithdraw'] / tmp_df['TotalEnrollments']
        tmp_df = tmp_df.drop(['TotalEnrollments', 'TotalWithdraw'], axis=1)

        # remove duplicate course enrollments by aggregating the enrollments (mean of grades) and store how many times students taking this course
        # tmp_df['AccumGrade'] = tmp_df.groupby(['CourseCode', 'StudentCode'], as_index=False)['NumericGrade'].mean().NumericGrade
        tmp_df['TimesTaken'] = tmp_df.groupby(['CourseCode', 'StudentCode'], as_index=False)['Year'].count().Year
        # tmp_df = tmp_df.drop_duplicates(subset=['CourseCode', 'StudentCode'])

        tmp_df = tmp_df[tmp_df['FinalGrade'] != 'W']

        return tmp_df

    def getCourseType(self, coursecode):
        return self.course_df.loc[self.course_df['CourseCode'] == coursecode].CourseType

    # find drop rate of each course
    def getCourseWithdrawRate(self, df):
        tmp_df = self.studygrade_df.copy()
        tmp_df = tmp_df[['CourseCode', 'FinalGrade']]
        print(tmp_df.head())

        tmp_df['TotalEnrollments'] = tmp_df.groupby(['CourseCode'], as_index=False)['FinalGrade'].count().FinalGrade
        tmp_df['TotalWithdraw'] = tmp_df.loc[tmp_df['FinalGrade'] == 'W'].groupby(['CourseCode'], as_index=False)[
            'FinalGrade'].count().FinalGrade.astype(float)
        print(tmp_df.head())
        tmp_df['CourseWithdrawRate'] = tmp_df['TotalWithdraw'] / tmp_df['TotalEnrollments']

        tmp_df = tmp_df.drop(['TotalEnrollments', 'TotalWithdraw', 'FinalGrade'], axis=1)
        df = df.merge(tmp_df, how='left', on='CourseCode')
        return df

    def getCourseEnrollmentsWithInstructors(self):

        '''
        This course enrollment is unique by StudentCode, CourseCode and SectionID
        Steps
        1) Keep only English courses' sectiondetails in eng_sectiondetail_df
        2) Group instructors who teach the same course section which is unique by Year,Semester,SectionNumber,CourseCode
        3) Insert SectionID (same coursecode and same group of instructors) to eng_sectiondetail_df
        4) Create a copy of studygrade_df, name it 'tmp_df' and replace English CourseCode with <CourseCode_SectionID>
        5) Remove duplicate course enrollments by aggregating the enrollments and store how many times students taking this course
        '''

        print("Start preprocessing...")
        t0 = time.time()

        # step 1
        self.eng_sectiondetail_df = self.sectiondetail_df[self.sectiondetail_df.CourseCode.isin(self.eng_courses)]

        # step 2
        self.eng_sectiondetail_df = \
            self.eng_sectiondetail_df.groupby(['Year', 'Semester', 'SectionNumber', 'CourseCode'], as_index=False)[
                'InstructorCode'].apply(lambda x: ','.join(x.astype(str)))
        self.eng_sectiondetail_df = self.eng_sectiondetail_df.to_frame().reset_index()
        self.eng_sectiondetail_df.columns = ['Year', 'Semester', 'SectionNumber', 'CourseCode', 'InstructorCode']

        for index, row in self.eng_sectiondetail_df.iterrows():
            ls = np.unique(row.InstructorCode.split(','))
            self.eng_sectiondetail_df.at[index, 'InstructorCode'] = ','.join(ls)

        # step 3
        eng_tmp = self.eng_sectiondetail_df.copy()
        eng_tmp = eng_tmp.drop_duplicates(subset=['CourseCode', 'InstructorCode'])
        eng_tmp.insert(0, 'SectionID', range(0, len(eng_tmp)))
        eng_tmp = eng_tmp[['CourseCode', 'InstructorCode', 'SectionID']]
        self.eng_sectiondetail_df = self.eng_sectiondetail_df.merge(eng_tmp, on=['CourseCode', 'InstructorCode'],
                                                                    how='left')

        # step 4
        tmp_df = self.studygrade_df.copy()
        for index, row in tmp_df.iterrows():
            if row.CourseCode in self.eng_courses:
                sectionid = self.eng_sectiondetail_df['SectionID'].values[0]
                newCourseCode = "%s_%d" % (row.CourseCode, sectionid)
                tmp_df.at[index, 'CourseCode'] = newCourseCode

        # step 5
        # remove duplicate course enrollments by aggregating the enrollments (mean of grades) and store how many times students taking this course
        tmp_df['AccumGrade'] = tmp_df.groupby(['CourseCode', 'StudentCode'], as_index=False)[
            'NumericGrade'].mean().NumericGrade
        tmp_df['TimesTaken'] = tmp_df.groupby(['CourseCode', 'StudentCode'], as_index=False)['Year'].count().Year
        tmp_df = tmp_df.drop(['NumericGrade', 'FinalGrade'], axis=1)
        tmp_df = tmp_df.drop_duplicates(subset=['CourseCode', 'StudentCode'])

        t1 = time.time()
        print("Done preprocessing...")
        print("Time taken:", t1 - t0)
        return tmp_df
