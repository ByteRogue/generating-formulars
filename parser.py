READ = 0
SUM = 1
CONCAT = 2
BIGGER = 3

def parse(expression):
    if expression == '%':
        return 'get_data(-1)'
    if expression.startswith('`'):
        return expression[1:]
    if expression.startswith('@'):
        return 'get_data("%s")' % (expression[1:])
    if ':' in expression:
        return 'get_data(\'%s\')' % (expression)
    if '>' in expression:
        nums = expression.split('>')
        a = 'get_data('+nums[0]+')'
        b = 'get_data('+nums[1]+')'
        return '('+a+' > '+b+' ? '+a+' : \'\')'
    elif '^' in expression:
        nums = expression.split('^')
        a = 'get_data('+nums[0]+')'
        b = 'get_data('+nums[1]+')'
        return '('+a+' ? '+a+' : '+b+')'
    calculation = ''
    stack = []
    val = ''
    state = READ
    number = False
    cmd = ''
    b1 = b2 = 0
    for c in expression:

        if c.isdigit():
            val+=c
        elif c.isalpha():
            cmd+=c
        elif c == '#':
            number = True
            
        elif c in ('+','-','*','(',')',','):
            if number:
                calculation+=val
                number = False
            else:
                if cmd:
                    calculation+=cmd
                    cmd =''
                else:
                    calculation+='get_data('+val+')'
            calculation += ' '+c+' '
            val = ''
        elif c=='|':
            
            calculation+='get_data('+val+')'
            calculation += '.\' \'.'
            val=''
            number=False

    if val:
        if number:
            calculation+=val
        else:
            calculation+='get_data('+val+')'
    return '('+calculation+')'

