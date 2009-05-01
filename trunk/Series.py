#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Serie.py
#
# Copyright (c) 2008 Magnun Leno da Silva
#
# Author: Magnun Leno da Silva <magnun.leno@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

# Contributor: Rodrigo Moreiro Araujo <alf.rodrigo@gmail.com>

#import cairoplot
import doctest

NUMTYPES = (int, float, long)
LISTTYPES = (list, tuple)
STRTYPES = (str, unicode)
FILLING_TYPES = ['linear', 'solid', 'gradient']
DEFAULT_COLOR_FILLING = 'solid'
#TODO: Define default color list
DEFAULT_COLOR_LIST = None

class Data(object):
    '''
        Class that models the main data structure.
        It can hold:
         - a number type (int, float or long)
         - a tuple, witch represents a point and can have 2 or 3 items (x,y,z)
         - if passed a list it will be converted to a tuple.
         
        obs: In case is passed a tuple it will convert to tuple
    '''
    def __init__(self, data=None, name=None, parent=None):
        '''
            Starts main atributes from the Data class
            @name    - Name for each point;
            @content - The real data, can be an int, float, long or tuple, which
                        represents a point (x,y,z);
            @parent  - A pointer that give the data access to it's parent.
            
            Usage:
            >>> d = Data(name='empty'); print d
            empty: ()
            >>> d = Data((1,1),'point a'); print d
            point a: (1, 1)
            >>> d = Data((1,2,3),'point b'); print d
            point b: (1, 2, 3)
            >>> d = Data([2,3],'point c'); print d
            point c: (2, 3)
            >>> d = Data(12, 'simple value'); print d
            simple value: 12
        '''
        # Initial values
        self.__content = None
        self.__name = None
        
        # Setting passed values
        self.parent = parent
        self.name = name
        self.content = data
        
    # Name property
    @apply
    def name():
        doc = '''
            Name is a read/write property that controls the input of name.
             - If passed an invalid value it cleans the name with None
             
            Usage:
            >>> d = Data(13); d.name = 'name_test'; print d
            name_test: 13
            >>> d.name = 11; print d
            13
            >>> d.name = 'other_name'; print d
            other_name: 13
            >>> d.name = None; print d
            13
            >>> d.name = 'last_name'; print d
            last_name: 13
            >>> d.name = ''; print d
            13
        '''
        def fget(self):
            '''
                returns the name as a string
            '''
            return self.__name
        
        def fset(self, name):
            '''
                Sets the name of the Data
            '''
            if type(name) in STRTYPES and len(name) > 0:
                self.__name = name
            else:
                self.__name = None
                
        
        
        return property(**locals())

    # Content property
    @apply
    def content():
        doc = '''
            Content is a read/write property that validate the data passed
            and return it.
            
            Usage:
            >>> d = Data(); d.content = 13; d.content
            13
            >>> d = Data(); d.content = (1,2); d.content
            (1, 2)
            >>> d = Data(); d.content = (1,2,3); d.content
            (1, 2, 3)
            >>> d = Data(); d.content = [1,2,3]; d.content
            (1, 2, 3)
            >>> d = Data(); d.content = [1.5,.2,3.3]; d.content
            (1.5, 0.20000000000000001, 3.2999999999999998)
        '''
        def fget(self):
            '''
                Return the content of Data
            '''
            return self.__content

        def fset(self, data):
            '''
                Ensures that data is a valid tuple/list or a number (int, float
                or long)
            '''
            # Type: None
            if data is None:
                self.__content = None
                return
            
            # Type: Int or Float
            elif type(data) in NUMTYPES:
                self.__content = data
            
            # Type: List or Tuple
            elif type(data) in LISTTYPES:
                # Ensures the correct size
                if len(data) not in (2, 3):
                    raise TypeError, "Data (as list/tuple) must have 2 or 3 items"
                    return
                    
                # Ensures that all items in list/tuple is a number
                isnum = lambda x : type(x) not in NUMTYPES
                    
                if max(map(isnum, data)):
                    # An item in data isn't an int or a float
                    raise TypeError, "All content of data must be a number (int or float)"
                    
                # Convert the tuple to list
                if type(data) is list:
                    data = tuple(data)
                    
                # Append a copy and sets the type
                self.__content = data[:]
            
            # Unknown type!
            else:
                self.__content = None
                raise TypeError, "Data must be an int, float or a tuple with two or three items"
                return
            
        return property(**locals())

    
    def clear(self):
        '''
            Clear the all Data (content, name and parent)
        '''
        self.content = None
        self.name = None
        self.parent = None
        
    def copy(self):
        '''
            Returns a copy of the Data structure
        '''
        # The copy
        new_data = Data()
        if self.content is not None:
            # If content is a point
            if type(self.content) is tuple:
                new_data.__content = self.content[:]
                
            # If content is a number
            else:
                new_data.__content = self.content
                
        # If it has a name
        if self.name is not None:
            new_data.__name = self.name
            
        return new_data
    
    def __str__(self):
        '''
            Return a string representation of the Data structure
        '''
        if self.name is None:
            if self.content is None:
                return ''
            return str(self.content)
        else:
            if self.content is None:
                return self.name+": ()"
            return self.name+": "+str(self.content)

    def __len__(self):
        '''
            Return the length of the Data.
             - If it's a number return 1;
             - If it's a list return it's length;
             - If its None return 0.
        '''
        if self.content is None:
            return 0
        elif type(self.content) in NUMTYPES:
            return 1
        return len(self.content)
    
    
    

class Group(object):
    '''
        Class that moodels a group of data. Every value (int, float, long, tuple
        or list) passed is converted to a list of Data.
        It can receive:
         - A single number (int, float, long);
         - A list of numbers;
         - A tuple of numbers;
         - An instance of Data;
         - A list of Data;
         
         Obs: If a tuple with 2 or 3 items is passed it is converted to a point.
              If a tuple with only 1 item is passed it's converted to a number;
              If a tuple with more then 2 items is passed it's converted to a
               list of numbers
    '''
    def __init__(self, group=None, name=None, parent=None):
        '''
            Starts main atributes in Group instance.
            @data_list  - a list of data witch compound the group;
            @range      - a range that represent the x axis of possible functions;
            @name       - name of the grouping of data;
            @parent     - the Serie parent of this group.
            
            Usage:
            >>> g = Group(13, 'simple number'); print g
            simple number ['13']
            >>> g = Group((1,2), 'simple point'); print g
            simple point ['(1, 2)']
            >>> g = Group([1,2,3,4], 'list of numbers'); print g
            list of numbers ['1', '2', '3', '4']
            >>> g = Group((1,2,3,4),'int in tuple'); print g
            int in tuple ['1', '2', '3', '4']
            >>> g = Group([(1,2),(2,3),(3,4)], 'list of points'); print g
            list of points ['(1, 2)', '(2, 3)', '(3, 4)']
            >>> g = Group([[1,2,3],[1,2,3]], '2D coordinated lists'); print g
            2D coordinated lists ['(1, 1)', '(2, 2)', '(3, 3)']
            >>> g = Group([[1,2],[1,2],[1,2]], '3D coordinated lists'); print g
            3D coordinated lists ['(1, 1, 1)', '(2, 2, 2)']
        '''
        # Initial values
        self.__data_list = []
        self.__range = []
        self.__name = None
        
        
        self.parent = parent
        self.name = name
        self.data_list = group
        
    # Name property
    @apply
    def name():
        doc = '''
            Name is a read/write property that controls the input of name.
             - If passed an invalid value it cleans the name with None
             
            Usage:
            >>> g = Group(13); g.name = 'name_test'; print g
            name_test ['13']
            >>> g.name = 11; print g
            ['13']
            >>> g.name = 'other_name'; print g
            other_name ['13']
            >>> g.name = None; print g
            ['13']
            >>> g.name = 'last_name'; print g
            last_name ['13']
            >>> g.name = ''; print g
            ['13']
        '''
        def fget(self):
            '''
                Returns the name as a string
            '''
            return self.__name
        
        def fset(self, name):
            '''
                Sets the name of the Group
            '''
            if type(name) in STRTYPES and len(name) > 0:
                self.__name = name
            else:
                self.__name = None
        
        return property(**locals())

    # data_list property
    @apply
    def data_list():
        doc = '''
            The data_list is a read/write property that can be a list of
            numbers, a list of points or a list of coordinated lists. This
            property use mainly the self.add_data method.
            
            Usage:
            >>> g = Group(); g.data_list = 13; print g
            ['13']
            >>> g.data_list = (1,2); print g
            ['(1, 2)']
            >>> g.data_list = Data((1,2),'point a'); print g
            ['point a: (1, 2)']
            >>> g.data_list = [1,2,3]; print g
            ['1', '2', '3']
            >>> g.data_list = (1,2,3,4); print g
            ['1', '2', '3', '4']
            >>> g.data_list = [(1,2),(2,3),(3,4)]; print g
            ['(1, 2)', '(2, 3)', '(3, 4)']
            >>> g.data_list = [[1,2],[1,2]]; print g
            ['(1, 1)', '(2, 2)']
            >>> g.data_list = [[1,2],[1,2],[1,2]]; print g
            ['(1, 1, 1)', '(2, 2, 2)']
            >>> g.range = (10); g.data_list = lambda x:x**2; print g
            ['(0.0, 0.0)', '(1.0, 1.0)', '(2.0, 4.0)', '(3.0, 9.0)', '(4.0, 16.0)', '(5.0, 25.0)', '(6.0, 36.0)', '(7.0, 49.0)', '(8.0, 64.0)', '(9.0, 81.0)']
        '''
        def fget(self):
            '''
                Returns the value of data_list
            '''
            return self.__data_list

        def fset(self, group):
            '''
                Ensures that group is valid.
            '''
            # None
            if group is None:
                self.__data_list = []
            
            # Int/float/long or Instance of Data
            elif type(group) in NUMTYPES or isinstance(group, Data):
                # Clean data_list
                self.__data_list = []
                self.add_data(group)
            
            # One point
            elif type(group) is tuple and len(group) in (2,3):
                self.__data_list = []
                self.add_data(group)
            
            # list of items
            elif type(group) in LISTTYPES and type(group[0]) is not list:
                # Clean data_list
                self.__data_list = []
                for item in group:
                    # try to append and catch an exception
                    self.add_data(item)
            
            # function lambda
            elif callable(group):
                # Explicit is better than implicit
                function = group
                # Have range
                if len(self.range) is not 0:
                    # Clean data_list
                    self.__data_list = []
                    # Generate values for the lambda function
                    for x in self.range:
                        #self.add_data((x,round(group(x),2)))
                        self.add_data((x,function(x)))
                        
                # Only have range in parent
                elif self.parent is not None and len(self.parent.range) is not 0:
                    # Copy parent range
                    self.__range = self.parent.range[:]
                    # Clean data_list
                    self.__data_list = []
                    # Generate values for the lambda function
                    for x in self.range:
                        #self.add_data((x,round(group(x),2)))
                        self.add_data((x,function(x)))
                        
                # Don't have range anywhere
                else:
                    # x_data don't exist
                    raise Exception, "Data argument is valid but to use function type please set x_range first"
                
            # Coordinated Lists
            elif type(group) in LISTTYPES and type(group[0]) is list:
                # Clean data_list
                self.__data_list = []
                data = []
                if len(group) == 3:
                    data = [ (group[0][i], group[1][i], group[2][i]) for i in range(len(group[0])) ]
                elif len(group) == 2:
                    data = [ (group[0][i], group[1][i]) for i in range(len(group[0])) ]
                else:
                    raise TypeError, "Only one list of coordinates was received."
                
                for item in data:
                    self.add_data(item)
                
            else:
                raise TypeError, "Group type not supported"

        return property(**locals())

    @apply
    def range():
        doc = '''
            The range is a read/write property that generates a range of values
            for the x axis of the functions. When passed a tuple it almost works
            like the buil-in range funtion:
             - 1 item, represent the end of the range started from 0;
             - 2 items, represents the start and the end, respectively;
             - 3 items, the last one represents the step;
             
            When passed a list the range function understands as a valid range.
            
            Usage:
            >>> g = Group(); g.range = 10; print g.range
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
            >>> g = Group(); g.range = (5); print g.range
            [0.0, 1.0, 2.0, 3.0, 4.0]
            >>> g = Group(); g.range = (1,7); print g.range
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
            >>> g = Group(); g.range = (0,10,2); print g.range
            [0.0, 2.0, 4.0, 6.0, 8.0]
            >>>
            >>> g = Group(); g.range = [0]; print g.range
            [0.0]
            >>> g = Group(); g.range = [0,10,20]; print g.range
            [0.0, 10.0, 20.0]
        '''
        def fget(self):
            '''
                Returns the range
            '''
            return self.__range
        
        def fset(self, x_range):
            '''
                Controls the input of a valid type and generate the range
            '''
            # if passed a simple number convert to tuple
            if type(x_range) in NUMTYPES:
                x_range = (x_range,)
            
            # A list, just convert to float
            if type(x_range) is list and len(x_range) > 0:
                # Convert all to float
                x_range = map(float, x_range)
                # Prevents repeated values and convert back to list
                self.__range = list(set(x_range[:]))
                # Sort the list to ascending order
                self.__range.sort()
            
            # A tuple, must check the lengths and generate the values
            elif type(x_range) is tuple and len(x_range) in (1,2,3):
                # Convert all to float
                x_range = map(float, x_range)
                
                # Inital values
                start = 0.0
                step = 1.0
                end = 0.0
                
                # Only the end and it can't be less or iqual to 0
                if len(x_range) is 1 and x_range > 0:
                        end = x_range[0]
                
                # The start and the end but the start must be lesser then the end
                elif len(x_range) is 2 and x_range[0] < x_range[1]:
                        start = x_range[0]
                        end = x_range[1]
                
                # All 3, but the start must be lesser then the end
                elif x_range[0] <= x_range[1]:
                        start = x_range[0]
                        end = x_range[1]
                        step = x_range[2]
                
                # Starts the range
                self.__range = []
                # Generate the range
                # Cnat use the range function becouse it don't suport float values
                while start < end:
                    self.__range.append(start)
                    start += step
                
            # Incorrect type
            else:
                raise Exception, "x_range must be a list with one or more item or a tuple with 2 or 3 items"
        
        return property(**locals())

    def add_data(self, data, name=None):
        '''
            Append a new data to the data_list.
             - If data is an instance of Data, append it
             - If it's an int, float, tuple or list create an instance of Data and append it
            
            Usage:
            >>> g = Group()
            >>> g.add_data(12); print g
            ['12']
            >>> g.add_data(7,'other'); print g
            ['12', 'other: 7']
            >>>
            >>> g = Group()
            >>> g.add_data((1,1),'a'); print g
            ['a: (1, 1)']
            >>> g.add_data((2,2),'b'); print g
            ['a: (1, 1)', 'b: (2, 2)']
            >>> 
            >>> g.add_data(Data((1,2),'c')); print g
            ['a: (1, 1)', 'b: (2, 2)', 'c: (1, 2)']
        '''
        if not isinstance(data, Data):
            # Try to convert
            data = Data(data,name,self)
        
        if data.content is not None:
            self.__data_list.append(data.copy())
            self.__data_list[-1].parent = self
        

    def to_list(self):
        '''
            Returns the group as a list of numbers (int, float or long) or a
            list of tuples (points 2D or 3D).
            
            Usage:
            >>> g = Group([1,2,3,4],'g1'); g.to_list()
            [1, 2, 3, 4]
            >>> g = Group([(1,2),(2,3),(3,4)],'g2'); g.to_list()
            [(1, 2), (2, 3), (3, 4)]
            >>> g = Group([(1,2,3),(3,4,5)],'g2'); g.to_list()
            [(1, 2, 3), (3, 4, 5)]
        '''
        return [data.content for data in self]
    
    def copy(self):
        '''
            Returns a copy of this group
        '''
        new_group = Group()
        new_group.__name = self.__name
        if self.__range is not None:
            new_group.__range = self.__range[:]
        for data in self:
            new_group.add_data(data.copy())
        return new_group
    
    def get_names(self):
        '''
            Return a list with the names of all data in this group
        '''
        names = []
        for data in self:
            if data.name is None:
                names.append('Data '+str(data.index()+1))
            else:
                names.append(data.name)
        return names
        
    
    def __str__ (self):
        '''
            Returns a string representing the Group
        '''
        ret = ""
        if self.name is not None:
            ret += self.name + " "
        if len(self) > 0:
            list_str = [str(item) for item in self]
            ret += str(list_str)
        else:
            ret += "[]"
        return ret
    
    def __getitem__(self, key):
        '''
            Makes a Group iterable, based in the data_list property
        '''
        return self.data_list[key]
    
    def __len__(self):
        '''
            Returns the length of the Group, based in the data_list property
        '''
        return len(self.data_list)


class Colors(object):
    '''
        Class that models the colors its labels (names) and its properties, RGB
        and filling type.
        
        It can receive:
        - A list where each item is a list with 3 or 4 items. The
          first 3 item represents the colors RGB and the last argument
          defines the filling type. The list will be converted to a dict
          and each color will receve a name based in its position in the
          list.
        - A dictionary where each key will be the color name and its item
          can be a list with 3 or 4 items. The first 3 item represents
          the colors RGB and the last argument defines the filling type.
    '''
    def __init__(self, color_list=None):
        '''
            Start the color_list property
            @ color_list
               is the list or dict contaning the colors properties.
        '''
        self.__color_list = None
        
        self.color_list = color_list
    
    @apply
    def color_list():
        doc = '''
        >>> c = Colors([[1,1,1],[2,2,2,'linear'],[3,3,3,'gradient']])
        >>> print c.color_list
        {'Color 2': [2, 2, 2, 'linear'], 'Color 3': [3, 3, 3, 'gradient'], 'Color 1': [1, 1, 1, 'solid']}
        >>> c.color_list = [[1,1,1],(2,2,2,'solid'),(3,3,3,'linear')]
        >>> print c.color_list
        {'Color 2': [2, 2, 2, 'solid'], 'Color 3': [3, 3, 3, 'linear'], 'Color 1': [1, 1, 1, 'solid']}
        >>> c.color_list = {'a':[1,1,1],'b':(2,2,2,'solid'),'c':(3,3,3,'linear'), 'd':(4,4,4)}
        >>> print c.color_list
        {'a': [1, 1, 1, 'solid'], 'c': [3, 3, 3, 'linear'], 'b': [2, 2, 2, 'solid'], 'd': [4, 4, 4, 'solid']}
        '''
        def fget(self):
            '''
                Return the color list
            '''
            return self.__color_list
        
        def fset(self, color_list):
            '''
                Format the color list to a dictionary
            '''
            if color_list is None:
                self.__color_list = None
                return
            
            if type(color_list) in LISTTYPES and type(color_list[0]) in LISTTYPES:
                old_color_list = color_list[:]
                color_list = {}
                for index, color in enumerate(old_color_list):
                    if len(color) is 3 and max(map(type, color)) in NUMTYPES:
                        color_list['Color '+str(index+1)] = list(color)+[DEFAULT_COLOR_FILLING]
                    elif len(color) is 4 and max(map(type, color[:-1])) in NUMTYPES and color[-1] in FILLING_TYPES:
                        color_list['Color '+str(index+1)] = list(color)
                    else:
                        raise TypeError, "Unsuported color format"
            elif type(color_list) is not dict:
                raise TypeError, "Unsuported color format"
            
            for name, color in color_list.items():
                if len(color) is 3:
                    if max(map(type, color)) in NUMTYPES:
                        color_list[name] = list(color)+[DEFAULT_COLOR_FILLING]
                    else:
                        raise TypeError, "Unsuported color format"
                elif len(color) is 4:
                    if max(map(type, color[:-1])) in NUMTYPES and color[-1] in FILLING_TYPES:
                        color_list[name] = list(color)
                    else:
                        raise TypeError, "Unsuported color format"
            self.__color_list = color_list.copy()
        
        return property(**locals())
        
    
class Serie(object):
    '''
        Class that models a Serie (group of groups). Every value (int, float,
        long, tuple or list) passed is converted to a list of Group or Data.
        It can receive:
         - a single number or point, will be converted to a Group of one Data;
         - a list of numbers, will be converted to a group of numbers;
         - a list of tuples, will converted to a single Group of points;
         - a list of lists of numbers, each 'sublist' will be converted to a
           group of numbers;
         - a list of lists of tuples, each 'sublist' will be converted to a
           group of points;
         - a list of lists of lists, the content of the 'sublist' will be
           processed as coordinated lists and the result will be converted to
           a group of points;
         - a Dictionary where each item can be the same of the list: number,
           point, list of numbers, list of points or list of lists (coordinated
           lists);
         - an instance of Data;
         - an instance of group.
    '''
    def __init__(self, serie=None, name=None, property=[], colors=None):
        '''
            Starts main atributes in Group instance.
            @serie      - a list, dict of data witch compound the serie;
            @name       - name of the serie;
            @property   - a list/dict of properties to be used in the plots of
                          this Serie
            
            Usage:
            >>> print Serie([1,2,3,4])
            ["Group 1 ['1', '2', '3', '4']"]
            >>> print Serie([[1,2,3],[4,5,6]])
            ["Group 1 ['1', '2', '3']", "Group 2 ['4', '5', '6']"]
            >>> print Serie((1,2))
            ["Group 1 ['(1, 2)']"]
            >>> print Serie([(1,2),(2,3)])
            ["Group 1 ['(1, 2)', '(2, 3)']"]
            >>> print Serie([[(1,2),(2,3)],[(4,5),(5,6)]])
            ["Group 1 ['(1, 2)', '(2, 3)']", "Group 2 ['(4, 5)', '(5, 6)']"]
            >>> print Serie([[[1,2,3],[1,2,3],[1,2,3]]])
            ["Group 1 ['(1, 1, 1)', '(2, 2, 2)', '(3, 3, 3)']"]
            >>> print Serie({'g1':[1,2,3], 'g2':[4,5,6]})
            ["g1 ['1', '2', '3']", "g2 ['4', '5', '6']"]
            >>> print Serie({'g1':[(1,2),(2,3)], 'g2':[(4,5),(5,6)]})
            ["g1 ['(1, 2)', '(2, 3)']", "g2 ['(4, 5)', '(5, 6)']"]
            >>> print Serie({'g1':[[1,2],[1,2]], 'g2':[[4,5],[4,5]]})
            ["g1 ['(1, 1)', '(2, 2)']", "g2 ['(4, 4)', '(5, 5)']"]
            >>> print Serie(Data(1,'d1'))
            ["Group 1 ['d1: 1']"]
            >>> print Serie(Group([(1,2),(2,3)],'g1'))
            ["g1 ['(1, 2)', '(2, 3)']"]
        '''
        # Intial values
        self.__group_list = []
        self.__name = None
        self.__range = None
        
        # TODO: Implement colors with filling
        self.__colors = None
        
        self.name = name
        self.group_list = serie
        self.colors = colors
        
    # Name property
    @apply
    def name():
        doc = '''
            Name is a read/write property that controls the input of name.
             - If passed an invalid value it cleans the name with None
             
            Usage:
            >>> s = Serie(13); s.name = 'name_test'; print s
            name_test ["Group 1 ['13']"]
            >>> s.name = 11; print s
            ["Group 1 ['13']"]
            >>> s.name = 'other_name'; print s
            other_name ["Group 1 ['13']"]
            >>> s.name = None; print s
            ["Group 1 ['13']"]
            >>> s.name = 'last_name'; print s
            last_name ["Group 1 ['13']"]
            >>> s.name = ''; print s
            ["Group 1 ['13']"]
        '''
        def fget(self):
            '''
                Returns the name as a string
            '''
            return self.__name
        
        def fset(self, name):
            '''
                Sets the name of the Group
            '''
            if type(name) in STRTYPES and len(name) > 0:
                self.__name = name
            else:
                self.__name = None
        
        return property(**locals())
        
        
        
    # Colors property
    @apply
    def colors():
        doc = '''
        >>> s = Serie()
        >>> s.colors = [[1,1,1],[2,2,2,'linear'],[3,3,3,'gradient']]
        >>> print s.colors
        {'Color 2': [2, 2, 2, 'linear'], 'Color 3': [3, 3, 3, 'gradient'], 'Color 1': [1, 1, 1, 'solid']}
        >>> s.colors = [[1,1,1],(2,2,2,'solid'),(3,3,3,'linear')]
        >>> print s.colors
        {'Color 2': [2, 2, 2, 'solid'], 'Color 3': [3, 3, 3, 'linear'], 'Color 1': [1, 1, 1, 'solid']}
        >>> s.colors = {'a':[1,1,1],'b':(2,2,2,'solid'),'c':(3,3,3,'linear'), 'd':(4,4,4)}
        >>> print s.colors
        {'a': [1, 1, 1, 'solid'], 'c': [3, 3, 3, 'linear'], 'b': [2, 2, 2, 'solid'], 'd': [4, 4, 4, 'solid']}
        '''
        def fget(self):
            '''
                Return the color list
            '''
            return self.__colors.color_list
        
        def fset(self, colors):
            '''
                Format the color list to a dictionary
            '''
            self.__colors = Colors(colors)
        
        return property(**locals())
        
    @apply
    def range():
        doc = '''
            The range is a read/write property that generates a range of values
            for the x axis of the functions. When passed a tuple it almost works
            like the buil-in range funtion:
             - 1 item, represent the end of the range started from 0;
             - 2 items, represents the start and the end, respectively;
             - 3 items, the last one represents the step;
             
            When passed a list the range function understands as a valid range.
            
            Usage:
            >>> s = Serie(); s.range = 10; print s.range
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
            >>> s = Serie(); s.range = (5); print s.range
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
            >>> s = Serie(); s.range = (1,7); print s.range
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
            >>> s = Serie(); s.range = (0,10,2); print s.range
            [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]
            >>>
            >>> s = Serie(); s.range = [0]; print s.range
            [0.0]
            >>> s = Serie(); s.range = [0,10,20]; print s.range
            [0.0, 10.0, 20.0]
        '''
        def fget(self):
            '''
                Returns the range
            '''
            return self.__range
        
        def fset(self, x_range):
            '''
                Controls the input of a valid type and generate the range
            '''
            # if passed a simple number convert to tuple
            if type(x_range) in NUMTYPES:
                x_range = (x_range,)
            
            # A list, just convert to float
            if type(x_range) is list and len(x_range) > 0:
                # Convert all to float
                x_range = map(float, x_range)
                # Prevents repeated values and convert back to list
                self.__range = list(set(x_range[:]))
                # Sort the list to ascending order
                self.__range.sort()
            
            # A tuple, must check the lengths and generate the values
            elif type(x_range) is tuple and len(x_range) in (1,2,3):
                # Convert all to float
                x_range = map(float, x_range)
                
                # Inital values
                start = 0.0
                step = 1.0
                end = 0.0
                
                # Only the end and it can't be less or iqual to 0
                if len(x_range) is 1 and x_range > 0:
                        end = x_range[0]
                
                # The start and the end but the start must be lesser then the end
                elif len(x_range) is 2 and x_range[0] < x_range[1]:
                        start = x_range[0]
                        end = x_range[1]
                
                # All 3, but the start must be lesser then the end
                elif x_range[0] < x_range[1]:
                        start = x_range[0]
                        end = x_range[1]
                        step = x_range[2]
                
                # Starts the range
                self.__range = []
                # Generate the range
                # Cnat use the range function becouse it don't suport float values
                while start <= end:
                    self.__range.append(start)
                    start += step
                
            # Incorrect type
            else:
                raise Exception, "x_range must be a list with one or more item or a tuple with 2 or 3 items"
            
        return property(**locals())
    
    @apply
    def group_list():
        doc = '''
            The group_list is a read/write property used to pre-process the list
            of Groups.
            It can be:
             - a single number, point or lambda, will be converted to a single
               Group of one Data;
             - a list of numbers, will be converted to a group of numbers;
             - a list of tuples, will converted to a single Group of points;
             - a list of lists of numbers, each 'sublist' will be converted to
               a group of numbers;
             - a list of lists of tuples, each 'sublist' will be converted to a
               group of points;
             - a list of lists of lists, the content of the 'sublist' will be
               processed as coordinated lists and the result will be converted
               to a group of points;
             - a list of lambdas, each lambda represents a Group;
             - a Dictionary where each item can be the same of the list: number,
               point, list of numbers, list of points, list of lists
               (coordinated lists) or lambdas
             - an instance of Data;
             - an instance of group.
             
            Usage:
            >>> s = Serie()
            >>> s.group_list = [1,2,3,4]; print s
            ["Group 1 ['1', '2', '3', '4']"]
            >>> s.group_list = [[1,2,3],[4,5,6]]; print s
            ["Group 1 ['1', '2', '3']", "Group 2 ['4', '5', '6']"]
            >>> s.group_list = (1,2); print s
            ["Group 1 ['(1, 2)']"]
            >>> s.group_list = [(1,2),(2,3)]; print s
            ["Group 1 ['(1, 2)', '(2, 3)']"]
            >>> s.group_list = [[(1,2),(2,3)],[(4,5),(5,6)]]; print s
            ["Group 1 ['(1, 2)', '(2, 3)']", "Group 2 ['(4, 5)', '(5, 6)']"]
            >>> s.group_list = [[[1,2,3],[1,2,3],[1,2,3]]]; print s
            ["Group 1 ['(1, 1, 1)', '(2, 2, 2)', '(3, 3, 3)']"]
            >>> s.group_list = {'g1':[1,2,3], 'g2':[4,5,6]}; print s
            ["g1 ['1', '2', '3']", "g2 ['4', '5', '6']"]
            >>> s.group_list = {'g1':[(1,2),(2,3)], 'g2':[(4,5),(5,6)]}; print s
            ["g1 ['(1, 2)', '(2, 3)']", "g2 ['(4, 5)', '(5, 6)']"]
            >>> s.group_list = {'g1':[[1,2],[1,2]], 'g2':[[4,5],[4,5]]}; print s
            ["g1 ['(1, 1)', '(2, 2)']", "g2 ['(4, 4)', '(5, 5)']"]
            >>> s.range = 10
            >>> s.group_list = lambda x:x*2
            >>> s.group_list = [lambda x:x*2, lambda x:x**2, lambda x:x**3]; print s
            ["Group 1 ['(0.0, 0.0)', '(1.0, 2.0)', '(2.0, 4.0)', '(3.0, 6.0)', '(4.0, 8.0)', '(5.0, 10.0)', '(6.0, 12.0)', '(7.0, 14.0)', '(8.0, 16.0)', '(9.0, 18.0)', '(10.0, 20.0)']", "Group 2 ['(0.0, 0.0)', '(1.0, 1.0)', '(2.0, 4.0)', '(3.0, 9.0)', '(4.0, 16.0)', '(5.0, 25.0)', '(6.0, 36.0)', '(7.0, 49.0)', '(8.0, 64.0)', '(9.0, 81.0)', '(10.0, 100.0)']", "Group 3 ['(0.0, 0.0)', '(1.0, 1.0)', '(2.0, 8.0)', '(3.0, 27.0)', '(4.0, 64.0)', '(5.0, 125.0)', '(6.0, 216.0)', '(7.0, 343.0)', '(8.0, 512.0)', '(9.0, 729.0)', '(10.0, 1000.0)']"]
            >>> s.group_list = {'linear':lambda x:x*2, 'square':lambda x:x**2, 'cubic':lambda x:x**3}; print s
            ["cubic ['(0.0, 0.0)', '(1.0, 1.0)', '(2.0, 8.0)', '(3.0, 27.0)', '(4.0, 64.0)', '(5.0, 125.0)', '(6.0, 216.0)', '(7.0, 343.0)', '(8.0, 512.0)', '(9.0, 729.0)', '(10.0, 1000.0)']", "linear ['(0.0, 0.0)', '(1.0, 2.0)', '(2.0, 4.0)', '(3.0, 6.0)', '(4.0, 8.0)', '(5.0, 10.0)', '(6.0, 12.0)', '(7.0, 14.0)', '(8.0, 16.0)', '(9.0, 18.0)', '(10.0, 20.0)']", "square ['(0.0, 0.0)', '(1.0, 1.0)', '(2.0, 4.0)', '(3.0, 9.0)', '(4.0, 16.0)', '(5.0, 25.0)', '(6.0, 36.0)', '(7.0, 49.0)', '(8.0, 64.0)', '(9.0, 81.0)', '(10.0, 100.0)']"]
            >>> s.group_list = Data(1,'d1'); print s
            ["Group 1 ['d1: 1']"]
            >>> s.group_list = Group([(1,2),(2,3)],'g1'); print s
            ["g1 ['(1, 2)', '(2, 3)']"]
        '''
        def fget(self):
            '''
                Return the group list.
            '''
            return self.__group_list
        
        def fset(self, serie):
            '''
                Controls the input of a valid group list.
            '''
            #TODO: Add support to the following strem of data: [ (0.5,5.5) , [(0,4),(6,8)] , (5.5,7) , (7,9)]
            
            # Type: None
            if serie is None:
                self.__group_list = []
            
            # List or Tuple
            elif type(serie) in LISTTYPES:
                self.__group_list = []
                # List of numbers
                if type(serie[0]) in NUMTYPES or type(serie[0]) is tuple:
                    print serie
                    self.add_group(serie)
                    
                # List of anything else
                else:
                    for group in serie:
                        self.add_group(group)
            
            # Dict representing serie of groups
            elif type(serie) is dict:
                self.__group_list = []
                names = serie.keys()
                names.sort()
                for name in names:
                    self.add_group(Group(serie[name],name,self))
                    
            # A single lambda
            elif callable(serie):
                self.__group_list = []
                self.add_group(serie)
                
            # Int/float, instance of Group or Data
            elif type(serie) in NUMTYPES or isinstance(serie, Group) or isinstance(serie, Data):
                self.__group_list = []
                self.add_group(serie)
                
            # Default
            else:
                raise TypeError, "Serie type not supported"

        return property(**locals())
    
    def add_group(self, group, name=None):
        '''
            Append a new group in group_list
        '''
        if not isinstance(group, Group):
            #Try to convert
            group = Group(group, name, self)
            
        if len(group.data_list) is not 0:
            # Auto naming groups
            if group.name is None:
                group.name = "Group "+str(len(self.__group_list)+1)
            self.__group_list.append(group)
            self.__group_list[-1].parent = self
            
    def copy(self):
        '''
            Returns a copy of the Serie
        '''
        new_serie = Serie()
        new_serie.__name = self.__name
        if self.__range is not None:
            new_serie.__range = self.__range[:]
        #Add color property in the copy method
        #self.__colors = None
        
        for group in self:
            new_serie.add_group(group.copy())
            
        return new_serie
    
    def get_names(self):
        '''
            Returns a list of the names of all groups in the Serie
        '''
        names = []
        for group in self:
            if group.name is None:
                names.append('Group '+str(group.index()+1))
            else:
                names.append(group.name)
                
        return names
        
    def to_list(self):
        '''
            Returns a list with the content of all groups and data
        '''
        big_list = []
        for group in self:
            for data in group:
                if type(data.content) in NUMTYPES:
                    big_list.append(data.content)
                else:
                    big_list = big_list + list(data.content)
        return big_list

    def __getitem__(self, key):
        '''
            Makes the Serie iterable, based in the group_list property
        '''
        return self.__group_list[key]
        
    def __str__(self):
        '''
            Returns a string that represents the Serie
        '''
        ret = ""
        if self.name is not None:
            ret += self.name + " "
        if len(self) > 0:
            list_str = [str(item) for item in self]
            ret += str(list_str)
        else:
            ret += "[]"
        return ret
    
    def __len__(self):
        '''
            Returns the length of the Serie, based in the group_lsit property
        '''
        return len(self.group_list)
    

if __name__ == '__main__':
    doctest.testmod()
