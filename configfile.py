import configparser

# TODO Make unnamed section on config file for introdutory comments

def ConfigFile():
    config_file = configparser.ConfigParser(allow_no_value=True)
    config_file.read('tasks.config')
    if config_file.sections() == []:
        print('Config file not found, creating tasks.config')
        config_file['DEFAULT'] = {
            '# These are the possible values for the config file':None,
            '# if you mess up, just delete the config file':None,
            '# and a new config file will be created the next time you run':None,
            '# the software':None,
            
            '# status_scope: (simple, in progress)':None,
            '# choose to have the "in progress" status (not yet supported)\n':None,
            
            '# table_align: (left, center, right)':None,
            '# choose the alignment of the printed tasks table (not yet supported)\n':None,
            
            '# subtasks: (true, false)':None,
            '# choose to have subtasks (not yet supported)\n':None,
            
            '# autosave: (true, false)':None,
            '# autosave before exiting when using program mode (not yet supported)\n':None,
            
            '# show: (all, current)': None,
            '# show all tasks in save file or just Todo/In Progress (not yet supported)\n':None,
            
            '# done_tasks: (keep, hide, delete)': None,
            '# keep, hide or delete tasks marked as To Do (not yet supported)\n':None,
            
            '# screen_clean: (true, false)': None,
            '# clean the screen after each command on program mode (not yet supported)\n':None,
            
            '# table_lines: (all, title, columns, rows)': None,
            '# which lines to show when drawing the tasks table (not yet supported)\n':None,
            
            '# extra_left_spacing: (0...)': None,
            '# add extra spacing on the left of tasks table cells (not yet supported)\n':None,
            
            '# extra_right_spacing: (0...)': None,
            '# add extra spacing on the right of tasks table cells (not yet supported)\n':None,
            
            '# save_file: (tasks.txt...)': None,
            '# custom save file name/directory (not yet supported)\n':None,
            
            'status_scope': 'simple',
            'table_align': 'left',
            'subtasks': 'false',
            'autosave': 'true',
            'show': 'all',
            'done_tasks': 'keep',
            'screen_clean': 'true',
            'table_lines': 'all',
            'extra_left_spacing': '0',
            'extra_right_spacing': '0',
            'save_file': 'tasks.txt'}

        config['CUSTOM'] = {
            'status_scope': 'simple',
            'table_align': 'left',
            'subtasks': 'false',
            'autosave': 'true',
            'show': 'all',
            'done_tasks': 'keep',
            'screen_clean': 'true',
            'table_lines': 'all',
            'extra_left_spacing': '0',
            'extra_right_spacing': '0',
            'save_file': 'tasks.txt'}
        
        with open('tasks.config', 'w') as configfile:
            config_file.write(configfile)

    config = {
        'status_scope': config_file['CUSTOM']['status_scope'],
        'table_align': config_file['CUSTOM']['table_align'],
        'subtasks': config_file['CUSTOM'].getboolean('subtasks'),
        'autosave': config_file['CUSTOM'].getboolean('autosave'),
        'show': config_file['CUSTOM']['show'],
        'done_tasks': config_file['CUSTOM']['done_tasks'],
        'screen_clean': config_file['CUSTOM'].getboolean('screen_clean'),
        'table_lines': config_file['CUSTOM']['table_lines'],
        'extra_left_spacing': config_file['CUSTOM'].getint('extra_left_spacing'),
        'extra_right_spacing': config_file['CUSTOM'].getint('extra_right_spacing'),
        'save_file': config_file['CUSTOM']['save_file']
    }
    
    return config