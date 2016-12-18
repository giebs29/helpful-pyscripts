class FauxClass(object):
    def __init__(self,print_name=None,print_args=None):
        self.print_name = print_name
        self.print_args = print_args

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            if self.print_name and self.print_args:
                print name,kwargs
            elif self.print_args:
                print kwargs
            elif self.print_name:
                print name
        return wrapper

arcpy = FauxClass(True,True)
arcpy.fake_method(param1="a",param2="b",param3="c")
