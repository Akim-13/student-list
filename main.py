import logging
import sys

STUDENT_LIST_PATH = 'student_list.csv'

class StudentList():
    def get_the_list_of_students(self):
        with open(STUDENT_LIST_PATH, 'r') as student_list_csv:
            self.students = student_list_csv.readlines()
        return self.students

    def append_with(self, student):
        with open(STUDENT_LIST_PATH, 'a') as self.students:
            self.students.write(student)

class Student():
    # TODO: still needs to be done dynamically
    def __init__(self, parameters):
        self.parameters = parameters

    def append_to_file(self):
        student_in_csv_format = Student.get_in_csv_format(self)
        StudentList().append_with(student_in_csv_format)

    def get_in_csv_format(self):
        student_in_csv_format = ''

        i = 1
        for parameter_value in self.parameters.values():
            is_last_iteration = i==len(self.parameters)
            student_in_csv_format += Student.get_parameter_value_with_delimiter(self, parameter_value, is_last_iteration)
            i += 1

        return student_in_csv_format

    def get_parameter_value_with_delimiter(self, parameter_value, is_last_iteration):
        if is_last_iteration:
            return parameter_value + '\n'
        else:
            return parameter_value + ', '

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
        Validator.validate_by_type(self)

        if self.valid:
            has_restrictions = self.restrictions
            if has_restrictions:
                Validator.validate_restrictions(self)

            has_options = self.options
            if has_options:
                Validator.validate_options(self)

        return self.valid

    def validate_by_type(self):
        if self.type == 'string':
            Validator.validate_string(self)
        elif self.type == 'number': 
            Validator.validate_number(self)
        else:
            sys.exit('ERROR: Unknown parameter type.')

    def validate_string(self):
        # Any user input can be converted to string, so just return it.
        self.result = str(self.value)
        self.valid = True

    def validate_number(self):
        try:
            self.result = float(self.value)
            self.valid = True
        except ValueError:
            self.error = 'The value is not a number.'
            self.valid = False

    def validate_restrictions(self):
        for restriction in self.restrictions:
            if restriction == 'non-empty':
                Validator.validate_non_empty_restriction(self, restriction)

            elif restriction == 'integer':
                Validator.validate_integer_restriction(self)

            elif restriction == 'positive':
                Validator.validate_positive_restriction(self, restriction)

            else:
                return

    def validate_non_empty_restriction(self, restriction):
        try:
            Validator.check_if_empty(self, self.result)
        except:
            Validator.exit_with_error_invalid_restriction(self, restriction)

    def check_if_empty(self, result):
        if result == '':
            self.error = 'The value is empty.'
            self.valid = False

    def exit_with_error_invalid_restriction(self, restriction):
        sys.exit(f'ERROR: invalid restriction {restriction} for type {self.type}')

    def validate_integer_restriction(self):
        try:
            Validator.check_if_integer(self, self.result)
        except:
            self.error = 'The value is not an integer.'
            self.valid = False

    def check_if_integer(self, result):
        if result == int(result):
            self.result = int(result)
        else:
            self.error = 'The value is a number but not an integer.'
            self.valid = False

    def validate_positive_restriction(self, restriction):
        try:
            Validator.check_if_positive(self, self.result)
        except:
            Validator.exit_with_error_invalid_restriction(self, restriction)

    def check_if_positive(self, result):
        if result <= 0:
            self.valid = False
            self.error = 'The value is not positive'

    def validate_options(self):
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
        { 'description':'Edit an existing student',      'function':edit_student },               # TODO
        { 'description':'List all students',             'function':list_students },
        { 'description':'List all subjects',             'function':list_subjects },              # TODO
        { 'description':'List all students by subjects', 'function':list_students_by_subjects }   # TODO
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

    # Call a function corresponding to a selected action.
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
    Student.append_to_file(student)

def edit_student():
    pass

def list_students():
    students = StudentList().get_the_list_of_students()

    if list_of_students_is_empty(students):
        print('There are no students in the list.')
        return
    else:
        print_each_students(students)

def list_subjects():
    pass

def list_students_by_subjects():
    pass

def list_of_students_is_empty(students):
    if len(students) == 0:
        return True
    else:
        return False

def print_each_students(students):
    student_num = 1
    for student in students:
        print(f'Student #{student_num}')

        values_of_student_parameters = student.split(', ')
        print_each_parameter(values_of_student_parameters)

        student_num += 1

def print_each_parameter(values_of_student_parameters):
    i = 0
    for parameter in required_parameters:
        parameter_name = required_parameters[ parameter ][ 'name' ].capitalize()
        print_formatted_student_parameter(parameter_name, values_of_student_parameters[ i ], i)
        i += 1

def print_formatted_student_parameter(parameter_name, parameter_value, current_iteration):
    parameter_num = current_iteration + 1
    print(f'{parameter_num}. {parameter_name}: {parameter_value}')

def prompt_parameter_until_valid(parameter):
    entered_parameter = enter_parameter(parameter)
    while not parameter_is_valid(entered_parameter):
        entered_parameter = enter_parameter(parameter)

    return entered_parameter[ 'input_value' ]

def enter_parameter(parameter):
    input_prompt = "Please enter the student's " + parameter[ 'name' ]

    options = None
    has_options = 'options' in parameter and len(parameter[ 'options' ])>0
    if has_options:
        options = parameter[ 'options' ]
        input_prompt += list_parameter_options(options)

    input_value = input(input_prompt + ": ")

    entered_parameter = { 
        'input_value':input_value,\
        'type':parameter[ 'type' ],\
        'restrictions': parameter[ 'restrictions' ],\
        'options':options
    }

    return entered_parameter

def parameter_is_valid(entered_parameter):
    validation_result = Validator(entered_parameter)

    if validation_result.is_valid():
        return True
    else:
        print("Error: " + validation_result.error)

def list_parameter_options(options):
    options_list = ''
    for option in options:
        if len(options_list) > 0:
            options_list += (f", '{option}'")
        else:
            options_list += (f"'{option}'")

    input_prompt = ("; possible values are " + options_list)
    return input_prompt

if __name__ == '__main__':
    # Logging
    lvl = logging.DEBUG 
    fmt = '%(lineno)s: [%(levelname)s] %(msg)s'
    logging.basicConfig(level = lvl, format = fmt)

    main()
