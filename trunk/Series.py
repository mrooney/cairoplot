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

#TODO: Add the x_lables and y_labels to the Series structure
#TODO: Sort the when using dict

import cairoplot

NUMTYPES = (int, float, long)
LISTTYPES = (list, tuple)
STRTYPES = (str, unicode)

class Data(object):
    '''
        Class that models the main data structure
    '''
    def __init__(self, data=None, name=None):
        '''
            Starts main atributes from the Data class
            @name - Possible name for each point
            @data - The real data, can be an int, float or tuple, which represents
                        a point (x,y)
            @type - variable that holds the type of data
        '''
        self.__content = None
        self.__name = None
        self.type = None
        self.parent = None
        
        self.name = name
        self.content = data

    # Data property
    @apply
    def content():
        def fget(self):
            return self.__content

        def fset(self, data):
            '''
                Ensures that data is a valid tuple/list or a number (float or int)
            '''
            # Type: None
            if data is None:
                self.__content = None
                self.type = None
                return

            # Type: List or Tuple
            elif type(data) in LISTTYPES:
                # Ensures the correct size
                if len(data) is not 2 and len(data) is not 3:
                    raise TypeError, "Data (as list/tuple) must have 2 or 3 items"
                    return
                # Ensures thet all items in list/tuple is a number
                isnum = lambda x : type(x) in NUMTYPES
                ret = map(isnum, data)
                if False in ret:
                    # An item in data isn't an int or a float
                    raise TypeError, "All content of data must be a number (int or float)"
                    return
                # Convert the tuple to list
                if type(data) is list:
                    data = tuple(data)
                # Append a copy and sets the type
                self.__content = data[:]
                self.type = tuple

            # Type: Int or Float
            elif type(data) in NUMTYPES:
                self.__content = data
                self.type = type(data)
    
            else:
                self.type = None
                self.__content = None
                raise TypeError, "Data must be an int, float or a tuple with two or three items"
                return

        return property(**locals())

    
    # Name property
    @apply
    def name():
        def fget(self):
            return self.__name

        def fset(self, name):
            '''
                Ensures that data is a valid tuple/list or a number (float or int)
            '''
            if type(name) in STRTYPES and len(name) > 0:
                self.__name = name
            else:
                name = None

        return property(**locals())

    
    
    def clear(self):
        '''
            Clear the content of Data
        '''
        self.content = None
        self.name = None
        self.type = None
        
    def copy(self):
        new_data = Data()
        if self.content is not None:
            if type(self.content) is tuple:
                new_data.__content = self.content[:]
            else:
                new_data.__content = self.content
        if self.name is not None:
            new_data.__name = self.name
        new_data.type = self.type
        new_data.parent = self.parent
        return new_data
        
    def __str__(self):
        if self.name is None:
            if self.content is None:
                return ''
            return str(self.content)
        else:
            if self.content is None:
                return self.name+": ()"
            return self.name+": "+str(self.content)

    def __len__(self):
        if self.content is None:
            return 0
        elif type(self.content) in NUMTYPES:
            return 1
        return len(self.content)
    

class Group(object):
    '''
        Class that moodels a group of data.
    '''
    def __init__(self, group=None, name=None):
        self.__data_list = []
        self.__x_range = []
        self.parent = None
        self.__name = None
        
        self.name = name
        if group is not None:
            self.data_list = group
        
    # Name property
    @apply
    def name():
        def fget(self):
            return self.__name

        def fset(self, name):
            '''
                Ensures that data is a valid tuple/list or a number (float or int)
            '''
            if type(name) in STRTYPES and len(name) > 0:
                self.__name = name
            else:
                name = None

        return property(**locals())

    # Group property
    @apply
    def data_list():
        def fget(self):
            return tuple(self.__data_list)

        def fset(self, group):
            '''
                Set the group data.
                If any data is a list, passes the data and the next value, as these are coordinates list.
            '''
            # function lambda
            if callable(group):
                if len(self.__x_range) is 0:
                    # x_data don't exist
                    raise Exception, "Data argument is valid but to use function type please set x_range first"
                else:
                    # Clean data_list
                    self.__data_list = []
                    # Generate values for the lambda function
                    for x in self.__x_range:
                        self.add_data(group(x))
                        
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
                    return
                for item in data:
                    self.add_data(item)
            
            # point
            elif type(group) is tuple and 2 <= len(group) <= 3:
                self.__data_list = []
                self.add_data(group)
                
            # list of items
            elif type(group) in LISTTYPES:
                # Clean data_list
                self.__data_list = []
                for item in group:
                    # try to append and catch an exception
                    try:
                        self.add_data(item)
                    except:
                        raise TypeError, "One of the contents of group isn't an instance of Data"
                        self.__data_list = []
                        return
            # Int/Float
            elif type(group) in NUMTYPES:
                # Clean data_list
                self.__data_list = []
                try:
                    self.add_data(group)
                except:
                    raise TypeError, "One of the contents of group isn't an instance of Data"
                    self.__data_list = []
                    return
            # Instance of Data
            elif isinstance(group, Data):
                self.__data_list = []
                self.add_data(group)
            else:
                raise TypeError, "Group type not supported"

        return property(**locals())


    def add_data(self, data, name=None):
        '''
            Append a new data to the data_list.
            If data is an instance of Data, append it
            If it's an int, float, tuple or list create an instance of Data and append it
        '''
        if not isinstance(data, Data):
            # Try to convert
            data = Data(data,name)
            
        if data.content is not None:
            self.__data_list.append(data.copy())
            self.__data_list[-1].parent = self
        
    
    def _get_x_range(self):
        return str(self.__x_range)
        
    def _set_x_range(self, x_range):
        '''
            Sets the x_data in case it is necessary
            @range - Can be a list of 2 elements [start, end] or a range
            @step - Used if the arg range has only 2 elements. It is used to create the x_range
        '''
        if type(x_range) is list and len(x_range) > 0:
            self.__x_range = x_range[:]
            return
        
        elif type(x_range) is tuple and len(x_range) in (2,3):
            step = 1
            start = x_range[0]
            end = x_range[-1]
            if len(x_range) is 3:
                step = x_range[1]
                
            if float in [type(start), type(end), type(step)]:
                start = float(start)
                end = float(end)
                step = float(step)
            
            self.__x_range = [start]
            while True:
                start = start + step
                if start > end:
                    break
                self.__x_range.append(start)
        else:
            raise Exception, "x_range must be a list with one or more item or a tuple with 2 or 3 items"

    def toList(self):
        return [data.content for data in self]
            
    def __str__ (self):
        ret = ""
        if self.name is not None:
            ret += self.name + " "
        if len(self.data_list) > 0:
            list_str = [str(item) for item in self]
            ret += str(list_str)
        else:
            ret += "[]"
        return ret
            
    def __getitem__(self, key):
        return self.data_list[key]

    def __len__(self):
        n = 0
        for data in self:
            n += 1
        return n
        
    x_range = property(_get_x_range, _set_x_range)
    
class Serie(object):
    def __init__(self, serie=None, name=None):
        self.__group_list = []
        self.__name = None
        if name is not None:
            self.name = name
        if serie is not None:
            self.group_list = serie
        
    # Name property
    @apply
    def name():
        def fget(self):
            return self.__name

        def fset(self, name):
            '''
                Ensures that data is a valid tuple/list or a number (float or int)
            '''
            if type(name) in STRTYPES and len(name) > 0:
                self.__name = name
            else:
                name = None

        return property(**locals())
    
    @apply
    def group_list():
        def fget(self):
            return self.__group_list
        
        def fset(self, serie):
            # List or Tuple
            if type(serie) in LISTTYPES:
                self.__group_list = []
                # List of numbers
                if type(serie[0]) in NUMTYPES:
                    self.add_group(serie)
                    
                # List of lists/tuple or anything else
                else:
                    for group in serie:
                        self.add_group(group)
            
            # Dict representing serie of groups
            elif type(serie) is dict:
                self.__group_list = []
                groups = serie.items()
                for group in groups:
                    self.add_group(Group(group[1],group[0]))
            # Int/float, instance of Group or Data
            elif type(serie) in [int, float] or isinstance(serie, Group) or isinstance(serie, Data):
                self.__group_list = []
                self.add_group(serie)
            else:
                raise TypeError, "Serie type not supported"

        return property(**locals())
    
    def add_group(self, group, name=None):
        if not isinstance(group, Group):
            #Try to convert
            group = Group(group, name)
            
        if len(group.data_list) is not 0:
            self.__group_list.append(group)
            self.__group_list[-1].parent = self        

    def __getitem__(self, key):
        return self.__group_list[key]
        
    def __str__(self):
        ret = ""
        if self.name is not None:
            ret += self.name + " "
        if len(self.__group_list) > 0:
            list_str = [str(item) for item in self.__group_list]
            ret += str(list_str)
        else:
            ret += "[]"
        return ret
    
    def __len__(self):
        n = 0
        for group in self:
            n += 1
        return n

    def tste(self):
        pass
              

############################### Tests ###############################

DATAS = 0
GROUPS = 0
SERIES = 0

if DATAS:
    # DATA TESTS!!
    print "Part 1"
    print "Blank data -",Data()
    print "Int data -",Data(1)
    print "List data 1 -",Data([1,2,3])
    print "List data 2 -",Data((1,2))
    print
    print "Part 2"
    print "Blank named data -",Data(name="test")
    print "Int data -",Data(1,"int_test")
    print "List data 1 -",Data([1,2,3],"list_test")
    print "List data 2 -",Data((1,2),"tuple_test")
    print 
    print "part 3"
    d1 = Data((1,2,3),"D1")
    print "data 1 -", d1
    d2 = d1.copy()
    print "data 2 (copy of D1) -", d2
    d1.content = [7,6]
    print "altered D1 -",d1
    print "data 2 -",d2
    print "End of data tests..."
if GROUPS:
    # GROUP TESTS
    print
    print "Group tests"
    print "Part 1"
    g = Group()
    print "Blank group -", g
    print "simple type -", Group(1)
    print "Incremental feed 1-"
    g = Group()
    for i in range(5):
        g.add_data(i)
        print "\t"+str(g)
    g = Group()
    x = [(1,2),(2,3),(3,4),(5,6)]
    print "Incremental feed 2-"
    for i in x:
        g.add_data(i)
        print "\t"+str(g)
    print "Lists of int 1 -", Group([1,2,3,4,5])
    print "Lists of int 2 -", Group((1,2,3,4,5))
    print "Lists of coord 2D lists -", Group(([1,2,3,4],[5,6,7,8]))
    print "Lists of coord 3D lists -", Group(([1,2,3,4],[5,6,7,8],[9,10,11,12]))
    print "Lists of 2D points -", Group([(1,2), (2,3), (4,5)])
    print "Lists of 3D points -", Group([(1,2,3), (2,3,4), (4,5,6)])
    print
    print "Part 2"
    g = Group()
    g.name = "blanks"
    print "Blank group -", g
    print "simple type -", Group(1,"simple")
    print "Incremental feed 1-"
    g = Group(name="inc int")
    for i in range(5):
        g.add_data(i)
        print "\t"+str(g)

    g = Group(name="inc list")
    x = [(1,2),(2,3),(3,4),(5,6)]
    print "Incremental feed 2-"
    for i in x:
        g.add_data(i)
        print "\t"+str(g)
        
    print "Lists of int 1 -", Group([1,2,3,4,5],"int list1")
    print "Lists of int 2 -", Group((1,2,3,4,5),"int list2")
    print "Lists of coord 2D lists -", Group(([1,2,3,4],[5,6,7,8]),"2D pts")
    print "Lists of coord 3D lists -", Group(([1,2,3,4],[5,6,7,8],[9,10,11,12]),"3D pts")
    print "Lists of 2D points -", Group([(1,2), (2,3), (4,5)], "2D Pts")
    print "Lists of 3D points -", Group([(1,2,3), (2,3,4), (4,5,6)],"3d Pts")
    print
    print "Part 3"
    g = Group()
    y = lambda x:x**2
    g.x_range = [1,10]
    g.data_list = y
    print "Group range with list 1:",g.x_range
    print "group",g
    g.x_range = range(1,7)
    g.data_list = y
    print "Group range with list 2:",g.x_range
    print "group",g
    g.x_range = (1,10)
    g.data_list = y
    print "Group range with tuple 1:",g.x_range
    print "group",g
    g.x_range = (1,2,10)
    g.data_list = y
    print "Group range with tuple 2:",g.x_range
    print "group",g
    
if SERIES:
    # SERIES TEST
    print
    print "Series Testes"
    print "Part 1"
    s = Serie()
    s.add_group([1,2,3])
    print "Adding Groups -",s

    s = Serie()
    s.add_group(Group([(7,5),(8,9)],"group1"))
    s.add_group(Group([(4,3),(1,2)],"group2"))
    print "Adding named groups -",s

    s = Serie()
    s.group_list = {"g1":[1,2,3],
               "g2":[3,5,4],
               "g3":[5,6,8]}
    print "Using Dictionary -",s

    s = Serie()
    s.group_list = [[(1,2),(2,3)],[(4,5),(5,6)],[(7,8),(8,9)]]
    print "Groups of points -",s
    s = Serie([[1,2,3],[4,5,6]],"Serie1")
    print "Named simple goup -",s

    #Caso 1: 3 grupos com nomes e cada grupo com uma swrie de numeros
    data = { "john" : [-5, -2, 0, 1, 3], "mary" : [0, 0, 3, 5, 2], "philip" : [-2, -3, -4, 2, 1] }
    s = Serie(data,"dic2")
    print "Dic declaration test -",s
    # >>> dic2 ["philip ['-2', '-3', '-4', '2', '1']", "john ['-5', '-2', '0', '1', '3']", "mary ['0', '0', '3', '5', '2']"]

    #Caso 3: 4 grupos e cada um com nome com numero
    data = {"john" : 700, "mary" : 100, "philip" : 100 , "suzy" : 50, "yman" : 50}
    s = Serie(data, "simple dic")
    print "Dic only with numbers -",s
    # >>> simple dic ["yman ['50']", "philip ['100']", "john ['700']", "mary ['100']", "suzy ['50']"]

    #Caso 4: um grupo com uma serie de numeros
    data = [ 0, 1, 3.5, 8.5, 9, 0, 10, 10, 2, 1 ]
    s = Serie(data, "num group")
    print "Only one group of numbers -",s
    # >>> num group ["['0']", "['1']", "['3.5']", "['8.5']", "['9']", "['0']", "['10']", "['10']", "['2']", "['1']"]
    # Criar verificacao pra criar apenas um grupo

    #Caso 5: grupos com series de pontos
    data = [ [ (0,0), (-2,10), (0,15), (1,5), (2,0), (3,-10), (3,5) ],
             [ (0,2), (-2,12), (0,17), (1,7), (2,2), (3,-8),  (3,7) ]  ]
    s = Serie(data, "pts groups")
    print "groups of points -",s
    # >>> pts groups ["['(0, 0)', '(-2, 10)', '(0, 15)', '(1, 5)', '(2, 0)', '(3, -10)', '(3, 5)']", "['(0, 2)', '(-2, 12)', '(0, 17)', '(1, 7)', '(2, 2)', '(3, -8)', '(3, 7)']"]

    #Caso 6: grupos com series de pontos e nomes
    data = { 'data1' : [ (0,0), (0,10), (0,15), (1,5), (2,0), (3,-10), (3,5) ],
             'data2' : [ (2,2), (2,12), (2,17), (3,7), (4,2), (5,-8),  (5,7) ]}
    s = Serie(data, "points dic")
    print "Dic with groups of named points -",s
    # >>> points dic ["data1 ['(0, 0)', '(0, 10)', '(0, 15)', '(1, 5)', '(2, 0)', '(3, -10)', '(3, 5)']", "data2 ['(2, 2)', '(2, 12)', '(2, 17)', '(3, 7)', '(4, 2)', '(5, -8)', '(5, 7)']"]

    #Caso 7: grupos com listas de coordenadas x e y
    data = [ [ [0, 0, 0, 1, 2, 3, 3], [0, 10, 15, 5, 0, -10, 5] ],
             [ [2, 2, 2, 3, 4, 5, 5], [2, 12, 17, 7, 2, -8, 7] ]  ]
    s = Serie(data, "coord 1")
    print "2 groups of coord lists -",s
    # >>> Caso 7 ["['(0, 0)', '(0, 10)', '(0, 15)', '(1, 5)', '(2, 0)', '(3, -10)', '(3, 5)']", "['(2, 2)', '(2, 12)', '(2, 17)', '(3, 7)', '(4, 2)', '(5, -8)', '(5, 7)']"]

    #Caso 8: grupos com listas de coordenadas x e y e nome para o grupo
    data = { 'data1' : [ [0, 0, 0, 1, 2, 3, 3], [0, 10, 15, 5, 0, -10, 5] ],
             'data2' : [ [2, 2, 2, 3, 4, 5, 5], [2, 12, 17, 7, 2, -8, 7] ]  }
    s = Serie(data, "Caso 8")
    print s
    # >>> Caso 8 ["data1 ['(0, 0)', '(0, 10)', '(0, 15)', '(1, 5)', '(2, 0)', '(3, -10)', '(3, 5)']", "data2 ['(2, 2)', '(2, 12)', '(2, 17)', '(3, 7)', '(4, 2)', '(5, -8)', '(5, 7)']"]

    # TODO
    # Caso 9: lista de lambdas
    #data = [ lambda x : 1, lambda y : y**2, lambda z : -z**2 ]
    #s = Serie(data, "lab")
    #print s
    # Ocorre erro pois temos que especificar o x_range para que os valores de lambda sejam gerados!






