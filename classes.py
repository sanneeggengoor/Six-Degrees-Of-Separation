# -*- coding: utf-8 -*-
"""

Classes file: computes everything on "student level"
i.e. which characteristics does the student have etc.
"""

import numpy as np
import insert
import random

# insert data from csv file
data = insert.load_data()
students_per_study = data.groupby('Study').sum()[1:]
students_per_study = students_per_study[1:]
number_of_students = students_per_study.sum(axis=0)[1]
nationalities = ["Dutch","German","Other"]


# studies with number of students, for drawing a weighted random study per student
studyNames = students_per_study.index.values.tolist()
studyWeights = list(students_per_study['Members'])
studyWeightsNorm = [float(i)/sum(studyWeights) for i in studyWeights]
facultyNames = data.groupby('Faculty').sum()[1:].index.values.tolist()
associationsOnly = data[data['Study'] == '0']
associationNames = associationsOnly.index.values.tolist()


class Student(object):
    """ class of students, containing the different characteristics of each student

        parameters: id : int

    """
    def __init__(self, id, with_study_association, with_student_association):
        self.connections = []
        self.id = id
        self.connections.append(id)
        # which study, year and Bachelor or Master
        self.study = np.random.choice(studyNames, p=studyWeightsNorm)
        self.year = 0
        self.BM = 0  #Bachelor or Master
        # list of associations that student is member of
        self.association = []
        self.studentsInAssociation = []
        # nationality of student (might change into "german" or "other" later)
        self.international = "Dutch"
        #number of students in study and year
        self.studentsInStudy = 0
        # faculty study is member of
        self.faculty = 0

        self.with_study_association = with_study_association
        self.with_student_association = with_student_association
       # etc.


    def create_connection(self, id_new_connection):
        """ creates a new connection between the current student and another student

            parameters: id_new_connection : Int
        """
        if(not(id_new_connection in self.connections)):
            self.connections.append(id_new_connection)
            self.connections.sort()

    def has_connection(self, id_other_student):
        if(id_other_student in self.connections):
            return True
        else:
            return False

    # this will randomly draw the characteristics of the student, based on its study
    # will then be used to create connections that "make sense"
    def draw_study_characteristics(self):
        # only select data relevant for study of student
        studyOnly = data[data['Study'] == self.study]
        # give student faculty
        self.faculty = studyOnly['Faculty'].iloc[0]

        # decide whether student is master or bachelor, random choice from weighted list
        #only do random choice if the study exists in the bachelor and master otherwise assign the only possibility
        if(len(studyOnly)>1):
            bmWeights = [studyOnly.groupby(['BM']).sum().iloc[0]['Members'],
                         studyOnly.groupby(['BM']).sum().iloc[1]['Members']]
            self.BM = np.random.choice(['B', 'M'], p=[float(i)/sum(bmWeights) for i in bmWeights])
        else:
            self.BM = studyOnly['BM'][0]

        # only select data relevant for study AND studyphase of student
        studyOnly = studyOnly[studyOnly['BM'] == self.BM]
        # decide which year, similarly to how phase is decided
        # 40% 1. year bachelor, 35% 2. year, 25% 3.year
        # master one year, as not all masters are 2 years
        if(self.BM == 'B'):
            yearWeights = [0.4,0.35,0.25]
        else:
            yearWeights = [1,0,0]

        self.year = np.random.choice([1, 2, 3], p=[float(i) / sum(yearWeights) for i in yearWeights])
        if((len(studyOnly) == 1) or (self.BM == 'B')):
            self.studentsInStudy = yearWeights[self.year-1] * studyOnly.groupby(['BM']).sum().iloc[0]['Members']
        else:
            self.studentsInStudy = studyOnly.groupby(['BM']).sum().iloc[1]['Members']



    # draw the associations students are member of
    def draw_nonstudy_characteristics(self):
        # decide whether student stays Dutch or becomes German or of other nationality
        if self.BM == 'B':
            if 0.1 > random.random():
                if 0.5 > random.random():
                    self.international = "German"
                else:
                    self.international = "Other"
        else:
            if 0.5 > random.random():
                if 0.8 > random.random():
                    self.international = "Other"
                else:
                    self.international = "German"
        # only select non study data
        noStudyOnly = data[data['Study'] == '0']
        # for all possible associations, calculate probability of being a member and then randomly draw whether they are one
        for index, row in noStudyOnly.iterrows():
            # check whether it is a study association: if so, only enrolled students are eligible
            if(len(self.association) < 3):
                if (row['Study-Association'] == '0' and self.with_student_association) or (self.study in row['Study-Association'].split(' ') and self.with_study_association):
                    #check whether the association is international or only for dutch students
                    if((row['Association']!='Dutch') or ((row['Association']!='Dutch') and self.international == 'Dutch') ):
                        if(row['Study-Association'] == '0'):
                            p = float((row['Members']/number_of_students)/2)  # members of associations can be students at the rug or hanze
                        else:
                            p = float(row['Members']/self.studentsInStudy)
                        if np.random.random() < p:
                            # if so, add association to list
                            self.association = self.association + [index]
                            self.studentsInAssociation = self.studentsInAssociation + [row['Members']]
            else:
                break
