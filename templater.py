import os, re, yaptu, cgi
import warnings
warnings.simplefilter('ignore', UserWarning)
import formencode
from formencode import validators
warnings.simplefilter('default', UserWarning)
from crypt_framework import qcrypt

__rex = re.compile('\s*\<\%([^\<\%]+)\%\>')
__rbe = re.compile('\s*\<\+')
__ren = re.compile('\s*\-\>')
__rco = re.compile('\s*\|= ')

__templater_namespace = locals()
#validators.MaxLength

class Text(formencode.FancyValidator):
    __unpackargs__ = ('length',)
    
    htmlre = re.compile('''</?\w+((\s+\w+(\s*=\s*(?:".*?"|'.*?'|[^'">\s]+))?)+\s*|\s*)/?>''')
    
    def allow_whitehtml(self, text):
        whitehtml = ['p', 'i', 'strong', 'b', 'u']
        lt = '&lt;'
        gt = '&gt;'
        for tag in whitehtml:
            while text.find(lt+tag+gt) != -1 and text.find(lt+'/'+tag+gt) != -1:
                text = text.replace(lt+tag+gt, '<'+tag+'>', 1)
                text = text.replace(lt+'/'+tag+gt, '</'+tag+'>', 1)
        return text
    
    def _to_python(self, value, state):
        msg = self.clean(value, True)
        msg = validators.MaxLength(self.length).to_python(msg)
        return msg
    def _from_python(self, value, state):
        return value
    
    def clean(self, text, whitehtml=False):
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        if whitehtml: text = self.allow_whitehtml(text)
        text = text.replace('\n', '<br>')
        text = text.replace('\r', '')
        return text
    
    def hide_all_tags(self, text):
        g = self.htmlre.search(text)
        while g:
            text = text.replace(g.group(), '')
            g = self.htmlre.search(text)
        return text


class SN_Exists(formencode.FancyValidator):
    def _to_python(self, value, state):
        import db
        sn = validators.PlainText(not_empty=True).to_python(value)
        con = db.connections.get_con()
        cur = db.DictCursor(con)
        cur.callproc('user_data_bysn', (sn,))
        r = cur.fetchall()
        cur.close()
        db.connections.release_con(con)
        if r: return sn
        else: 
            raise formencode.Invalid('The screen_name supplied is not in the database.', sn, state)

def print_error(error):
    
    error = Text().clean(error)
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

def print_table(table, table_info, target_page=None, table_name=None, paging=False, rows=15):
    '''
    Prints a paged html table to the standard out.
        table = a list of lists, tuples, or dicts
        table_info = a tuple or list of the this form
            ((0, "column1"), (3, "column2"), (5, "column3"))
            the numbers refer to the column in the table variable the strings are the name of the
            columns
        target_page = The page the table resides on (needed if paging=True)
        table_name = The name of the table (it doesn't print out just used by the pager to
                     refer to this table, need if paging=True)
        paging = turns paging on or off
        rows = number of rows per page
    '''
    form = cgi.FieldStorage()
    if form.has_key(table_name+'_page'): page = int(form[table_name+'_page'].value)
    else: page = 0
    
    if paging: rows_per_page = rows
    else: rows_per_page = 0
    
    if (len(table)%rows_per_page) == 0: pages = len(table)/rows_per_page
    else: pages = len(table)/rows_per_page + 1
    
    print_template("templates/create_table.html", locals())

if __name__ == '__main__':
    print locals()
    print globals()
    print dir()
    print __templater_namespace

