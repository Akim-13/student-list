import logging

NUM_OF_OPTS = 5

class Student():
    def __init__(self, parameters):  # TODO: subjects
        if 'first_name' in parameters:
            self.first_name = parameters[ 'first_name' ]
        else:
            print( "ERROR" )
            # insert error handling here

        self.last_name = parameters[ 'last_name' ]
        self.age = parameters[ 'age' ]
        self.gender = parameters[ 'gender' ]

def opt_is_valid(inp):
    isValid = False
    for i in range(NUM_OF_OPTS):
        if inp.isdigit() and int(inp) == i + 1 or inp == 'q':
            isValid = True
    return isValid


def no_exceptions(inp):
    if not opt_is_valid(inp):
        print('The option is invalid!')
        return False
    if inp == 'q':
        return False
    return True


def create_student():
        first_name = input('Enter the first name of the student: ')
        last_name = input('Enter the last name of the student: ')

        age = input('Enter the age of the student: ')
        if not age.isdigit():
            print('Incorrect age.')
            return

        gender = input('[M]ale or [F]emale:')
        if gender.lower() == 'm':
            gender = "Male"
        elif gender.lower() == 'f':
            gender = 'Female'
        else:
            print('Incorrect gender.')
            return

        parameters = { 'first_name':first_name,\
                       'last_name':last_name,\
                       'age':age,\
                       'gender':gender }

        students.append(Student(parameters))
        print(students)

def print_all_students():
    cnt = 1
    for student in students:
        print(f'{cnt})',
              f'First name: {student.first_name}',
              f'Last name: {student.last_name}',
              f'Age: {student.age}',
              f'Gender: {student.gender}')
        cnt += 1

def sel_opt(inp):
    if not no_exceptions(inp):
        return

    opt = int(inp)

    # Not scalable solution
    if opt == 1:
        create_student()
    elif opt == 2:
        print_all_students()
        student_to_edit = input('Please choose a students to edit: ')
        param_to_edit = None
        while param_to_edit != 'q':
            print('1) First name\n'
                  '2) Last name\n'
                  '3) Age \n'
                  '4) Gender\n'
                  'Enter q to quit.\n')
            param_to_edit = input('Please choose an option to edit: ')
            value = input('Enter a new value: ')
            if 
            students[student_to_edit - 1]
            
    elif opt == 3:
        print_all_students()
    elif opt == 4:
        pass
    elif opt == 5:
        pass


def input_loop(inp):
    while inp != 'q':
        sel_opt(inp)
        inp = input('Enter an option: ')


def print_opts():
    print('1) Add a new student\n'
          '2) Edit an existing student\n'
          '3) List all students\n'
          '4) List all subjects\n'
          '5) List all students by subjects\n\n'
          'Enter q to quit.\n')


def main():
    global students, subjects
    students = []
    subjects = []
    print_opts()
    input_loop(input('Enter an option: '))

    
if __name__ == '__main__':
    # Logging
    lvl = logging.DEBUG 
    fmt = '%(lineno)s: [%(levelname)s] %(msg)s'
    logging.basicConfig(level = lvl, format = fmt)

    main()

