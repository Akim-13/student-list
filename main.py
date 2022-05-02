import logging

class Student():
    def __init__(self, parameters):
        self.first_name = parameters['first name']
        self.last_name = parameters['last name']
        self.age = parameters['age']
        self.gender = parameters['gender']


def action_is_valid(selected_action):
    if selected_action.isdigit()\
       and int(selected_action) > 0\
       and int(selected_action) <= len(actions):
        return True
    else:
        return False


def select_action():
    selected_action = input('Please select an action: ')
    if not action_is_valid(selected_action):
        print('Error: invalid action.\n')
        print_actions()
        return
    selected_action = int(selected_action) - 1

    actions[selected_action]['function']()

def validate_parameter( value, type, restrictions ):
    # TODO: clean up
    valid = True
    result = None
    error = ''
    
    if type == 'string':
        try:
            result = str( value )
        except:
            valid = False
            error = 'The value is not a string'
    elif type == 'number':
        try:
            result = float( value )
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
                    if result == int( result ):
                        result = int( result )
                    # Why? Isn't except enough?
                    else:
                        valid = False
                        error = 'The value is not an integer'
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


def add_student():
    # TODO: clean up
    student_parameters = {}
    for parameter in required_parameters:
        current_result_valid = False
        while not current_result_valid:
            input_prompt = "Please enter the student's " + required_parameters[ parameter ][ 'name' ]
            # Why do we need to check the lenght?
            if 'options' in required_parameters[ parameter ][ 'restrictions' ] and len( required_parameters[ parameter ][ 'restrictions' ][ 'options' ] ) > 0:
                options_list = ''
                for option in required_parameters[ parameter ][ 'restrictions' ][ 'options' ]:
                    if len( options_list ) > 0:
                        options_list += (f", '{option}'")
                    else:
                        options_list += (f"'{option}'")
                input_prompt += ( "; possible values are " + options_list )

            input_value = input( input_prompt + ": " )
            validation_result = validate_parameter( input_value, required_parameters[ parameter ][ 'type' ], required_parameters[ parameter ][ 'restrictions' ] )
            if validation_result[ 'valid' ]:
                current_result_valid = True
                student_parameters[required_parameters[parameter]['name']] = input_value
            else:
                print( "Error: " + validation_result[ 'error' ] )
    #logging.debug(f'Student parameters: {student_parameters}')
    student = Student(student_parameters)
    students.append(student)
    
def edit_student():
    pass
        
def list_students():
    print(students)
    
def list_subjects():
    pass

def list_students_by_subjects():
    pass


def print_actions():
    cnt = 1
    for action in actions:
        print(f"{cnt}) {action['description']}")
        cnt += 1
    print()

def initialisation():
    global students, required_parameters, actions
    students = []
    actions = [ { 'description':'Add a new students',            'function':add_student },
                { 'description':'Edit an existing student',      'function':edit_student },               # TODO
                { 'description':'List all students',             'function':list_students },
                { 'description':'List all subjects',             'function':list_subjects },              # TODO
                { 'description':'List all students by subjects', 'function':list_students_by_subjects },  # TODO
                { 'description':'Quit',                          'function':quit }
              ]

    required_parameters = { 'first_name': { 'name': 'first name', 'type': 'string', 'restrictions': { 'list': ['non-empty' ] } },\
                            'last_name': { 'name': 'last name', 'type': 'string', 'restrictions': { 'list': [ 'non-empty' ] } }, \
                            'age': { 'name': 'age', 'type': 'number', 'restrictions': { 'list': [ 'integer', 'positive' ] } }, \
                            'gender': { 'name': 'gender', 'type': 'string', 'restrictions': { 'list': [ 'non-empty' ], 'options': [ 'male', 'female' ] } } \
                          }

def main():
    initialisation()
    print_actions()
    while True:
        select_action()

    
if __name__ == '__main__':
    # Logging
    lvl = logging.DEBUG 
    fmt = '%(lineno)s: [%(levelname)s] %(msg)s'
    logging.basicConfig(level = lvl, format = fmt)

    main()

