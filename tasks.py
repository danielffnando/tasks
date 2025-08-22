import numpy
import sys
import configparser

task_array = numpy.array(['n','Task','Status'])
task_config = configparser.ConfigParser()
loop = True
defaut_config = ['status_scope=simple',
                 'table_align=left',
                 'subtasks=false',
                 'autosave=true',
                 'show=all',
                 'done_tasks=keep',
                 'run_withou_args=open',
                 'screen_clean=true']
# TODO Options:
# Status: To Do, In Progress, Done// To Do, Done
# Table: Left align, centered, right align
# Sub tasks (1.1, 1.1.1, etc)
# Autosave=(true,false)
# show=all, todo/in prongress
# done tasks = keep, delete, archive (archive will give special index numeber, maybe a.1 or a1)
# run_withou_args = open, open with new, list
# screen_clean = true, false


class TaskFiles:
    def TaskFileLoad(): # TODO 'self'
        global task_array
        try:
            task_array = numpy.loadtxt('tasks.txt', dtype='str', delimiter=',')
        except FileNotFoundError:
            print('Tasks file not found, creating new tasks file...')
            try:
                TaskFiles.TaskFileSave()
            except:
                print('Tasks file creation failed')
                sys.exit()
            else:
                print('New tasks file created')
                
    def TaskFileSave():
        try:
            numpy.savetxt('tasks.txt', task_array, delimiter=',', fmt='%s')
        except:
            print('Failed to save')

class TaskCommands:
    def TaskList():
        TaskTableDraw.TableDraw()

    def TaskNew(): # TODO 'self'
        global task_array
        taskname = input('New task name: ')
        if taskname == '':
            return
        task_array = numpy.vstack((task_array,['1970', taskname, 'To Do']))

    def TaskEdit(): # TODO 'self'
        global task_array
        TaskCommands.TaskList()
        try:
            to_edit = int(input('Task to edit (leave empty to return): '))
        except:
            print('Please type the task index number')
            TaskCommands.TaskEdit()
        else: # TODO match case
            if to_edit == '':
                return
            elif to_edit == 0:
                return
            elif to_edit > numpy.shape(task_array)[0]-1:
                print('Please use an index number corrently in use\n')
                TaskCommands.TaskEdit()
            else: # TODO match case
                to_change = input('Change task name or status? (Leave empty to return): ')
                if to_change == 'name':
                    new_name = input('New task name: ')
                    task_array[to_edit][1] = new_name
                elif to_change == 'status':
                    new_status = input('New task status (done, todo): ')
                    task_array[to_edit][2] = new_status
                elif to_change == '':
                    TaskCommands.TaskEdit()
                else:
                    print('Please choose a valid option\n')
                    TaskCommands.TaskEdit()
                    
    def TaskDelete(): # TODO 'self'
        global task_array
        TaskCommands.TaskList()
        try:
            to_delete = int(input('Task to delete (Leave empty to return): '))
        except:
            print('Please type the task index number\n')
            TaskDelete()
        else:
            if to_delete == '':
                return
            elif to_delete == 0:
                return
            elif to_delete > numpy.shape(task_array)[0]-1:
                print('Please use an index number corrently in use\n')
                TaskDelete()
            else:
                task_array = numpy.delete(task_array,to_delete,axis=0)

class TaskUtils:
    def UpdateTasksIndexNumber(): # TODO 'self'
        global task_array
        for i in range(numpy.shape(task_array)[0]):
            try:
                if task_array[i][0] != 'n' and task_array[i][0] != i:
                    task_array[i][0] = i
            except:
                break
        
class TaskTableDraw:
    def ArrayCharWidth(array): # TODO 'self'
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

    def DrawDividingLine(size): # TODO 'self'
        to_print = '-' * size
        return to_print
        
    def PrintLineWithVerticalSpacer(array, longer_line): # TODO 'self'
        to_print = '|'
        for cell in range(numpy.shape(array)[0]):
            space_buffer_size = len(longer_line[cell]) - len(array[cell])
            space_buffer = ' ' * space_buffer_size
            to_print = to_print + array[cell] + space_buffer + '|'
        return to_print

    def TableDraw(): # TODO 'self'
        try:
            number_table_row_column_cross = numpy.shape(task_array)[1] + 1
        except:
            number_table_row_column_cross = 4
        
        array_char_width = TaskTableDraw.ArrayCharWidth(task_array)[0]
        array_longer_line = TaskTableDraw.ArrayCharWidth(task_array)[1]
        table_row_num_char_with_spacer = array_char_width + number_table_row_column_cross
        table_column_num_char = numpy.shape(task_array)[0]
        
        print(TaskTableDraw.DrawDividingLine(table_row_num_char_with_spacer))
        try:
            for line in range(0, table_column_num_char):
                print(TaskTableDraw.PrintLineWithVerticalSpacer(task_array[line], array_longer_line))
                print(TaskTableDraw.DrawDividingLine(table_row_num_char_with_spacer))
        except IndexError:
            table_column_num_char = numpy.shape(task_array)[0]
            for line in range(0, table_column_num_char-2):
                print(TaskTableDraw.PrintLineWithVerticalSpacer(task_array, array_longer_line))
#        print(TaskTableDraw.DrawDividingLine(table_row_num_char_with_spacer))


def Commands(comm): # TODO 'self'
    global loop
    match comm:
        case 'List' | 'list' | 'l':
            TaskCommands.TaskList()
        case 'New' | 'new' | 'n':
            TaskCommands.TaskNew()
            TaskUtils.UpdateTasksIndexNumber()
            TaskCommands.TaskList()
        case 'Edit' | 'edit' | 'e':
            TaskCommands.TaskEdit()
            TaskUtils.UpdateTasksIndexNumber()
            TaskCommands.TaskList()
        case 'Delete' | 'delete' | 'd':
            TaskCommands.TaskDelete()
            TaskUtils.UpdateTasksIndexNumber()
            TaskCommands.TaskList()
        # TODO Undo: undo last edit
        # TODO Config: edit program options
        # TODO Save: save current tasklist
        # TODO Save and exit: save current tasklist and exit
        # TODO auto save when comm=ex: true, false
        case 'Save' | 'save' | 's':
            TaskFiles.TaskFileSave()
        case 'Exit' | 'exit' | 'ex':
            TaskFiles.TaskFileSave()
            loop = False
        case _:
            return 'Please select an option'
        
def main():
    TaskFiles.TaskFileLoad()
    while loop == True:
        Commands(input('Type your option: '))

if __name__ == '__main__':

    main()
