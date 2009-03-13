import random

# Diplomacy territory name generator
# last edited on 2/6/09 by LP

# assumptions: all sea territories end with an end_s
# land territories may start with a title OR end with end_l

# Pass in type variable, which can be either 'land' or 'sea'
class NameIt(object):

    def __init__(self, land, sea):
        self.title = ["New ", "The "]
        self.prefix = ["Co", "Oh", "Cal", "Ok", "Vir", "Flor", "Kan", "Min", "Ar", "Ne", "Wa", "Id"]
        self.mid = ["la", "if", "gin", "i", "e", "v", "sh"]
        self.mid2 = ["ra", "or", "hom", "d", "sot", "zon", "ad", "ing"]
        self.suffix = ["do", "io", "nia", "a", "sas", "ton", "ho"]
        self.end_l = [" Land", " Kingdom"]
        self.end_s = [" Sea", " Ocean"]

        self.naming = [self.title, self.prefix, self.mid, self.mid2, self.suffix, self.end_l, self.end_s]

        self.land = land
        self.sea = sea

        result = self.fillTable(land, sea)
        print result


    def fillTable(self, land, sea):
        nameset = []

        for i in range(self.land):
            nameset.append(self.createName('land'))
            
        for j in range(self.sea):
            nameset.append(self.createName('sea'))

        return nameset
    

    def createName(self, tpe):
        name = []

        # choose a random number between 0 and the end of a list
        def pickno(x_): return random.randint(0, (x_-1))
        # decide if there will be a title or ending appended to the name
        def extendname(x_): name.append(x_[pickno(len(x_))])
        
        extra = random.randint(0,2)
        skip = random.randint(0,2)

        if extra == 1:
            extendname(self.title)

        extendname(self.prefix)

        for x in self.naming[2+skip:5]:
            extendname(x)

        if tpe == 'land' and extra == 2:
            extendname(self.end_l)

        if tpe == 'sea':
            extendname(self.end_s)

        n = ""
        for x in name[0:(len(name)+1)]:
            n = n + x

        return n




