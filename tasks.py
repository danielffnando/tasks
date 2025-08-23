import numpy
import sys
import argparse

#task_array = numpy.array(['n','Task','Status'])
default_config = ['status_scope=simple',
                'table_align=left',
                'subtasks=false',
                'autosave=true',
                'show=all',
                'done_tasks=keep',
                'run_without_args=open',
                'screen_clean=true',
                'table_lines = all',
                'extra_left_spacing = 0',
                'extra_right_spacing = 0']
# TODO Options:
# Status: To Do, In Progress, Done// To Do, Done
# Table: Left align, centered, right align
# Sub tasks (1.1, 1.1.1, etc.)
# Autosave=(true,false)
# show=all, todo/in progress
# done tasks = keep, delete, archive (archive will give special index number, maybe a.1 or a1)
# run_without_args = open, open with new, list
# screen_clean = true, false
# table_lines = all, column, line, title
# extra_left_spacing = int()
# extra_right_spacing = int()

# Dealing with args

parser = argparse.ArgumentParser(
                    prog='Tasks',
                    description='A simple to-do list and task manager. '\
                                'Give no option '\
                                'to open cli interface.')

group = parser.add_mutually_exclusive_group()

group.add_argument('-l', help='list all tasks', action='store_true')
group.add_argument('-n', help='create a new task', nargs=1, metavar=('task_name'))
group.add_argument('-t', help='toggle task status', nargs=1, metavar=('task_id'))
group.add_argument('-r', help='rename a task', nargs=2,
                    metavar=('task_id', 'task_name'))
group.add_argument('-d', help='delete a task', nargs=1, metavar=('task_name'))
group.add_argument('-c', help='edit flags in tasks.config file', metavar=('FLAG=VALUE'))
options = vars(parser.parse_args())

arg_value = None
if options['l'] is not False:
    chosen_arg = 'l'
    arg_value = options['l']
    print(f'args.l, chosen_arg={chosen_arg}, arg_value={arg_value}')
if options['n'] is not None:
    chosen_arg = 'n'
    arg_value = options['n']
    print(f'args.n, chosen_arg={chosen_arg}, arg_value={arg_value}')
if options['t'] is not None:
    chosen_arg = 't'
    arg_value = options['t']
    print(f'args.t, chosen_arg={chosen_arg}, arg_value={arg_value}')
if options['r'] is not None:
    chosen_arg = 'r'
    arg_value = options['r']
    print(f'args.r, chosen_arg={chosen_arg}, arg_value={arg_value}')
if options['d'] is not None:
    chosen_arg = 'd'
    arg_value = options['d']
    print(f'args.d, chosen_arg={chosen_arg}, arg_value={arg_value}')
if options['c'] is not None:
    chosen_arg = 'c'
    arg_value = options['c']
    print(f'args.c, chosen_arg={chosen_arg}, arg_value={arg_value}')

# Classes for the program

class TaskFiles:
    @staticmethod
    def TaskFileLoad():
        try:
            array = numpy.loadtxt('tasks.txt', dtype='str', delimiter=',')
        except FileNotFoundError:
            print('Tasks file not found, creating new tasks file...')
            try:
                TaskFiles.TaskFileSave(numpy.array(['n','Task','Status']))
            except:
                print('Tasks file creation failed')
                sys.exit()
            else:
                print('New tasks file created')
        return array

    @staticmethod
    def TaskFileSave(array):
        try:
            numpy.savetxt('tasks.txt', array, delimiter=',', fmt='%s')
        except:
            print('Failed to save')

class TaskCommands:
    @staticmethod
    def TaskList(array):
        TaskTableDraw.TableDraw(array)

    @staticmethod
    def TaskNew(array):
        taskname = input('New task name: ')
        if taskname == '':
            return array
        array = numpy.vstack((array,['1970', taskname, 'To Do']))
        return array

    @staticmethod
    def TaskEdit(array):
        TaskCommands.TaskList(array)
        to_edit = input('Task to edit (Leave empty to return): ')
        try:
            to_edit = int(to_edit) # não está permitindo deixar vazio
        except:
            print('Please type the task index number')
            TaskCommands.TaskEdit(array)
        else: # TODO match case
            if to_edit == '': # use 'or' # não está chegando aqui por causa do try
                return array
            elif to_edit == 0:
                return array
            elif to_edit > numpy.shape(array)[0]-1:
                print('Please use an index number currently in use\n')
                TaskCommands.TaskEdit(array)
            else: # TODO match case
                to_change = input('Change task name or status?'\
                                    '(Leave empty to return): ')
                if to_change == 'name':
                    new_name = input('New task name: ')
                    array[to_edit][1] = new_name
                elif to_change == 'status':
                    new_status = input('New task status (done, todo): ')
                    array[to_edit][2] = new_status
                elif to_change == '':
                    TaskCommands.TaskEdit(array)
                else:
                    print('Please choose a valid option\n')
                    TaskCommands.TaskEdit(array)
        return array
    
    @staticmethod
    def TaskToggle(array):
        TaskCommands.TaskList(array)
        to_edit = input('Task to edit (Leave empty to return): ')
        try:
            to_edit = int(to_edit) # não está permitindo deixar vazio
        except:
            print('Please type the task index number')
            TaskCommands.TaskEdit(array)
        else: # TODO match case
            if to_edit == '': # use 'or' # não está chegando aqui por causa do try
                return array
            elif to_edit == 0:
                return array
            elif to_edit > numpy.shape(array)[0]-1:
                print('Please use an index number currently in use\n')
                TaskCommands.TaskEdit(array)
            else: # TODO match case
                to_change = input('Change task name or status?'\
                                    '(Leave empty to return): ')
                if to_change == 'name':
                    new_name = input('New task name: ')
                    array[to_edit][1] = new_name
                elif to_change == 'status':
                    new_status = input('New task status (done, todo): ')
                    array[to_edit][2] = new_status
                elif to_change == '':
                    TaskCommands.TaskEdit(array)
                else:
                    print('Please choose a valid option\n')
                    TaskCommands.TaskEdit(array)
        return array
    
    @staticmethod
    def TaskRename(array):
        TaskCommands.TaskList(array)
        to_edit = input('Task to edit (Leave empty to return): ')
        try:
            to_edit = int(to_edit) # não está permitindo deixar vazio
        except:
            print('Please type the task index number')
            TaskCommands.TaskEdit(array)
        else: # TODO match case
            if to_edit == '': # use 'or' # não está chegando aqui por causa do try
                return array
            elif to_edit == 0:
                return array
            elif to_edit > numpy.shape(array)[0]-1:
                print('Please use an index number currently in use\n')
                TaskCommands.TaskEdit(array)
            else: # TODO match case
                to_change = input('Change task name or status?'\
                                    '(Leave empty to return): ')
                if to_change == 'name':
                    new_name = input('New task name: ')
                    array[to_edit][1] = new_name
                elif to_change == 'status':
                    new_status = input('New task status (done, todo): ')
                    array[to_edit][2] = new_status
                elif to_change == '':
                    TaskCommands.TaskEdit(array)
                else:
                    print('Please choose a valid option\n')
                    TaskCommands.TaskEdit(array)
        return array
    
    @staticmethod
    def TaskDelete(array):
        TaskCommands.TaskList(array)
        try:
            to_delete = int(input('Task to delete (Leave empty to return): '))
        except:
            print('Please type the task index number\n')
            TaskDelete(array)
        else:
            if to_delete == '':
                return
            elif to_delete == 0:
                return
            elif to_delete > numpy.shape(array)[0]-1:
                print('Please use an index number currently in use\n')
                TaskDelete(array)
            else:
                array = numpy.delete(array,to_delete,axis=0)
            return array

class TaskUtils:
    @staticmethod
    def UpdateTasksIndexNumber(array):
        for i in range(numpy.shape(array)[0]):
            try:
                if array[i][0] != 'n' and array[i][0] != i:
                    array[i][0] = i
            except:
                break
        return array
        
class TaskTableDraw:
    @staticmethod
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

    @staticmethod
    def DrawDividingLine(size):
        to_print = '-' * size
        return to_print
        
    @staticmethod
    def PrintLineWithVerticalSpacer(array, longer_line):
        to_print = '|'
        for cell in range(numpy.shape(array)[0]):
            space_buffer_size = len(longer_line[cell]) - len(array[cell])
            space_buffer = ' ' * space_buffer_size
            to_print = to_print + array[cell] + space_buffer + '|'
        return to_print
    
    @staticmethod
    def TableDraw(array):
        try:
            number_table_row_column_cross = numpy.shape(array)[1] + 1
        except:
            number_table_row_column_cross = 4
        
        array_char_width = TaskTableDraw.ArrayCharWidth(array)[0]
        array_longer_line = TaskTableDraw.ArrayCharWidth(array)[1]
        row_size_padded = array_char_width\
                                        + number_table_row_column_cross
        table_column_num_char = numpy.shape(array)[0]
        
        print(TaskTableDraw.DrawDividingLine(row_size_padded))
        try:
            for line in range(0, table_column_num_char):
                print(TaskTableDraw.PrintLineWithVerticalSpacer(array[line],\
                                                        array_longer_line))
                print(TaskTableDraw.DrawDividingLine(row_size_padded))
        except IndexError:
            table_column_num_char = numpy.shape(array)[0]
            for line in range(0, table_column_num_char-2):
                print(TaskTableDraw.PrintLineWithVerticalSpacer(array,\
                                                        array_longer_line))
            
            print(TaskTableDraw.DrawDividingLine(row_size_padded))
        return

def Commands(array, option):
    loop = True
    match option:
        case 'List' | 'list' | 'l':
            TaskCommands.TaskList(array)
            return array, loop
        case 'New' | 'new' | 'n':
            array = TaskCommands.TaskNew(array)
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskCommands.TaskList(array)
            return array, loop
        case 'Edit' | 'edit' | 'e':
            array = TaskCommands.TaskEdit(array)
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskCommands.TaskList(array)
            return array, loop
        case 'Toggle' | 'toggle' | 't':
            array = TaskCommands.TaskToggle(array)
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskCommands.TaskList(array)
            return array, loop
        case 'Rename' | 'rename' | 'r':
            array = TaskCommands.TaskRename(array)
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskCommands.TaskList(array)
            return array, loop
        case 'Delete' | 'delete' | 'd':
            array = TaskCommands.TaskDelete(array)
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskCommands.TaskList(array)
            return array, loop
        case 'Config' | 'config' | 'c':
            print('Config not yet working')
            return array, loop
        # TODO add Undo: undo last edit
        # TODO add Save and exit: save current tasklist and exit
        # TODO add auto save when comm=ex: true, false
        # TODO add in program help
        case 'Save' | 'save' | 's':
            TaskFiles.TaskFileSave(array)
        case 'Exit' | 'exit' | 'ex':
            TaskFiles.TaskFileSave(array)
            loop = False
            return array, loop
        case _:
            return 'Please select an option'

def CliCommands(array, option):
    match option:
        case 'l': # List
            TaskCommands.TaskList(array)
        case 'n':
            # New
            array = TaskCommands.TaskNew(array)
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskFiles.TaskFileSave(array)
        case 'e':
            # Edit
            array = TaskCommands.TaskEdit(array)
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskFiles.TaskFileSave(array)
        case 't':
            # Toggle
            array = TaskCommands.TaskToggle(array)
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskFiles.TaskFileSave(array)
        case 'r':
            # Rename
            array = TaskCommands.TaskRename(array)
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskFiles.TaskFileSave(array)
        case 'd':
            # Delete
            array = TaskCommands.TaskDelete(array)
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskFiles.TaskFileSave(array)
        case 'c':
            # Config
            print('Config not yet working')

def main():
    task_array = TaskFiles.TaskFileLoad()
    loop = True
    while loop == True:
        task_array, loop = Commands(task_array, input('Type your option: '))

def cli(chosen_arg, arg_value):
    task_array = TaskFiles.TaskFileLoad()
    CliCommands(task_array, chosen_arg)

if __name__ == '__main__' and arg_value == None:
    print('we went with main')
    main()
else:
    print('we went with cli')
    cli(chosen_arg, arg_value)