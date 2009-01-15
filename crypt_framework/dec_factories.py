def create_existance_check_dec(attr):
    def dec(f, *args, **kwargs):
        def h(*args, **kwargs):
            if len(args) <= 0: raise Exception, 'must be applied to a class method'
            attrs = dir(args[0])
            if '__dict__' in attrs and args[0].__dict__.has_key(attr):
                if args[0].__dict__[attr] != None:
                    return f(*args, **kwargs)
                else:
                    raise Exception, attr + ' must not be None'
            elif '__contains__' in attrs and args[0].__contains__(attr):
                if args.__getattribute__(attr) != None:
                    return f(*args, **kwargs)
                else:
                    raise Exception, attr + ' must not be None'
            else:
                raise Exception, 'could not detirmine the existance of ' + attr + ' in args[0]'
        return h
    return dec

def create_value_check_dec(attr, desired_value):
    def dec(f, *args, **kwargs):
        '''Assumes that an existance check has already been done'''
        def h(*args, **kwargs):
            attrs = dir(args[0])
            if ('__dict__' in attrs):
                if (args[0].__dict__[attr] != desired_value):  raise Exception, attr + ' must equal ' + str(desired_value)
                return f(*args, **kwargs)
            else:
                if args.__getattribute__(attr) != desired_value: raise Exception, attr + ' must equal ' + str(desired_value)
                return f(*args, **kwargs)
        return h
    return dec