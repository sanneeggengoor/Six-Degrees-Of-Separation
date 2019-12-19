## Degrees of Separation in a Student Population

# Instructions

## Prerequisites

```pip install nibabel, networkx, pandas```

```sudo apt install libcanberra-gtk-module libcanberra-gtk3-module```

```sudo apt install openjdk-8-jre openjdk-8-jdk```

please download gephi at: https://gephi.org/users/download/

*Linux* move the unzipped folder to this folder

*Windows* install gephi

## Run the program

for window's CMD:
`py main.py`
or if you want to run with a parameterfile
`py main.py "link\to\parameterfile"`
i.e.
`py main.py parameters\parametersdefault.csv`

Linux terminal:
`python main.py`
or if you want to run with a parameterfile
`py main.py "link/to/parameterfile"`
i.e.
`py main.py parameters/parametersdefault.csv`

the program will generate a network file named: net.gexf in default mode.

## Gephi

*Linux* To see the network using gephi use: `gephi-0.9.2/./bin/gephi *path/to/.gexf/file*`

*Windows* Open the file using gephi

A tutorial on how to generate nice looking graphs see: https://duo.com/blog/mapping-social-networks-with-gephi

We are using the Yifun Hu layout to generate our graphs and color the nodes according to the study.

# Program Description


## Default Mode

In default mode, the network will create 5000 students, make a gephi network file
named net.gexf and use the connection probabilities as stated in the parameter
description at the bottom of this file.

## Parameter Mode

If you want to specify the parameters yourself, you can add a parameterfile as
argument in the terminal, when running the main file. The format of the parameter
file can be found in parameters/parametersdefault.csv. A description of all
parameters is shown at the bottom of this file.


## Output Description

When running, the program will write during initialising and connecting the
students. In the end it will print the average degrees of separation. If wanted,
the connections are exported into a network that can be analyzed with Gephi.

# Files/Folders in Repo

* main.py: main python script
* classes.py: contains the student class, made for initialising students
* insert.py: file to read in data
* gephi_files: folder with some premade gephi networks, see section *Gephi* for showing
* results: folder with all the results and the means
* data_test.csv: file containing all the data that was collected regarding study programs and associations
* Overfiew faculties and programmes.xlsx: file received from RUG with registration numbers
* README.md: this one

# Parameter Description

* number_of_students = total number of students in simulation (default:30000)
* p_international_knows_international = probability two random international students know each other (default:0.00003)
* p_german_knows_german = probability two random German students know each other (default:0.0003)
* p_dutch_knows_dutch = probability two random Dutch students know eachother (default:0.001)
* p_faculty_knows_faculty = probability two random students from the same faculty know eachother (default:0.005)
* n_students_know_student_study_same_year = number of students a student probably knows at his/her study in the same year (default:25)
* n_students_know_student_study_other_year = number of students a student probably knows at his/her study in other years (default:10)
* n_students_know_student_study_other_phase = number of students a student probably knows at his/her study in the other phase (Bachelor <-> Master) (default:5)
* n_students_know_student_association = number of students a student probably knows at his/her association (default:30)
* with_study_association = boolean that contains whether study associations exist (default:True)
* with_student_association = boolean that contains whether studemt associations exist (default:True)
* make_network = boolean that contains whether a gephi network file should be made (default: True)
** WARNING: making a gephi network for 30,000 students takes a lot of time and memory.
* output_file = filename for where the output should be written to
* attempt_name = name of the attempt, will be used in outputfile and as name for gephi network file.
