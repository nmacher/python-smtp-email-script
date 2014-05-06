'''
A file containing a class with a few utilities
Created on Jan 19, 2014

@author: Nathan
'''

class MyFlattener:
    '''
    This class contains a few utilities for flattening lists into different types
    '''
    def flatten_list_of_list(self, lst):
        """example: [[a],[b]] --> [a, b]"""
        flattened_list = list()
        for i in lst:
            for item in i:
                flattened_list.append(item)
        return flattened_list
    
    def list_to_str(self, lst, glue):
        return glue.join(str(x) for x in lst)


    def __init__(self):
        '''
        Constructor
        '''
        