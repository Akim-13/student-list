import logging
import sys
import os

STUDENT_LIST_DIR_ABSOLUTE_PATH = os.path.join(sys.path[ 0 ], 'student_list/')

# TODO: Implement class Subject() and corresponding csv files for each subject.

# TODO: Link students and subjects by creating one relational file.csv:
# student1.csv, subject2.csv, subject3.csv, subject6.csv
# student5.csv, subject1.csv, subject2.csv
# ...
 
# EXPERIMENTAL: I'm unsure about the usefulness of
# this class yet, but it may have some applications.
# Ask AK to search for 'Null' and examine the code.
# SEE: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s24.html
class Null:
    """ Null objects always and reliably "do nothing." """

    def __init__(self, *args, **kwargs): 
        pass
    def __call__(self, *args, **kwargs): 
        return self
    def __repr__(self): 
        return "Null( )"
    def __nonzero__(self): 
        return 0
    def __getattr__(self, name): 
        return self
    def __setattr__(self, name, value): 
        return self
    def __delattr__(self, name): 
        return self

class StudentList():
    def get_raw_list_of_students(self):
        try:
            self.students = StudentList.__read_each_file(self)
            return self.students
        except FileNotFoundError:
            StudentList.__create_dir_if_nonexistent(self)
            StudentList.get_raw_list_of_students(self)
        except:
            StudentList.__exit_with_error()

    def __read_each_file(self):
        # HACK: self.students doesn't work, so using a local list instead.
        students = []

        student_files = StudentList.__get_sorted_list_of_files()
        for student_file in student_files:
            with open(STUDENT_LIST_DIR_ABSOLUTE_PATH + student_file, 'r') as self.cur_student_file:
                student = self.cur_student_file.read()
                # QUESTION: why doesn't self.students.append(...) work?
                students.append(student)

        return students

    @staticmethod
    def __get_sorted_list_of_files():
        os.chdir(STUDENT_LIST_DIR_ABSOLUTE_PATH)
        student_files = os.listdir(STUDENT_LIST_DIR_ABSOLUTE_PATH)
        # NOTE: Sort the list of files by date. 
        student_files.sort(key = os.path.getmtime)

        return student_files

    def __create_dir_if_nonexistent(self):
        if not os.path.exists(STUDENT_LIST_DIR_ABSOLUTE_PATH):
            os.makedirs(STUDENT_LIST_DIR_ABSOLUTE_PATH)

    @staticmethod
    def __exit_with_error():
        sys.exit(f'ERROR: cannot access or modify "{STUDENT_LIST_DIR_ABSOLUTE_PATH}" directory.')

    def add_student_file(self, student, filename):
        try: 
            with open(STUDENT_LIST_DIR_ABSOLUTE_PATH + filename, 'w') as self.cur_student_file:
                self.cur_student_file.write(student)
        except FileNotFoundError:
            StudentList.__create_dir_if_nonexistent(self)
            StudentList.add_student_file(self, student, filename)
        except:
            StudentList.__exit_with_error()

class Student():
    def __init__(self, parameters):
        self.parameters = parameters

    def get_parameter(self, parameter_name):
        if parameter_name in self.parameters:
            return self.parameters[ parameter_name ]
        else:
            return Null() 
            #raise TypeError(f'parameter {parameter_name} does not exist.')

    def set_parameter(self, parameter_name, parameter_value):
        if parameter_name in self.parameters:
            # TODO: Validate the parameter.
            self.parameters[ parameter_name ] = parameter_value
            return True
        else:
            return False

    def write_to_file(self):
        student_in_csv_format = Student.__get_in_csv_format(self)
        filename = Student.__generate_filename(self)
        StudentList().add_student_file(student_in_csv_format, filename)

    def __get_in_csv_format(self):
        student_in_csv_format = ''

        i = 1
        for self.key, self.value in self.parameters.items():
            is_last_iteration = i==len(self.parameters)
            student_in_csv_format += Student.__get_parameter_with_delimiter(self, is_last_iteration)
            i += 1

        return student_in_csv_format

    def __get_parameter_with_delimiter(self, is_last_iteration):
        format = f'"{self.key}":"{self.value}"'
        if is_last_iteration:
            return format + '\n'
        else:
            return format + ', '

    def __generate_filename(self):
        first_name = self.parameters[ 'first_name' ]
        last_name = self.parameters[ 'last_name' ]
        extension = 'csv'
        filename = f'{first_name}_{last_name}.{extension}'
        return filename

class Validator():
    def __init__(self, entered_parameter):
        self.value = entered_parameter[ 'input_value' ]
        self.type = entered_parameter[ 'type' ]
        self.restrictions = entered_parameter[ 'restrictions' ]
        self.options = entered_parameter[ 'options' ]

        self.valid = False
        self.result = ''
        self.error = ''

    def is_valid(self):
        Validator.__validate_by_type(self)

        if self.valid:
            if self.restrictions:
                Validator.__validate_restrictions(self)

            has_options = not isinstance(self.options, Null)
            if has_options:
                Validator.__validate_options(self)

        return self.valid

    def __validate_by_type(self):
        if self.type == 'string':
            Validator.__validate_string(self)
        elif self.type == 'number': 
            Validator.__validate_number(self)
        else:
            sys.exit('ERROR: Unknown parameter type.')

    def __validate_string(self):
        # NOTE: Any user input can be converted to string, so just return it.
        self.result = str(self.value)
        self.valid = True

    def __validate_number(self):
        try:
            self.result = float(self.value)
            self.valid = True
        except:
            self.error = 'The value is not a number.'
            self.valid = False

    def __validate_restrictions(self):
        for restriction in self.restrictions:
            if restriction == 'non-empty':
                Validator.__validate_non_empty_restriction(self, restriction)

            elif restriction == 'integer':
                Validator.__validate_integer_restriction(self)

            elif restriction == 'positive':
                Validator.__validate_positive_restriction(self, restriction)

            else:
                return

    def __validate_non_empty_restriction(self, restriction):
        try:
            Validator.__check_if_empty(self, self.result)
        except:
            Validator.__exit_with_error_invalid_restriction(self, restriction)

    def __check_if_empty(self, result):
        if result == '':
            self.error = 'The value is empty.'
            self.valid = False

    def __exit_with_error_invalid_restriction(self, restriction):
        sys.exit(f'ERROR: invalid restriction {restriction} for type {self.type}')

    def __validate_integer_restriction(self):
        try:
            Validator.__check_if_integer(self, self.result)
        except:
            self.error = 'The value is not an integer.'
            self.valid = False

    def __check_if_integer(self, result):
        if result == int(result):
            self.result = int(result)
        else:
            self.error = 'The value is a number but not an integer.'
            self.valid = False

    def __validate_positive_restriction(self, restriction):
        try:
            Validator.__check_if_positive(self, self.result)
        except:
            Validator.__exit_with_error_invalid_restriction(self, restriction)

    def __check_if_positive(self, result):
        if result <= 0:
            self.valid = False
            self.error = 'The value is not positive'

    def __validate_options(self):
        value_found = False

        for option in self.options:
            if option == self.result:
                value_found = True

        if not value_found:
            self.error = 'The value was not found in the list of valid options'
            self.valid = False

def main():
    initialisation()
    print_actions()
    while True:
        select_action()

def initialisation():
    global required_parameters, actions
    actions = [ 
        { 'description':'Quit',                          'function':quit },
        { 'description':'Add a new students',            'function':add_student },
        { 'description':'List all students',             'function':list_students },
        { 'description':'Edit an existing student',      'function':edit_student },
        { 'description':'List all subjects',             'function':list_subjects },
        { 'description':'List all students by subjects', 'function':list_students_by_subjects }
    ]

    required_parameters = {
        'first_name': { 'name':'first name', 'type':'string', 'restrictions':[ 'non-empty' ] },\
        'last_name':  { 'name':'last name',  'type':'string', 'restrictions':[ 'non-empty' ] }, \
        'age':        { 'name':'age',        'type':'number', 'restrictions':[ 'integer', 'positive' ] }, \
        'gender':     { 'name':'gender',     'type':'string', 'restrictions':[ 'non-empty' ], 'options':[ 'male', 'female' ] } \
    }

def print_actions():
    action_num = 0
    for action in actions:
        print(f'{action_num}) {action[ "description" ]}')
        action_num += 1
    print()

def select_action():
    selected_action = input('Please select an action: ')

    if not action_is_valid(selected_action):
        print('Error: invalid action.\n')
        print_actions()
        return

    # NOTE: Call a function corresponding to a selected action.
    actions[ int(selected_action) ][ 'function' ]()

def action_is_valid(selected_action):
    is_valid = selected_action.isdigit() and int(selected_action)>=0 and int(selected_action)<=len(actions)

    if is_valid:
        return True
    else:
        return False

def add_student():
    student_parameters = {}

    for i_parameter in required_parameters:
        parameter = required_parameters[ i_parameter ]
        student_parameters[ i_parameter ] = prompt_parameter_until_valid(parameter)

    student = Student(student_parameters)
    Student.write_to_file(student)

def prompt_parameter_until_valid(parameter):
    entered_parameter = enter_parameter(parameter)
    while not parameter_is_valid(entered_parameter):
        entered_parameter = enter_parameter(parameter)

    return entered_parameter[ 'input_value' ]

def enter_parameter(parameter):
    input_prompt = "Please enter the student's " + parameter[ 'name' ]

    options = Null()
    has_options = 'options' in parameter and len(parameter[ 'options' ])>0
    if has_options:
        options = parameter[ 'options' ]
        input_prompt += list_parameter_options(options)

    input_value = input(input_prompt + ": ")

    entered_parameter = { 
        'input_value':input_value,\
        'type':parameter[ 'type' ],\
        'restrictions':parameter[ 'restrictions' ],\
        # WARNING: Can return None.
        'options':options
    }

    return entered_parameter

def list_parameter_options(options):
    options_list = ''
    for option in options:
        if len(options_list) > 0:
            options_list += (f", '{option}'")
        else:
            options_list += (f"'{option}'")

    input_prompt = ("; possible values are " + options_list)
    return input_prompt

def parameter_is_valid(entered_parameter):
    validation_result = Validator(entered_parameter)

    if validation_result.is_valid():
        return True
    else:
        print("Error: " + validation_result.error)

def list_students():
    raw_list_of_students = StudentList().get_raw_list_of_students()

    if list_of_students_is_empty(raw_list_of_students):
        print('There are no students in the list.')
        return
    else:
        print_each_student(raw_list_of_students)

def list_of_students_is_empty(students):
    if len(students) == 0:
        return True
    else:
        return False

def print_each_student(raw_list_of_students):
    student_num = 1
    for raw_student in raw_list_of_students:
        print(f'Student #{student_num}')

        print_student(raw_student)

        student_num += 1

def print_student(raw_student):
    parameter_num = 1

    str_raw_student_parameters = raw_student.split(', ')
    for str_raw_parameter in str_raw_student_parameters:
        print(f'{parameter_num}) ', end='')

        print_parameter(str_raw_parameter)

        parameter_num += 1

def print_parameter(str_raw_parameter):
    key_value_pair = str_raw_parameter.split(':')
    key = key_value_pair[ 0 ].replace('"', '')
    value = key_value_pair[ 1 ].replace('"', '')

    for req_parameter_key in required_parameters.keys():
        parameter_name = get_parameter_name_by_matching_keys(key, req_parameter_key)
        if not isinstance(parameter_name, Null):
            print_formatted_student_parameter(parameter_name, value)

def get_parameter_name_by_matching_keys(key, req_parameter_key):
    if key == req_parameter_key:
        parameter_name = required_parameters[ req_parameter_key ][ 'name' ].capitalize()
        return parameter_name
    else:
        # WONTFIX: this function is intended to be used only in
        # print_parameter(...), where there is a check for Null.
        return Null()

def print_formatted_student_parameter(parameter_name, parameter_value):
    print(f'{parameter_name}: {parameter_value}')

# TODO
def edit_student():
    pass

# TODO
def list_subjects():
    pass

# TODO
def list_students_by_subjects():
    pass

if __name__ == '__main__':
    # Logging
    lvl = logging.DEBUG 
    fmt = '%(lineno)s: [%(levelname)s] %(msg)s'
    logging.basicConfig(level = lvl, format = fmt)

    main()
