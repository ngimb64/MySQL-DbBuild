districtDatabase = 'CREATE DATABASE district'

districtTables = [ 
'''
CREATE TABLE districtEmployees (
employee_id INT PRIMARY KEY,
first_name VARCHAR(40) NOT NULL,
last_name VARCHAR(40) NOT NULL,
language_1 VARCHAR(3) NOT NULL,
language_2 VARCHAR(3),
dob DATE,
tax_id INT UNIQUE,
phone_num VARCHAR(20));
''', 
'''
CREATE TABLE districtClient (
client_id INT PRIMARY KEY,
client_name VARCHAR(40) NOT NULL,
address VARCHAR(60) NOT NULL,
industry VARCHAR(20));
''',
'''
CREATE TABLE districtParticipant (
participant_id INT PRIMARY KEY,
first_name VARCHAR(40) NOT NULL,
last_name VARCHAR(40) NOT NULL,
phone_num VARCHAR(20),
client INT);
''',
'''
CREATE TABLE districtCourse (
course_id INT PRIMARY KEY,
course_name VARCHAR(40) NOT NULL,
language VARCHAR(3) NOT NULL,
level VARCHAR(2),
course_len_weeks INT,
start_date DATE,
in_school BOOLEAN,
teacher INT,
client INT);
'''
]

districtAlterations = [
'''
ALTER TABLE districtParticipant 
ADD FOREIGN KEY(client)
REFERENCES districtClient(client_id)
ON DELETE SET NULL;
''',
'''
ALTER TABLE districtCourse
ADD FOREIGN KEY(teacher)
REFERENCES districtEmployees(employee_id)
ON DELETE SET NULL;
''',

'''
ALTER TABLE districtCourse
ADD FOREIGN KEY(client)
REFERENCES districtClient(client_id)
ON DELETE SET NULL;
''',

'''
CREATE TABLE district_TakesCourse (
participant_id INT,
course_id INT,
PRIMARY KEY(participant_id, course_id),
FOREIGN KEY(participant_id) REFERENCES districtParticipant(participant_id) ON DELETE CASCADE,
FOREIGN KEY(course_id) REFERENCES districtCourse(course_id) ON DELETE CASCADE);
'''
]

districtPopulate = [
'''
INSERT INTO districtEmployees VALUES
(1, 'James', 'Smith', 'ENG', NULL, '1985-04-20', 12345, '+491774553676'),
(2, 'Stefanie', 'Martin', 'FRA', NULL, '1970-02-17', 23456, '+491234567890'),
(3, 'Steve', 'Wang', 'MAN', 'ENG', '1990-11-12', 34567, '+447840921333'),
(4, 'Friederike', 'Muller-Rossi', 'DEU', 'ITA', '1987-07-07', 45678, '+492345678901'),
(5, 'Isobel', 'Ivanova', 'RUS', 'ENG', '1963-05-30', 56789, '+491772635467'),
(6, 'Niamh', 'Murphy', 'ENG', 'IRI', '1995-09-08', 67890, '+491231231232');
''',
'''
INSERT INTO districtClient VALUES
(101, 'Big Business Federation', '123 Falschingstrabe, 10999 Berlin', 'NGO'),
(102, 'eCommerce GmbH', '27 Ersatz Allee, 10317 Berlin', 'Retail'),
(103, 'AutoMaker AG', '20 Kunstlichstrabe, 10023 Berlin', 'Auto'),
(104, 'Banko Bank', '12 Betrugstrabe, 12345 Berlin', 'Banking'),
(105, 'WeMoveIt GmbH', '138 Arglistweg, 10065 Berlin', 'Logistics');
''',
'''
INSERT INTO districtParticipant VALUES
(101, 'Marina', 'Berg', '491635558182', 101),
(102, 'Andrea', 'Duerr', '49159555740', 101),
(103, 'Philipp', 'Probst', '49155555692', 102),
(104, 'Rene', 'Brandt', '4916355546', 102),
(105, 'Susanne', 'Shuster', '49155555779', 102),
(106, 'Christian', 'Schreiner', '49162555375', 101),
(107, 'Harry', 'Kim', '49177555633', 101),
(108, 'Jan', 'Nowak', '49151555824', 101),
(109, 'Pablo', 'Garcia', '49162555176', 101),
(110, 'Melanie', 'Dreschler', '49151555527', 103),
(111, 'Dieter', 'Durr', '49178555311', 103),
(112, 'Max', 'Mustermann', '49152555195', 104),
(113, 'Maxine', 'Mustermann', '49177555355', 104),
(114, 'Heikp', 'Fleishcer', '49155555581', 105);
''',
'''
INSERT INTO districtCourse VALUES
(12, 'English for Logistics', 'ENG', 'A1', 10, '2020-02-01', TRUE, 1, 105),
(13, 'Beginner English', 'ENG', 'A2', 40, '2019-11-12', FALSE, 6, 101),
(14, 'Intermediate English', 'ENG', 'B2', 40, '2019-11-120', FALSE, 6, 101),
(15, 'Advanced English', 'ENG', 'C1', 40, '2019-11-12', FALSE, 6, 101),
(16, 'Mandarin for Autoindustries', 'ENG', 'B1', 15, '2020-01-15', TRUE, 3, 103),
(17, 'Francais Intermediate', 'FRA', 'B1', 18, '2020-04-03', FALSE, 2, 101),
(18, 'Deutsch for Anfanger', 'DEU', 'A2', 8, '2020-02-14', TRUE, 4, 102),
(19, 'Intermediate English', 'ENG', 'B2', 10, '2020-03-29', FALSE, 1, 104),
(20, 'Fortgeschrittens Russisch', 'RUS', 'C1', 4, '2020-04-08', FALSE, 5, 103);
''',
'''
INSERT INTO district_takesCourse VALUES
(101, 15),
(101, 17),
(102, 17),
(103, 18),
(104, 18),
(105, 18),
(106, 13),
(107, 13),
(108, 13),
(109, 14),
(109, 15),
(110, 16),
(110, 20),
(111, 16),
(114, 12),
(112, 19),
(113, 19);
'''
]