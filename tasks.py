import numpy
import sys
import configparser

#task_array = numpy.array(['n','Task','Status'])
task_config = configparser.ConfigParser()
loop = True
default_config = ['status_scope=simple',
                 'table_align=left',
                 'subtasks=false',
                 'autosave=true',
                 'show=all',
                 'done_tasks=keep',
                 'run_without_args=open',
                 'screen_clean=true']
# TODO Options:
# Status: To Do, In Progress, Done// To Do, Done
# Table: Left align, centered, right align
# Sub tasks (1.1, 1.1.1, etc.)
# Autosave=(true,false)
# show=all, todo/in progress
# done tasks = keep, delete, archive (archive will give special index number, maybe a.1 or a1)
# run_without_args = open, open with new, list
# screen_clean = true, false


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
        try:
            to_edit = int(input('Task to edit (leave empty to return): '))
        except:
            print('Please type the task index number')
            TaskCommands.TaskEdit(array)
        else: # TODO match case
            if to_edit == '': # use 'or'
                return array
            elif to_edit == 0:
                return array
            elif to_edit > numpy.shape(array)[0]-1:
                print('Please use an index number currently in use\n')
                TaskCommands.TaskEdit(array)
            else: # TODO match case
                to_change = input('Change task name or status? (Leave empty to return): ')
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
        table_row_num_char_with_spacer = array_char_width + number_table_row_column_cross
        table_column_num_char = numpy.shape(array)[0]
        
        print(TaskTableDraw.DrawDividingLine(table_row_num_char_with_spacer))
        try:
            for line in range(0, table_column_num_char):
                print(TaskTableDraw.PrintLineWithVerticalSpacer(array[line], array_longer_line))
                print(TaskTableDraw.DrawDividingLine(table_row_num_char_with_spacer))
        except IndexError:
            table_column_num_char = numpy.shape(array)[0]
            for line in range(0, table_column_num_char-2):
                print(TaskTableDraw.PrintLineWithVerticalSpacer(array, array_longer_line))
            
            print(TaskTableDraw.DrawDividingLine(table_row_num_char_with_spacer))
        return

def main():
    task_array = TaskFiles.TaskFileLoad()
    loop = True
    while loop == True:
        match input('Type your option: '):
            case 'List' | 'list' | 'l':
                TaskCommands.TaskList(task_array)
            case 'New' | 'new' | 'n':
                task_array = TaskCommands.TaskNew(task_array)
                task_array = TaskUtils.UpdateTasksIndexNumber(task_array)
                TaskCommands.TaskList(task_array)
            case 'Edit' | 'edit' | 'e':
                task_array = TaskCommands.TaskEdit(task_array)
                task_array = TaskUtils.UpdateTasksIndexNumber(task_array)
                TaskCommands.TaskList(task_array)
            case 'Delete' | 'delete' | 'd':
                task_array = TaskCommands.TaskDelete(task_array)
                task_array = TaskUtils.UpdateTasksIndexNumber(task_array)
                TaskCommands.TaskList(task_array)
            # TODO Undo: undo last edit
            # TODO Config: edit program options
            # TODO Save: save current tasklist
            # TODO Save and exit: save current tasklist and exit
            # TODO auto save when comm=ex: true, false
            case 'Save' | 'save' | 's':
                TaskFiles.TaskFileSave(task_array)
            case 'Exit' | 'exit' | 'ex':
                TaskFiles.TaskFileSave(task_array)
                loop = False
            case _:
                return 'Please select an option'

if __name__ == '__main__':
    main()