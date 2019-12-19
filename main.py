# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 11:09:18 2019

@author: Adna Bliek, Sanne Eggengoor, Niklas Erdman, Thanasis Trantas

Main file: performs computations on "network level"
i.e. draw all students, draw connections and generating the social network
"""
import numpy as np
import random
import classes
import networkx as nx
import csv
import sys


""" Parameters we are conducting experiments on (default values)"""

number_of_students = 5000


# probabilities students of "same" nationality know each other randomly
p_international_knows_international = 0.00003
p_german_knows_german = 0.0003
p_dutch_knows_dutch = 0.001

# probability two students of same faculty know each other
p_faculty_knows_faculty = 0.005

#number of students you know in your study
n_students_know_student_study_same_year = 25
n_students_know_student_study_other_year = 10
n_students_know_student_study_other_phase = 5

#number of students you know in your association
n_students_know_student_association = 30

# holds whether study and student associations are taken into account
with_study_association = True
with_student_association = True

# holds whether a network needs to be modeled
make_network = True

# name of the output file that holds results
output_file = "outputfile.csv"
attempt_name = "attemptname"

net_file = "net.gexf"

list_of_all_students = []


# the length of the 1D list is n + n-1 + ... + 2 + 1 = ((n-1)n)/2
list_length_num = int(((number_of_students - 1) * number_of_students)/2)
# the 1 dimensional list (instead of n_students * n_students matrix)
distance_nodes1D = [0]* list_length_num


def give_index_1D_connections(student_1, student_2):
    """
    student_1, student_2: integers IDs of students
    distance_nodes1D is a 1 dimensional list of all connections between all students. This is not a 30,000 * 30,000 matrix
    because it takes too much memory, a function give_index_1D_connections() was written to transform the (N,M) matrix index
    into the index of the one dimensional list.
    Example:
                [0  a  b  c]
    3D matrix = [a  0  d  e]
                [b  d  0  f]
                [c  e  f  0]

    1D list = [a b c d e f]

    This function transforms the index in the 3D matrix to the 1D list index
    """
    if student_2 < student_1: # check if student_1 is the student with lowest id
        student_temp = student_1
        student_1 = student_2
        student_2 = student_temp
    diff = number_of_students - student_1 # needed to calculate start_index
    start_index = int(list_length_num - ((diff - 1) * diff) / 2) # index at which distances to student 1 starts
    addition = student_2 - student_1 - 1 # at which entry from start_index can index be found
    final_index = start_index + addition
    return final_index


def distance_nodes_check(student_1, student_2):
    """
    student_1, student_2: integers IDs of students
    function which returns the known distance. If two students are the same, distance is 0. Otherwise it will be looked
    up in the 1 dimensional list"""
    if student_1 == student_2:
        return 0
    return distance_nodes1D[give_index_1D_connections(student_1, student_2)]


def distance_nodes_make(student_1, student_2, val):
    """
    student_1, student_2: integers IDs of students
    val: integer of distance value
    function that assigns a distance value to an entry in the 1 dimensional list"""
    distance_nodes1D[give_index_1D_connections(student_1, student_2)] = val



def init_students():
    """ initializes all students

    """
    for i in range(0,number_of_students):
        new_student = classes.Student(i, with_study_association, with_student_association)
        new_student.draw_study_characteristics()
        new_student.draw_nonstudy_characteristics()
        list_of_all_students.append(new_student)
        if i%200 == 0:
            print(str(i) + " students initialized")



def add_connections():
    """ adds connections between all students if they are in the same study or association
    """
    for i in range(0,number_of_students-1): # go trough all students
        student1 = list_of_all_students[i]
        if i % 100 == 0:
            print("for " + str(i) + " of students connections made")
        for j in range(i+1 , number_of_students): #go through all students a  second time
            student2 = list_of_all_students[j]
            # add students to connections based on study and membership of association
            if(student1.id!=student2.id and student1.has_connection(student2.id)==False): # connection to self already added, only search for connection if no connection exists
                # keeps track of whether these students are already connected
                connection = 0
                if(student1.study == student2.study): #check whether they do the same study
                    if(student1.BM == student2.BM): #check whether they are both in the master or bachelor
                        if(student1.year == student2.year):
                            #add connections within the same study and same year
                            if(n_students_know_student_study_same_year/student1.studentsInStudy > random.random()):
                                student1.create_connection(student2.id)
                                student2.create_connection(student1.id)
                                connection = 1

                        else:
                            # add connections within the same study and phase
                            if (n_students_know_student_study_other_year / student1.studentsInStudy > random.random()):
                                student1.create_connection(student2.id)
                                student2.create_connection(student1.id)
                                connection = 1

                    else:
                        # add connections between bachelor and master
                        if (n_students_know_student_study_other_phase / student1.studentsInStudy > random.random()):
                            student1.create_connection(student2.id)
                            student2.create_connection(student1.id)
                            connection = 1

                if(len(student1.association) > 0 and len(student2.association) > 0 and connection == 0):
                    #print(student1.association)
                    for ass1 in range(0,len(student1.association)-1):
                        for ass2 in range(0,len(student2.association)-1):
                            if(student1.association[ass1] == student2.association[ass2]):
                                #add connections
                                if(n_students_know_student_association/student1.studentsInAssociation[ass1] > random.random()):
                                    student1.create_connection(student2.id)
                                    student2.create_connection(student1.id)
                                    connection = 1

                if (student1.faculty == student2.faculty and connection == 0):
                    if p_faculty_knows_faculty > random.random():
                        student1.create_connection(student2.id)
                        student2.create_connection(student1.id)
                        connection = 1

                # connect students randomly based on nationality
                # numbers of students from https://www.rug.nl/news/2018/11/groningen-remains-popular-with-dutch-and-international-students?lang=en
                # assuming around 7000 internationals, of which 5000 masters (4000 other international, 1000 german) (of 10000 Master students in total
                # and of which 2000 bachelors (1000 other int and 1000 german) (of 20000 bachelor students in total)
                # assuming probability of two dutch students knowing each other = 0.1 %
                #                             german                            = 0.03%
                #                             other international               = 0.003%
                if (student1.international == student2.international and connection == 0):
                    if student1.international == "Dutch":
                        if p_dutch_knows_dutch > random.random():
                            student1.create_connection(student2.id)
                            student2.create_connection(student1.id)
                            connection = 1
                    elif student1.international == "German":
                        if p_german_knows_german > random.random():
                            student1.create_connection(student2.id)
                            student2.create_connection(student1.id)
                            connection = 1
                    else:
                        if p_international_knows_international > random.random():
                            student1.create_connection(student2.id)
                            student2.create_connection(student1.id)
                            connection = 1



def calc_average_dist():
    """
    calculates the average distance between 1% of all students
    """
    sum_dist = 0
    no_connection = 0
    for n in range(int(number_of_students/100)):
        student1 = random.choice(list_of_all_students)
        student2 = random.choice(list_of_all_students)
        dist = breadth_first_search(student1, student2)
        if(dist < 0):
            dist = 7
        sum_dist = sum_dist + dist
    if sum_dist > 0:
        return sum_dist/(number_of_students/100-no_connection)
    else:
        return -1

def calc_average_dist_faculty(name_faculty):
    """
    name_faculty: String
    calculates the average distance between students of one faculty for 10% of the students
    the names of the faculties are: FSE, FA, FEB, FBSS, FTRS, FMS, FL, FSS, FP, OT, O, UCG
    """
    students_in_faculty = []
    for student in list_of_all_students:
        if(student.faculty == name_faculty):
            students_in_faculty.append(student)
    sum_dist = 0
    no_connection = 0
    for n in range(int(len(students_in_faculty)/10)):
        student1 = random.choice(students_in_faculty)
        student2 = random.choice(students_in_faculty)
        dist = breadth_first_search(student1, student2)
        if(dist < 0):
            dist = 7
        sum_dist = sum_dist + dist
    if sum_dist > 0:
        return sum_dist/(len(students_in_faculty)/10-no_connection)
    else:
        return -1

def calc_average_dist_nationality(nationality):
    """
    name_faculty: String
    calculates the average distance between students of one nationality for 10% of the students
    the names of the nationalities are Dutch, German, Other
    """
    students_nationality= []
    for student in list_of_all_students:
        if(student.international == nationality):
            students_nationality.append(student)
    sum_dist = 0
    no_connection = 0
    for n in range(int(len(students_nationality)/10)):
        student1 = random.choice(students_nationality)
        student2 = random.choice(students_nationality)
        dist = breadth_first_search(student1, student2)
        if(dist < 0):
            dist = 7
        sum_dist = sum_dist + dist
    if sum_dist > 0:
        return sum_dist/(len(students_nationality)/10- no_connection)
    else:
        return -1

def calc_average_dist_associations(amount_associations):
    """
    amount_associations: Int
    calculates the average distance between students of one nationality for 10% of the students
    the amount of associations is the minimum amount of associations the student is member of
    """
    students_associations= []
    for student in list_of_all_students:
        if(len(student.association) >= amount_associations):
            students_associations.append(student)
    sum_dist = 0
    no_connection = 0
    for n in range(int(len(students_associations)/10)):
        student1 = random.choice(students_associations)
        student2 = random.choice(students_associations)
        dist = breadth_first_search(student1, student2)
        if(dist < 0):
            dist = 7
        sum_dist = sum_dist + dist
    if sum_dist > 0:
        return sum_dist/(len(students_associations)/10-no_connection)
    else:
        return -1

def calc_charact_connections():
    min_s = 100
    max_s = 0
    tot = 0
    for student in list_of_all_students:
        num_connections = len(student.connections)
        tot += num_connections
        if num_connections < min_s:
            min_s = num_connections
        elif max_s < num_connections:
            max_s = num_connections
    tot = float(tot/number_of_students)
    return [tot, min_s, max_s]


def breadth_first_search(node1, node2):
    """
    returns the distance between two nodes, updates the distance between other nodes at the same time
    took https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/ as starting point

    parameters: node1, node2 : Student
    """
    #only calculate distnace if the distance is not yet calculated
    if(node1.id != node2.id and distance_nodes_check(node1.id,node2.id) == 0):
        #Mark all vertices as not visited
        visited = [False] * number_of_students

        # Create a queue for BFS
        queue = []

        #create array containing the parent node of the node
        parents_id = np.zeros(number_of_students)

        # Mark the source node as
        # visited and enqueue it
        queue.append(node1)
        visited[node1.id] = True
        parents_id[node1.id] = int(node1.id)
        #print(parents_id)

        visited_node2 = False
        while not(visited_node2) and queue:

            #get next not visited node
            next_node = queue.pop(0)
            next_node_dist = distance_nodes_check(next_node.id,int(parents_id[next_node.id]))


            #for all connections of the node
            for i in next_node.connections:
                if visited[i] == False:
                    queue.append(list_of_all_students[i])
                    visited[i] = True
                    parents_id[i] = next_node.id
                    distance_nodes_make(i,next_node.id,next_node_dist + 1)
                    # distance_nodes_make(next_node.id,i,next_node_dist + 1)
                    if(i == node2.id):
                        visited_node2 = True
                        return distance_nodes_check(next_node.id,i)
        return -1
    else:
        return distance_nodes_check(node1.id,node2.id)

def generate_network():
    """generates a file that can be read into Gephi

    """
    network = nx.Graph()
    for i in range(0,number_of_students):
        network.add_node(i)
        for edge in list_of_all_students[i].connections:
            network.add_edge(list_of_all_students[i].id, edge)
    for n in range(0,number_of_students):
        network.nodes[n]['label'] = list_of_all_students[n].id
        network.nodes[n]['Study'] = classes.studyNames.index(list_of_all_students[n].study)
        network.nodes[n]['nationality'] = classes.nationalities.index(list_of_all_students[n].international)
        network.nodes[n]['Faculty'] = classes.facultyNames.index(list_of_all_students[n].faculty)
        if(len(list_of_all_students[n].association)>0):
            network.nodes[n]['Association'] = classes.associationNames.index(list_of_all_students[n].association[0])

    nx.write_gexf(network, net_file)

def write_results():
    """ Function to write results to csv file. Decomment lines in first run, for having headers"""
    with open(output_file, mode='a') as results_file:
        results_writer = csv.writer(results_file, delimiter=',')
        # results_writer.writerow(['Attempt_name', 'Avg dist', 'Avg dist Dutch', 'Avg dist German', 'Avg dist International',
        #                          'Avg dist FSE', 'Avg dist FA', 'Avg dist FEB', 'Avg dist FBSS', 'Avg dist FTRS', 'Avg dist FMS',
        #                          'Avg dist FL', 'Avg dist FSS', 'Avg dist FP', 'Avg dist OT', 'Avg dist O', 'Avg dist UCG',
        #                          'Avg number of con p student','Min number of con p student','Max number of con p student',
        #                          'Avg dist over 5 associations', 'Avg dist over 3 associations','Avg dist over 1 associations'])
        results_writer.writerow([attempt_name, calc_average_dist(), calc_average_dist_nationality("Dutch"),calc_average_dist_nationality("German"),
                                 calc_average_dist_nationality("Other"), calc_average_dist_faculty("FSE"), calc_average_dist_faculty("FA"),
                                 calc_average_dist_faculty("FEB"), calc_average_dist_faculty("FBSS"), calc_average_dist_faculty("FTRS"),
                                 calc_average_dist_faculty("FMS"), calc_average_dist_faculty("FL"), calc_average_dist_faculty("FSS"),
                                 calc_average_dist_faculty("FP"), calc_average_dist_faculty("OT"), calc_average_dist_faculty("O"),
                                 calc_average_dist_faculty("UCG"), calc_charact_connections()[0], calc_charact_connections()[1],
                                 calc_charact_connections()[2], calc_average_dist_associations(3),calc_average_dist_associations(1),""])


def include_parameters(filename):
    """
    filename: string
    function for including parameters from parameter file"""
    global number_of_students, p_international_knows_international,p_german_knows_german,p_dutch_knows_dutch, p_faculty_knows_faculty
    global n_students_know_student_study_same_year, n_students_know_student_study_other_year, n_students_know_student_study_other_phase
    global n_students_know_student_association, with_study_association, with_student_association, make_network, output_file, attempt_name
    global list_length_num, distance_nodes1D
    global net_file

    with open(filename, mode='r') as para_file:
        para_reader = csv.reader(para_file, delimiter=',')
        for row in para_reader:
            if row[0] == "number_of_students":
                number_of_students = int(row[1])
            if row[0] == "p_international_knows_international":
                p_international_knows_international = float(row[1])
            elif row[0] == "p_german_knows_german":
                p_german_knows_german = float(row[1])
            elif row[0] == "p_dutch_knows_dutch":
                p_dutch_knows_dutch = float(row[1])
            elif row[0] == "p_faculty_knows_faculty":
                p_faculty_knows_faculty = float(row[1])
            elif row[0] == "n_students_know_student_study_same_year":
                n_students_know_student_study_same_year = int(row[1])
            elif row[0] == "n_students_know_student_study_other_year":
                n_students_know_student_study_other_year = int(row[1])
            elif row[0] == "n_students_know_student_study_other_phase":
                n_students_know_student_study_other_phase = int(row[1])
            elif row[0] == "n_students_know_student_association":
                n_students_know_student_association = int(row[1])
            elif row[0] == "with_study_association":
                with_study_association = bool(row[1])
            elif row[0] == "with_student_association":
                with_student_association = bool(row[1])
            elif row[0] == "make_network":
                make_network = bool(row[1])
            elif row[0] == "output_file":
                output_file = row[1]
            elif row[0] == "attempt_name":
                attempt_name = row[1]
                net_file = row[1] + "net.gexf"

    list_length_num = int(((number_of_students - 1) * number_of_students) / 2)
    distance_nodes1D = [0] * list_length_num

def main():
    # include parameters if necessary
    if len(sys.argv) > 1:
        include_parameters(str(sys.argv[1]))
    print("init students")
    init_students()
    print("add connections")
    add_connections()
    if make_network:
        generate_network()
    write_results()
    print("average dist: ")
    print(calc_average_dist())






if __name__ == "__main__":
    main()
