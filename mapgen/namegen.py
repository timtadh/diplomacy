import random, string

# Diplomacy territory name generator
# last edited on 2/6/09 by LP

# assumptions: all sea territories end with an end_s
# land territories may start with a title OR end with end_l

# Pass in type variable, which can be either 'land' or 'sea'
class Namer(object):

    def __init__(self):
        self.title = ["New", "The", "Republic of"]
        self.prefix = [
            "Co", "Oh", "Cal", "Ok", "Vir", "Flor", "Kan", "Min", "Ar", "Ne", "Wa", "Id", "Ma"
        ]
        self.mid = ["la", "if", "gin", "i", "e", "v", "sh", "gic"]
        self.mid2 = ["ra", "or", "hom", "d", "sot", "zon", "ad", "ing", "al"]
        self.suffix = ["do", "io", "nia", "a", "sas", "ton", "ho"]
        self.end_l = ["Land", "Kingdom", "Collective", "Republic", "Empire"]
        self.end_s = ["Sea", "Ocean"]

        self.naming = [
            self.title, self.prefix, self.mid, self.mid2, 
            self.suffix, self.end_l, self.end_s
        ]
        
        self.used_names = set()
        self.used_abbrevs = set()
    
    def create(self, tpe, i=0):

        name = []
        abbrev = ""
        
        # decide if there will be a title or ending appended to the name
        def extendname(x, prefix = "", suffix = ""):
            strval = random.choice(x)
            name.append(prefix + strval + suffix)
            return strval
        
        extra = random.randint(0,2)
        skip = random.randint(0,2)

        if extra == 1:
            extendname(self.title, suffix = " ")

        extendname(self.prefix)
        abbrev = name[0][0]

        for x in self.naming[2+skip:5]:
            piece = extendname(x)
            if len(abbrev) == 1 and random.randint(0, skip) == 0:
                abbrev = abbrev + piece[0]
        if len(abbrev) == 1:
            abbrev = abbrev + name[-1][0]

        if tpe == 'land' and extra == 2:
            s = extendname(self.end_l, prefix = " ")
            abbrev = abbrev + s[0]
        
        if tpe == 'sea':
            s = extendname(self.end_s, prefix = " ")
            abbrev = abbrev + s[0]
        
        if len(abbrev) == 2:
            abbrev = abbrev + name[-1][-1]
            
        name_str = "".join(name)
        abbrev = string.upper(abbrev)
        
        if abbrev in self.used_abbrevs or name_str in self.used_names and i < 1000:
            return self.create(tpe, i+1)
        elif i >= 100:
            print "Namer recursion depth exceeded (non-fatal, just annoying)"
        
        self.used_names.add(name_str)
        self.used_abbrevs.add(abbrev)
        return name_str, abbrev
    
