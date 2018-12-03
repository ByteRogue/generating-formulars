import os, sys
from fields import get_fields
#from parser import *
ROOT = 'st_galen'
if len(sys.argv) > 1:
    ROOT = sys.argv[1]

has_data = False
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


def get_name(field_type):
    if not has_data:
        if field_type == 'left':
            return '\'Podatak\''
        elif field_type == 'center':
            return '\'&times;\''
        elif field_type == 'date':
            return '\'123\''
        else:
            return '\'numero\''
    else:
        #implementirati citanje iz fajla polja
        return content_data[page_num][i]

full = open(os.path.join(ROOT,('data.php')),'w')
full.write('<?php\n\n')
full.write('$html = [\n')    
for f in os.listdir(ROOT):
    if not os.path.isdir(os.path.join(ROOT,f)):
        continue
    num = f.split(' ')[-1]

    form_root = os.path.join(ROOT, f)
    #offset file
    offsets = os.path.join(form_root,'offset.txt')
    if os.path.isfile(offsets):
        offsets = open(offsets).read().split('\n')
    else:
        offsets = []
    #reading data from file
    datafile = os.path.join(form_root,'data.txt')
    content_data = []
    if os.path.isfile(datafile):
        data = open(datafile,'r')
        lines = data.read().split('\n')
        
        for l in lines:
            
            page = []
            field_content = l.split(' ')
            for fil in field_content:
                parsed = parse(fil)
                
                page.append(parsed)
            content_data.append(page)
        
    out = open(os.path.join(ROOT,('out%s.php'%(num))),'w')
    out.write('<?php\n\n')
    out.write('$html = [\n')

    full.write('[\n')
    
    page_num = 0
    for filename in os.listdir(form_root):
        if not filename.endswith('.png'):
            continue
        path = os.path.join(form_root, filename)
        offset = (0,0)
        if page_num < len(offsets):
            offset = [int(x) for x in offsets[page_num].split(' ')]
        edges = get_fields(path,offset)
        
        for i,e in enumerate(edges):
            data = [x/300.0 for x in e[:-1]]

            div_class = 'data-left'
            if e[-1] == 'center':

                div_class = 'data-center'
            if e[-1] == 'right':

                div_class = 'data-right'
            if page_num < len(content_data) and i < len(content_data[page_num]):
                has_data = True
            else:
                has_data = False
            
            name = get_name(e[-1])
            t = (e[-1],)+tuple(data)+(div_class, name)
            if e != edges[-1]:
                full.write('\'<div class="field %s" style="top:%.2fin;left:%.2fin;width:%.2fin;height:%.2fin;"><div class="%s">\'.%s.\'</div></div>\'.\n' % t)

                out.write('\'<div class="field %s" style="top:%.2fin;left:%.2fin;width:%.2fin;height:%.2fin;"><div class="%s">\'.%s.\'</div></div>\'.\n' % t)
            else:
                full.write('\'<div class="field %s" style="top:%.2fin;left:%.2fin;width:%.2fin;height:%.2fin;"><div class="%s">\'.%s.\'</div></div>\'\n' % t)
                out.write('\'<div class="field %s" style="top:%.2fin;left:%.2fin;width:%.2fin;height:%.2fin;"><div class="%s">\'.%s.\'</div></div>\'\n' % t)
        out.write(',\n\n')
        full.write(',\n\n')
        page_num+=1

    out.write('];\n\n')
    out.close()
    full.write('],\n\n');
full.write('];\n\n')
full.close()
