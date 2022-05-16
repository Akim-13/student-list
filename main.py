import logging

STUDENT_LIST_PATH = 'student_list.csv'

class StudentList():
    def __init__(self):
        with open(STUDENT_LIST_PATH, 'r') as student_list_csv:
            self.students = student_list_csv.readlines()


    def append_with(self, student):
        with open(STUDENT_LIST_PATH, 'a') as self.students:
            self.students.write(student)


    def get_the_list_of_students(self):
        with open(STUDENT_LIST_PATH, 'r') as student_list_csv:
            self.students = student_list_csv.readlines()
        return self.students


class Student():
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


def main():
    initialisation()
    print_actions()
    while True:
        select_action()


def initialisation():
    global students, required_parameters, actions
    students = []
    actions = [ 
        { 'description':'Quit',                          'function':quit },
        { 'description':'Add a new students',            'function':add_student },
        { 'description':'Edit an existing student',      'function':edit_student },               # TODO
        { 'description':'List all students',             'function':list_students },              # TODO
        { 'description':'List all subjects',             'function':list_subjects },              # TODO
        { 'description':'List all students by subjects', 'function':list_students_by_subjects }   # TODO
    ]

    required_parameters = {
        'first_name': { 'name':'first name', 'type':'string', 'restrictions':{ 'list':['non-empty' ] } },\
        'last_name':  { 'name':'last name',  'type':'string', 'restrictions':{ 'list':[ 'non-empty' ] } }, \
        'age':        { 'name':'age',        'type':'number', 'restrictions':{ 'list':[ 'integer', 'positive' ] } }, \
        'gender':     { 'name':'gender',     'type':'string', 'restrictions':{ 'list':[ 'non-empty' ], 'options':[ 'male', 'female' ] } } \
    }


def print_actions():
    cnt = 0
    for action in actions:
        print(f"{cnt}) {action['description']}")
        cnt += 1
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

    if len(students) == 0:
        print('There are no students in the list.')
        return


def list_subjects():
    pass


def list_students_by_subjects():
    pass


def prompt_parameter_until_valid(parameter):
    entered_parameter = enter_parameter(parameter)
    while not parameter_is_valid(entered_parameter):
        entered_parameter = enter_parameter(parameter)

    return entered_parameter[ 'input_value' ]


def enter_parameter(parameter):
    input_prompt = "Please enter the student's " + parameter[ 'name' ]
    restrictions = parameter[ 'restrictions' ]
    has_options = 'options' in restrictions and len(restrictions[ 'options' ]) > 0

    if has_options:
        input_prompt += list_parameter_options(restrictions)

    input_value = input(input_prompt + ": ")

    return { 
        'input_value':input_value,\
        'type':parameter[ 'type' ],\
        'restrictions':restrictions 
    }


def parameter_is_valid(entered_parameter):
    validation_result = validate_parameter(entered_parameter)

    if validation_result[ 'valid' ]:
        return True
    else:
        print( "Error: " + validation_result[ 'error' ] )


def list_parameter_options(restrictions):
    options_list = ''
    for option in restrictions[ 'options' ]:
        if len( options_list ) > 0:
            options_list += (f", '{option}'")
        else:
            options_list += (f"'{option}'")

    input_prompt = ( "; possible values are " + options_list )
    return input_prompt


def validate_parameter(entered_parameter):
    # TODO: clean up

    value = entered_parameter[ 'input_value' ]
    type = entered_parameter[ 'type' ]
    restrictions = entered_parameter[ 'restrictions' ]

    valid = True
    result = None
    error = ''
    
    if type == 'string':
        try:
            result = str(value)
        except:
            valid = False
            error = 'The value is not a string'
    elif type == 'number':
        try:
            result = float(value)
        except:
            valid = False
            error = 'The value is not a number'
    
    if result == None:
        valid = False
    
    if valid and 'list' in restrictions:
        for restriction in restrictions[ 'list' ]:
            if restriction == 'non-empty':
                if result == '':
                    valid = False
                    error = 'The value is empty'
            elif restriction == 'integer':
                try:
                    if result == int(result):
                        result = int(result)
                    else:
                        valid = False
                        error = 'The value is a number but not an integer'
                except:
                    valid = False
                    error = 'The value is not an integer'
            elif restriction == 'positive':
                if result <= 0:
                    valid = False
                    error = 'The value is not positive'
    
    if valid and 'options' in restrictions:
        value_found = False
        for option in restrictions[ 'options' ]:
            if option == result:
                value_found = True

        if not value_found:
            valid = False
            error = 'The value was not found in the list of valid options'

    return { 'valid': valid, 'result': result, 'error': error }


if __name__ == '__main__':
    # Logging
    lvl = logging.DEBUG 
    fmt = '%(lineno)s: [%(levelname)s] %(msg)s'
    logging.basicConfig(level = lvl, format = fmt)

    main()
