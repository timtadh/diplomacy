import os, re, yaptu

__rex = re.compile('\s*\<\%([^\<\%]+)\%\>')
__rbe = re.compile('\s*\<\+')
__ren = re.compile('\s*\-\>')
__rco = re.compile('\s*\|= ')

__templater_namespace = locals()

def print_error(error):
    print_template("templates/error_template.html",  locals())

def print_template(template_path, namespace):
    f = open(template_path, 'r')
    s = f.readlines()
    f.close()
    
    #if 'yaptu' not in namespace: namespace.update({'yaptu':yaptu})
    if 'templater' not in namespace: 
        import templater as __templater
        namespace.update({'templater':__templater})
    
    cop = yaptu.copier(__rex, namespace, __rbe, __ren, __rco)
    cop.copy(s)


if __name__ == '__main__':
    print locals()
    print globals()
    print dir()
    print __templater_namespace

