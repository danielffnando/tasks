import numpy

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

def TableDraw(array, config, theme):
    try:
        table_num_of_cols = numpy.shape(array)[1] * 2 + 1
        table_num_of_rows = numpy.shape(array)[0] * 2 + 1
    except IndexError:
        table_num_of_cols = len(array) * 2 + 1
        table_num_of_rows = 1 * 2 + 1
    try:
        array_num_of_cols = numpy.shape(array)[1]
        array_num_of_rows = numpy.shape(array)[0]
    except IndexError:
        array_num_of_cols = len(array)
        array_num_of_rows = 1

    array_row = 0
    array_col = 0

    to_print = []
    longer_table_row = ArrayCharWidth(array)[1]

    for table_row in range(table_num_of_rows):
        if table_row == 0:
            # first table row
            i = 0
            for table_col in range(table_num_of_cols):
                if table_col % 2 == 0:
                    if table_col == 0:
                        # first table col
                        to_print.append(theme['top_left_corner'])
                    elif table_col == table_num_of_cols - 1:
                        # last table col
                        to_print.append(theme['top_right_corner'])
                        to_print.append('\n')
                    else:
                        to_print.append(theme['top_cross'])
                elif table_col % 2 == 1:
                    to_print.append(theme['hline_border'] * config['extra_left_spacing'])
                    to_print.append(theme['hline_border'] * len(longer_table_row[i]))
                    to_print.append(theme['hline_border'] * config['extra_right_spacing'])
                    i = i + 1
        elif table_row == table_num_of_rows - 1:
            # last table row
            i = 0
            for table_col in range(table_num_of_cols):
                if table_col % 2 == 0:
                    if table_col == 0:
                        # first table col
                        to_print.append(theme['bottom_left_corner'])
                    elif table_col == table_num_of_cols - 1:
                        # last table col
                        to_print.append(theme['bottom_right_corner'])
                    else:
                        to_print.append(theme['bottom_cross'])
                elif table_col % 2 == 1:
                    to_print.append(theme['hline_border'] * config['extra_left_spacing'])
                    to_print.append(theme['hline_border'] * len(longer_table_row[i]))
                    to_print.append(theme['hline_border'] * config['extra_right_spacing'])
                    i = i + 1
        else:
            # the mid rows
            if table_row % 2 == 0:
                i = 0
                for table_col in range(table_num_of_cols):
                    if table_col % 2 == 0:
                        if table_col == 0:
                            # first table col
                            to_print.append(theme['middle_left_cross'])
                        elif table_col == table_num_of_cols - 1:
                            # last table col
                            to_print.append(theme['middle_right_cross'])
                            to_print.append('\n')
                        else:
                            to_print.append(theme['middle_center_cross'])
                    elif table_col % 2 == 1:
                        to_print.append(theme['hline'] * config['extra_left_spacing'])
                        to_print.append(theme['hline'] * len(longer_table_row[i]))
                        to_print.append(theme['hline'] * config['extra_right_spacing'])
                        i = i + 1
            elif table_row % 2 == 1:
                array_col = 0
                for table_col in range(table_num_of_cols):
                    if table_col % 2 == 0:
                        if table_col == 0:
                            # first table col
                            to_print.append(theme['vline_border'])
                        elif table_col == table_num_of_cols - 1:
                            # last table col
                            to_print.append(theme['vline_border'])
                            to_print.append('\n')
                        else:
                            to_print.append(theme['vline'])
                    elif table_col % 2 == 1:
                        if array_col < array_num_of_cols:
                            to_print.append(' ' * config['extra_left_spacing'])
                            try:
                                to_print.append(array[array_row][array_col])
                            except IndexError:
                                to_print.append(array[array_col])
                            try:
                                to_print.append(' ' * (len(longer_table_row[array_col]) - len(array[array_row][array_col])))
                            except IndexError:
                                to_print.append(' ' * (len(longer_table_row[array_col]) - len(array[array_col])))
                            to_print.append(' ' * config['extra_right_spacing'])
                            array_col = array_col + 1
                array_row = array_row + 1

    print(''.join(to_print))