import tabledraw
import configfile
import numpy

test_array = numpy.array([['n','Tasks','Status'],
                          ['abcd','efgh','ijkl'],
                          ['mnop','qrst','uvwx']])

config = configfile.ConfigFile()


theme0 = {
    'hline' : '-',
    'hline_border' : '-',
    'vline' : '|',
    'vline_border' : '|',
    'top_left_corner' : '-',
    'top_right_corner' : '-',
    'bottom_left_corner' : '-',
    'bottom_right_corner' : '-',
    'top_cross' : '-',
    'middle_left_cross' : '-',
    'middle_center_cross' : '-',
    'middle_right_cross' : '-',
    'bottom_cross' : '-'
}

theme1 = {
    'hline' : '─',
    'hline_border' : '─',
    'vline' : '│',
    'vline_border' : '│',
    'top_left_corner' : '┌',
    'top_right_corner' : '┐',
    'bottom_left_corner' : '└',
    'bottom_right_corner' : '┘',
    'top_cross' : '┬',
    'middle_left_cross' : '├',
    'middle_center_cross' : '┼',
    'middle_right_cross' : '┤',
    'bottom_cross' : '┴'
}

theme2 = {
    'hline' : ' ',
    'hline_border' : '─',
    'vline' : '│',
    'vline_border' : '│',
    'top_left_corner' : '┌',
    'top_right_corner' : '┐',
    'bottom_left_corner' : '└',
    'bottom_right_corner' : '┘',
    'top_cross' : '┬',
    'middle_left_cross' : '│',
    'middle_center_cross' : '│',
    'middle_right_cross' : '│',
    'bottom_cross' : '┴'
}

theme3 = {
    'hline' : '-',
    'hline_border' : '=',
    'vline' : '│',
    'vline_border' : '|',
    'top_left_corner' : '+',
    'top_right_corner' : '+',
    'bottom_left_corner' : '+',
    'bottom_right_corner' : '+',
    'top_cross' : '+',
    'middle_left_cross' : '+',
    'middle_center_cross' : '+',
    'middle_right_cross' : '+',
    'bottom_cross' : '+'
}

theme4 = {
    'hline' : '-',
    'hline_border' : '=',
    'vline' : '│',
    'vline_border' : '|',
    'top_left_corner' : '+',
    'top_right_corner' : '+',
    'bottom_left_corner' : '+',
    'bottom_right_corner' : '+',
    'top_cross' : '+',
    'middle_left_cross' : '+',
    'middle_center_cross' : '+',
    'middle_right_cross' : '+',
    'bottom_cross' : '+'
}

def ShowThemes():
    tabledraw.TableDraw(test_array, config, theme0)
    print('\n')
    tabledraw.TableDraw(test_array, config, theme1)
    print('\n')
    tabledraw.TableDraw(test_array, config, theme2)
    print('\n')
    tabledraw.TableDraw(test_array, config, theme3)
    print('\n')
    tabledraw.TableDraw(test_array, config, theme4)
    print('\n')

def Themes(theme):
    match theme:
        case 0:
            return theme0
        case 1:
            return theme1
        case 2:
            return theme2
        case 3:
            return theme3
ShowThemes()