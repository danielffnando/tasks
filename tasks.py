import numpy
import sys

tasknum=1
taskarray = numpy.array(['n','Task','Status'])

def TasksFileLoad():
    global taskarray
    try:
        taskarray = numpy.loadtxt('tasks.txt', dtype='str', delimiter=',')
    except:
        print('Tasks file not found, creating new tasks file...')
        try:
            TasksFileSave()
        except:
            print('Tasks file creation failed')
            sys.exit()
        else:
            print('New tasks file created')
            
def TasksFileSave():
    try:
        numpy.savetxt('tasks.txt', taskarray, delimiter=',', fmt='%s')
    except:
        print('Failed to save')

def TaskList():
    #print(taskarray,"\n")
    TableDraw()

def TaskNew():
    global taskarray
    global tasknum
    taskname = input('New task name: ')
    taskarray = numpy.vstack((taskarray,[tasknum, taskname, 'todo']))
    tasknum += 1

def TaskEdit():
    global taskarray
    TaskList()
    try:
        to_edit = int(input('Task to edit ("0" to return): '))
    except:
        print('Please type the task index number')
        TaskEdit()
    else:
        if to_edit == 0:
            return
        elif to_edit > numpy.shape(taskarray)[0]-1:
            print('Please use an index number corrently in use\n')
            TaskEdit()
        else:
            to_change = input('Change task name or status? "back" to return): ')
            if to_change == 'name':
                new_name = input('New task name: ')
                taskarray[to_edit][1] = new_name
            elif to_change == 'status':
                new_status = input('New task status (done, todo): ')
                taskarray[to_edit][2] = new_status
            elif to_change == 'back':
                print('potato')
                TaskEdit()
            else:
                print('Please choose a valid option\n')
                TaskEdit()
                
def TaskDelete():
    global taskarray
    TaskList()
    try:
        to_delete = int(input('Task to delete ("0" to return): '))
    except:
        print('Please type the task index number\n')
        TaskDelete()
    else:
        if to_delete == 0:
            return
        elif to_delete > numpy.shape(taskarray)[0]-1:
            print('Please use an index number corrently in use\n')
            TaskDelete()
        else:
            taskarray = numpy.delete(taskarray,to_delete,axis=0)

def Commands(comm):
    match comm:
        case 'List' | 'list' | 'l':
            TaskList()
        case 'New' | 'new' | 'n':
            TaskNew()
            UpdateTasksIndexNumber()
            TaskList()
        case 'Edit' | 'edit' | 'e':
            TaskEdit()
            UpdateTasksIndexNumber()
            TaskList()
        case 'Delete' | 'delete' | 'd':
            TaskDelete()
            UpdateTasksIndexNumber()
            TaskList()
        case 'Exit' | 'exit' | 'ex':
            sys.exit()
        case _:
            return 'Please select an option'

def UpdateTasksIndexNumber():
    global taskarray
    for i in range(numpy.shape(taskarray)[0]):
        try:
            if taskarray[i][0] != 'n' and taskarray[i][0] != i:
                taskarray[i][0] = i
        except:
            break
        
def ArrayCharWidth(array):
    table_line_size = 0
    longer_line = []
    try:
        for col in range(numpy.shape(array)[1]):
            longer_line.append(max(array[:, col], key=len))
    except IndexError:
        longer_line = array
    table_line_size = 0
    for i in range(len(longer_line)):
        table_line_size = table_line_size + len(longer_line[i])
    return table_line_size, longer_line

def DrawDividingLine(size):
    to_print = '-' * size
    return to_print
    
def PrintLineWithVerticalSpacer(array, longer_line):
    to_print = '|'
    for cell in range(numpy.shape(array)[0]):
        space_buffer_size = len(longer_line[cell]) - len(array[cell])
        space_buffer = ' ' * space_buffer_size
        to_print = to_print + array[cell] + space_buffer + '|'
    return to_print

def TableDraw():
    try:
        number_table_row_column_cross = numpy.shape(taskarray)[1] + 1
    except:
        number_table_row_column_cross = 4
    
    array_char_width = ArrayCharWidth(taskarray)[0]
    array_longer_line = ArrayCharWidth(taskarray)[1]
    table_row_num_char_with_spacer = array_char_width + number_table_row_column_cross
    table_column_num_char = numpy.shape(taskarray)[0]
    
    print(DrawDividingLine(table_row_num_char_with_spacer))
    try:
        for line in range(0, table_column_num_char):
            print(PrintLineWithVerticalSpacer(taskarray[line], array_longer_line))
    except IndexError:
        table_column_num_char = numpy.shape(taskarray)[0]
        for line in range(0, table_column_num_char-2):
            print(PrintLineWithVerticalSpacer(taskarray, array_longer_line))
    print(DrawDividingLine(table_row_num_char_with_spacer))

while 'true':
    TasksFileLoad()
    inp = input('Type your option: ')
    Commands(inp)
    TasksFileSave()