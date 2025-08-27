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
                'table_lines=all',
                'extra_left_spacing=0',
                'extra_right_spacing=0',
                'save_file=tasks.txt']
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
# tasks file name

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
if options['n'] is not None:
    chosen_arg = 'n'
    arg_value = options['n']
if options['t'] is not None:
    chosen_arg = 't'
    arg_value = options['t']
if options['r'] is not None:
    chosen_arg = 'r'
    arg_value = options['r']
if options['d'] is not None:
    chosen_arg = 'd'
    arg_value = options['d']
if options['c'] is not None:
    chosen_arg = 'c'
    arg_value = options['c']

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
            except Exception as error:
                print('Tasks file creation failed:', error)
                sys.exit()
            else:
                print('New tasks file created')
        return array

    @staticmethod
    def TaskFileSave(array):
        try:
            numpy.savetxt('tasks.txt', array, delimiter=',', fmt='%s')
        except Exception as error:
            print('Failed to save:', error)

class TaskCommands:
    @staticmethod
    def TaskList(array):
        TaskTableDraw.TableDraw(array)

    @staticmethod
    def TaskNew(array, name):
        if name == '':
            return array
        array = numpy.vstack((array,['1970', name, 'To Do']))
        return array
    
    @staticmethod
    def TaskToggle(array, to_edit):
        try:
            to_edit = int(to_edit)
        except:
            print('Please type the task index number')
            return array
        else:
            if to_edit > numpy.shape(array)[0]-1:
                print('Please use an index number currently in use\n')
                return array
            else:
                if array[to_edit][2] == 'To Do':
                    array[to_edit][2] = 'Done'
                elif array[to_edit][2] == 'Done':
                    array[to_edit][2] = 'To do'
                else:
                    print('Something when wrong with toggle')
                    return array
        return array
    
    @staticmethod
    def TaskRename(array, to_edit, new_name):
        try:
            to_edit = int(to_edit)
        except ValueError:
            print('Please type a valid task index number')
        else:
            if to_edit > numpy.shape(array)[0]-1:
                print('Please use an index number currently in use\n')
                return array
            elif new_name == '':
                return array
            else:
                array[to_edit][1] = new_name
        return array
    
    @staticmethod
    def TaskDelete(array, to_delete):
        try:
            to_delete = int(to_delete)
        except ValueError:
            print('Please type the task index number\n')
            return array
        else:
            if to_delete > numpy.shape(array)[0]-1:
                print('Please use an index number currently in use\n')
                return array
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
            array = TaskCommands.TaskNew(array, input('New task name: '))
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskCommands.TaskList(array)
            return array, loop
        case 'Toggle' | 'toggle' | 't':
            array = TaskCommands.TaskToggle(array,
                        input('Task to toggle (Leave empty to return): '))
            TaskCommands.TaskList(array)
            return array, loop
        case 'Rename' | 'rename' | 'r':
            array = TaskCommands.TaskRename(array,
                        input('Task to rename (Leave empty to return): '),
                        input('Task to new name (Leave empty to return): '))
            TaskCommands.TaskList(array)
            return array, loop
        case 'Delete' | 'delete' | 'd':
            array = TaskCommands.TaskDelete(array,
                        input('Task to delete (Leave empty to return): '))
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
        case 'Help' | 'help' | 'h' | '-h' | '--help' | 'options':
            print('A simple to-do list and task manager.\n\n'\
                    'options:\n'\
                    '   h, help         show this help message\n'\
                    '   l, list         list all tasks\n'\
                    '   n, new          create a new task\n'\
                    '   t, toggle       toggle task status\n'\
                    '   r, rename       rename a task\n'\
                    '   d, delete       delete a task\n'\
                    '   c, config       edit flags in tasks.config file\n')
            return array, loop
        case _:
            return 'Please select an option'

def CliCommands(array, option, args):
    match option:
        case 'l': # List
            TaskCommands.TaskList(array)
        case 'n': # New
            array = TaskCommands.TaskNew(array, args[0])
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskFiles.TaskFileSave(array)
        case 't': # Toggle
            array = TaskCommands.TaskToggle(array, args[0])
            TaskFiles.TaskFileSave(array)
        case 'r': # Rename
            array = TaskCommands.TaskRename(array, args[0], args[1])
            TaskFiles.TaskFileSave(array)
        case 'd': # Delete
            array = TaskCommands.TaskDelete(array, args)
            array = TaskUtils.UpdateTasksIndexNumber(array)
            TaskFiles.TaskFileSave(array)
        case 'c':
            # Config
            print('Config still in development')

def main():
    task_array = TaskFiles.TaskFileLoad()
    loop = True
    while loop == True:
        task_array, loop = Commands(task_array, input('Type your option: '))

def cli(chosen_arg, arg_value):
    task_array = TaskFiles.TaskFileLoad()
    CliCommands(task_array, chosen_arg, arg_value)

if __name__ == '__main__' and arg_value == None:
    main()
else:
    cli(chosen_arg, arg_value)