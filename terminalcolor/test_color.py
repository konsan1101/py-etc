#!/usr/bin/env python
# -*- coding: utf-8 -*-



def colorText(txt='', fgColor='', fgLine='', bgColor='', ):
    txtColor = ''

    if   (fgLine != ''):
        txtColor += '\033[4m'

    if   (fgColor == 'black'):
        txtColor += '\033[30m'
    elif (fgColor == 'red'):
        txtColor += '\033[31m'
    elif (fgColor == 'green'):
        txtColor += '\033[32m'
    elif (fgColor == 'yellow'):
        txtColor += '\033[33m'
    elif (fgColor == 'blue'):
        txtColor += '\033[34m'
    elif (fgColor == 'magenta'):
        txtColor += '\033[35m'
    elif (fgColor == 'cyan'):
        txtColor += '\033[36m'
    elif (fgColor == 'white'):
        txtColor += '\033[37m'

    if   (bgColor == 'black'):
        txtColor += '\033[40m'
    elif (bgColor == 'red'):
        txtColor += '\033[41m'
    elif (bgColor == 'green'):
        txtColor += '\033[42m'
    elif (bgColor == 'yellow'):
        txtColor += '\033[43m'
    elif (bgColor == 'blue'):
        txtColor += '\033[44m'
    elif (bgColor == 'magenta'):
        txtColor += '\033[45m'
    elif (bgColor == 'cyan'):
        txtColor += '\033[46m'
    elif (bgColor == 'white'):
        txtColor += '\033[47m'

    resetColor = ''
    if (txtColor != ''):
        resetColor = '\033[0m'

    return txtColor + str(txt) + resetColor



if __name__ == '__main__':

    fgColor='white'
    bgColor='black'
    txt = colorText('white', fgColor=fgColor, bgColor=bgColor, )
    print(txt)

    fgColor='red'
    bgColor='green'
    txt = colorText('red/green', fgColor=fgColor, bgColor=bgColor, )
    print(txt)

    fgColor='cyan'
    bgColor=''
    txt = colorText('cyan/line', fgColor=fgColor, fgLine='yes', bgColor=bgColor, )
    print(txt)

    fgColor=''
    bgColor=''
    txt = colorText('normal', fgColor=fgColor, bgColor=bgColor, )
    print(txt)


