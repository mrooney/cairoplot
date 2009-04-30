#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Series.py
#
# Copyright (c) 2008 Rodrigo Moreira Araújo
#
# Author: Rodrigo Moreiro Araujo <alf.rodrigo@gmail.com>
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

# Contributor: Magnun Leno da Silva <magnun.leno@gmail.com>

#TODO: Add the x_lables and y_labels to the Series structure
#   Update: adde this feature using the CairoPlot class
#
#TODO: Test the basics of CairoPlot class
#
#TODO: Change range to float

from Series import Serie, Group, Data, LISTTYPES, NUMTYPES, STRTYPES

__version__ = 1.2

import cairo
import math
import random

HORZ = 0
VERT = 1
NORM = 2

COLORS = {"red"    : (1.0,0.0,0.0,1.0), "lime"    : (0.0,1.0,0.0,1.0), "blue"   : (0.0,0.0,1.0,1.0),
          "maroon" : (0.5,0.0,0.0,1.0), "green"   : (0.0,0.5,0.0,1.0), "navy"   : (0.0,0.0,0.5,1.0),
          "yellow" : (1.0,1.0,0.0,1.0), "magenta" : (1.0,0.0,1.0,1.0), "cyan"   : (0.0,1.0,1.0,1.0),
          "orange" : (1.0,0.5,0.0,1.0), "white"   : (1.0,1.0,1.0,1.0), "black"  : (0.0,0.0,0.0,1.0)}

THEMES = {"black_red"         : [(0.0,0.0,0.0,1.0), (1.0,0.0,0.0,1.0)],
          "red_green_blue"    : [(1.0,0.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,0.0,1.0,1.0)],
          "red_orange_yellow" : [(1.0,0.2,0.0,1.0), (1.0,0.7,0.0,1.0), (1.0,1.0,0.0,1.0)],
          "yellow_orange_red" : [(1.0,1.0,0.0,1.0), (1.0,0.7,0.0,1.0), (1.0,0.2,0.0,1.0)],
          "rainbow"           : [(1.0,0.0,0.0,1.0), (1.0,0.5,0.0,1.0), (1.0,1.0,0.0,1.0), (0.0,1.0,0.0,1.0), (0.0,0.0,1.0,1.0), (0.3, 0.0, 0.5,1.0), (0.5, 0.0, 1.0, 1.0)]}

def colors_from_theme( theme, series_length ):
    colors = []
    if theme not in THEMES.keys() :
        raise Exception, "Theme not defined" 
    color_steps = THEMES[theme]
    n_colors = len(color_steps)
    if series_length <= n_colors:
        colors = [color for color in color_steps[0:n_colors]]
    else:
        iterations = [(series_length - n_colors)/(n_colors - 1) for i in color_steps[:-1]]
        over_iterations = (series_length - n_colors) % (n_colors - 1)
        for i in range(n_colors - 1):
            if over_iterations <= 0:
                break
            iterations[i] += 1
            over_iterations -= 1
        for index,color in enumerate(color_steps[:-1]):
            colors.append(color)
            if iterations[index] == 0:
                continue
            next_color = color_steps[index+1]
            color_step = ((next_color[0] - color[0])/(iterations[index] + 1),
                          (next_color[1] - color[1])/(iterations[index] + 1),
                          (next_color[2] - color[2])/(iterations[index] + 1),
                          (next_color[3] - color[3])/(iterations[index] + 1))
            for i in range( iterations[index] ):
                colors.append((color[0] + color_step[0]*(i+1), 
                               color[1] + color_step[1]*(i+1), 
                               color[2] + color_step[2]*(i+1),
                               color[3] + color_step[3]*(i+1)))
        colors.append(color_steps[-1])
    return colors
        

def other_direction(direction):
    "explicit is better than implicit"
    if direction == HORZ:
        return VERT
    else:
        return HORZ

#Class definition

class Plot(object):
    def __init__(self, 
                 surface=None,
                 data=None,
                 width=640,
                 height=480,
                 background=None,
                 border = 0,
                 x_labels = None,
                 y_labels = None,
                 series_colors = None):
        random.seed(2)
        self.create_surface(surface, width, height)
        self.dimensions = {}
        self.dimensions[HORZ] = width
        self.dimensions[VERT] = height
        self.context = cairo.Context(self.surface)
        self.labels={}
        self.labels[HORZ] = x_labels
        self.labels[VERT] = y_labels
        self.load_series(data, x_labels, y_labels, series_colors)
        self.font_size = 10
        self.set_background (background)
        self.border = border
        self.borders = {}
        self.line_color = (0.5, 0.5, 0.5)
        self.line_width = 0.5
        self.label_color = (0.0, 0.0, 0.0)
        self.grid_color = (0.8, 0.8, 0.8)
    
    def create_surface(self, surface, width=None, height=None):
        self.filename = None
        if isinstance(surface, cairo.Surface):
            self.surface = surface
            return
        if not type(surface) in STRTYPES: 
            raise TypeError("Surface should be either a Cairo surface or a filename, not %s" % surface)
        sufix = surface.rsplit(".")[-1].lower()
        self.filename = surface
        if sufix == "png":
            self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        elif sufix == "ps":
            self.surface = cairo.PSSurface(surface, width, height)
        elif sufix == "pdf":
            self.surface = cairo.PSSurface(surface, width, height)
        else:
            if sufix != "svg":
                self.filename += ".svg"
            self.surface = cairo.SVGSurface(self.filename, width, height)

    def commit(self):
        try:
            self.context.show_page()
            if self.filename and self.filename.endswith(".png"):
                self.surface.write_to_png(self.filename)
            else:
                self.surface.finish()
        except cairo.Error:
            pass
        
    def load_series (self, data, x_labels=None, y_labels=None, series_colors=None):
        # Convert Data or Group instance to Serie
        if isinstance(data, Data) or isinstance(data, Group):
            data = Serie(data)
        # Not an instance of Series 
        if not isinstance(data, Serie):
            data = Serie(data)
            
        self.series_labels = []
        self.data = data
        for group in data:
            if group.name is not None:
                self.series_labels.append(group.name)
            elif len(self.series_labels) > 0:
                self.series_labels.append('_'+str(data.group_list.index(group)))
        
        if self.data[0][0].type is list and len(self.series_labels) is 0:
            self.series_labels = range(len(self.data))
            
            
        self.series_widths = [1.0 for series in self.data]
        self.process_colors( series_colors )
        
    def process_colors( self, series_colors, length = None ):
        #series_colors might be None, a theme, a string of colors names or a string of color tuples
        if length is None :
            length = len( self.data )
        #no colors passed
        if not series_colors:
            #Randomize colors
            self.series_colors = [ [random.random() for i in range(3)] + [1.0]  for series in range( length ) ]
        else:
            #Theme pattern
            if not hasattr( series_colors, "__iter__" ):
                theme = series_colors
                self.series_colors = colors_from_theme( theme.lower(), length )
            #List
            else:
                self.series_colors = series_colors
                for index, color in enumerate( self.series_colors ):
                    #list of color names
                    if not hasattr(color, "__iter__"):
                        self.series_colors[index] = COLORS[color.lower()]
                    #list of rgb colors instead of rgba
                    elif len( color ) == 3 :
                        self.series_colors[index] += tuple( [1.0] )

    def get_width(self):
        return self.surface.get_width()
    
    def get_height(self):
        return self.surface.get_height()

    def set_background(self, background):
        if background is None:
            self.background = cairo.LinearGradient(self.dimensions[HORZ] / 2, 0, self.dimensions[HORZ] / 2, self.dimensions[VERT])
            self.background.add_color_stop_rgba(0,1.0,1.0,1.0,1.0)
            self.background.add_color_stop_rgba(1.0,0.9,0.9,0.9,1.0)
        else:
            if type(background) in (cairo.LinearGradient, tuple):
                self.background = background
            else:
                raise TypeError ("Background should be either cairo.LinearGradient or a 3-tuple, not %s" % type(background))
        
    def render_background(self):
        if isinstance(self.background, cairo.LinearGradient):
            self.context.set_source(self.background)
        else:
            self.context.set_source_rgba(*self.background)
        self.context.rectangle(0,0, self.dimensions[HORZ], self.dimensions[VERT])
        self.context.fill()
        
    def render_bounding_box(self):
        self.context.set_source_rgba(*self.line_color)
        self.context.set_line_width(self.line_width)
        self.context.rectangle(self.border, self.border,
                               self.dimensions[HORZ] - 2 * self.border,
                               self.dimensions[VERT] - 2 * self.border)
        self.context.stroke()

    def render(self):
        pass

class ScatterPlot( Plot ):
    def __init__(self, 
                 surface=None,
                 data=None,
                 errorx=None,
                 errory=None,
                 width=640,
                 height=480,
                 background=None,
                 border=0, 
                 axis = False,
                 dash = False,
                 discrete = False,
                 dots = 0,
                 grid = False,
                 series_legend = False,
                 x_labels = None,
                 y_labels = None,
                 x_bounds = None,
                 y_bounds = None,
                 z_bounds = None,
                 x_title  = None,
                 y_title  = None,
                 series_colors = None,
                 circle_colors = None ):
        
        self.bounds = {}
        self.bounds[HORZ] = x_bounds
        self.bounds[VERT] = y_bounds
        self.bounds[NORM] = z_bounds
        self.titles = {}
        self.titles[HORZ] = x_title
        self.titles[VERT] = y_title
        self.max_value = {}
        self.axis = axis
        self.discrete = discrete
        self.dots = dots
        self.grid = grid
        self.series_legend = series_legend
        self.variable_radius = False
        self.x_label_angle = math.pi / 2.5
        self.circle_colors = circle_colors
        
        Plot.__init__(self, surface, data, width, height, background, border, x_labels, y_labels, series_colors)
        
        self.dash = None
        if dash:
            if hasattr(dash, "keys"):
                self.dash = [dash[key] for key in self.series_labels]
            elif max([hasattr(item,'__delitem__') for item in data]) :
                self.dash = dash
            else:
                self.dash = [dash]
                
        self.load_errors(errorx, errory)
    
    def load_series(self, data, x_labels = None, y_labels = None, series_colors=None):
        if not isinstance(data, Serie):
            data = Serie(data)
            
        for group in data:
            for item in group:
                if len(item) is 3:
                    self.variable_radius = True
                    
        Plot.load_series(self, data, x_labels, y_labels, series_colors)
        self.calc_boundaries()
        self.calc_labels()
    
    def load_errors(self, errorx, errory):
        self.errors = None
        if errorx == None and errory == None:
            return
        self.errors = {}
        self.errors[HORZ] = None
        self.errors[VERT] = None
        #asimetric errors
        if errorx and hasattr(errorx[0], "__delitem__"):
            self.errors[HORZ] = errorx
        #simetric errors
        elif errorx:
            self.errors[HORZ] = [errorx]
        #asimetric errors
        if errory and hasattr(errory[0], "__delitem__"):
            self.errors[VERT] = errory
        #simetric errors
        elif errory:
            self.errors[VERT] = [errory]
    
    def calc_labels(self):
        if not self.labels[HORZ]:
            amplitude = self.bounds[HORZ][1] - self.bounds[HORZ][0]
            if amplitude % 10: #if horizontal labels need floating points
                self.labels[HORZ] = ["%.2lf" % (float(self.bounds[HORZ][0] + (amplitude * i / 10.0))) for i in range(11) ]
            else:
                self.labels[HORZ] = ["%d" % (int(self.bounds[HORZ][0] + (amplitude * i / 10.0))) for i in range(11) ]
        if not self.labels[VERT]:
            amplitude = self.bounds[VERT][1] - self.bounds[VERT][0]
            if amplitude % 10: #if vertical labels need floating points
                self.labels[VERT] = ["%.2lf" % (float(self.bounds[VERT][0] + (amplitude * i / 10.0))) for i in range(11) ]
            else:
                self.labels[VERT] = ["%d" % (int(self.bounds[VERT][0] + (amplitude * i / 10.0))) for i in range(11) ]

    def calc_extents(self, direction):
        self.context.set_font_size(self.font_size * 0.8)
        self.max_value[direction] = max(self.context.text_extents(item)[2] for item in self.labels[direction])
        self.borders[other_direction(direction)] = self.max_value[direction] + self.border + 20

    def calc_boundaries(self):
        #HORZ = 0, VERT = 1, NORM = 2
        min_data_value = [0,0,0]
        max_data_value = [0,0,0]
        for group in self.data:
            for point in group:
                for index, item in enumerate(point.content):
                    if item > max_data_value[index]:
                        max_data_value[index] = item
                    elif item < min_data_value[index]:
                        min_data_value[index] = item
                
        if not self.bounds[HORZ]:
            self.bounds[HORZ] = (min_data_value[HORZ], max_data_value[HORZ])
        if not self.bounds[VERT]:
            self.bounds[VERT] = (min_data_value[VERT], max_data_value[VERT])
        if not self.bounds[NORM]:
            self.bounds[NORM] = (min_data_value[NORM], max_data_value[NORM])

    def calc_all_extents(self):
        self.calc_extents(HORZ)
        self.calc_extents(VERT)

        self.plot_height = self.dimensions[VERT] - 2 * self.borders[VERT]
        self.plot_width = self.dimensions[HORZ] - 2* self.borders[HORZ]
        
        self.plot_top = self.dimensions[VERT] - self.borders[VERT]
                
    def calc_steps(self):
        #Calculates all the x, y, z and color steps
        series_amplitude = [self.bounds[index][1] - self.bounds[index][0] for index in range(3)]

        if series_amplitude[HORZ]:
            self.horizontal_step = float (self.plot_width) / series_amplitude[HORZ]
        else:
            self.horizontal_step = 0.00
            
        if series_amplitude[VERT]:
            self.vertical_step = float (self.plot_height) / series_amplitude[VERT]
        else:
            self.vertical_step = 0.00

        if series_amplitude[NORM]:
            if self.variable_radius:
                self.z_step = float (self.bounds[NORM][1]) / series_amplitude[NORM]
            if self.circle_colors:
                self.circle_color_step = tuple([float(self.circle_colors[1][i]-self.circle_colors[0][i])/series_amplitude[NORM] for i in range(4)])
        else:
            self.z_step = 0.00
            self.circle_color_step = ( 0.0, 0.0, 0.0, 0.0 )
    
    def get_circle_color(self, value):
        return tuple( [self.circle_colors[0][i] + value*self.circle_color_step[i] for i in range(4)] )
    
    def render(self):
        self.calc_all_extents()
        self.calc_steps()
        self.render_background()
        self.render_bounding_box()
        if self.axis:
            self.render_axis()
        if self.grid:
            self.render_grid()
        self.render_labels()
        self.render_plot()
        if self.errors:
            self.render_errors()
        if self.series_legend and self.series_labels:
            self.render_legend()
            
    def render_axis(self):
        #Draws both the axis lines and their titles
        cr = self.context
        cr.set_source_rgba(*self.line_color)
        cr.move_to(self.borders[HORZ], self.dimensions[VERT] - self.borders[VERT])
        cr.line_to(self.borders[HORZ], self.borders[VERT])
        cr.stroke()

        cr.move_to(self.borders[HORZ], self.dimensions[VERT] - self.borders[VERT])
        cr.line_to(self.dimensions[HORZ] - self.borders[HORZ], self.dimensions[VERT] - self.borders[VERT])
        cr.stroke()

        cr.set_source_rgba(*self.label_color)
        self.context.set_font_size( 1.2 * self.font_size )
        if self.titles[HORZ]:
            title_width,title_height = cr.text_extents(self.titles[HORZ])[2:4]
            cr.move_to( self.dimensions[HORZ]/2 - title_width/2, self.borders[VERT] - title_height/2 )
            cr.show_text( self.titles[HORZ] )

        if self.titles[VERT]:
            title_width,title_height = cr.text_extents(self.titles[VERT])[2:4]
            cr.move_to( self.dimensions[HORZ] - self.borders[HORZ] + title_height/2, self.dimensions[VERT]/2 - title_width/2)
            cr.rotate( math.pi/2 )
            cr.show_text( self.titles[VERT] )
            cr.rotate( -math.pi/2 )
        
    def render_grid(self):
        cr = self.context
        horizontal_step = float( self.plot_height ) / ( len( self.labels[VERT] ) - 1 )
        vertical_step = float( self.plot_width ) / ( len( self.labels[HORZ] ) - 1 )
        
        x = self.borders[HORZ] + vertical_step
        y = self.plot_top - horizontal_step
        
        for label in self.labels[HORZ][:-1]:
            cr.set_source_rgba(*self.grid_color)
            cr.move_to(x, self.dimensions[VERT] - self.borders[VERT])
            cr.line_to(x, self.borders[VERT])
            cr.stroke()
            x += vertical_step
        for label in self.labels[VERT][:-1]:
            cr.set_source_rgba(*self.grid_color)
            cr.move_to(self.borders[HORZ], y)
            cr.line_to(self.dimensions[HORZ] - self.borders[HORZ], y)
            cr.stroke()
            y -= horizontal_step
    
    def render_labels(self):
        self.context.set_font_size(self.font_size * 0.8)
        self.render_horz_labels()
        self.render_vert_labels()
    
    def render_horz_labels(self):
        cr = self.context
        step = float( self.plot_width ) / ( len( self.labels[HORZ] ) - 1 )
        x = self.borders[HORZ]
        for item in self.labels[HORZ]:
            cr.set_source_rgba(*self.label_color)
            width = cr.text_extents(item)[2]
            cr.move_to(x, self.dimensions[VERT] - self.borders[VERT] + 5)
            cr.rotate(self.x_label_angle)
            cr.show_text(item)
            cr.rotate(-self.x_label_angle)
            x += step
    
    def render_vert_labels(self):
        cr = self.context
        step = ( self.plot_height ) / ( len( self.labels[VERT] ) - 1 )
        y = self.plot_top
        for item in self.labels[VERT]:
            cr.set_source_rgba(*self.label_color)
            width = cr.text_extents(item)[2]
            cr.move_to(self.borders[HORZ] - width - 5,y)
            cr.show_text(item)
            y -= step

    def render_legend(self):
        cr = self.context
        cr.set_font_size(self.font_size)
        cr.set_line_width(self.line_width)
        
        widest_word = max(self.series_labels, key = lambda item: self.context.text_extents(item)[2])
        tallest_word = max(self.series_labels, key = lambda item: self.context.text_extents(item)[3])
        max_width = self.context.text_extents(widest_word)[2]
        max_height = self.context.text_extents(tallest_word)[3] * 1.1
        
        color_box_height = max_height / 2
        color_box_width = color_box_height * 2
        
        #Draw a bounding box
        bounding_box_width = max_width + color_box_width + 15
        bounding_box_height = (len(self.series_labels)+0.5) * max_height
        cr.set_source_rgba(1,1,1)
        cr.rectangle(self.dimensions[HORZ] - self.borders[HORZ] - bounding_box_width, self.borders[VERT],
                            bounding_box_width, bounding_box_height)
        cr.fill()
        
        cr.set_source_rgba(*self.line_color)
        cr.set_line_width(self.line_width)
        cr.rectangle(self.dimensions[HORZ] - self.borders[HORZ] - bounding_box_width, self.borders[VERT],
                            bounding_box_width, bounding_box_height)
        cr.stroke()

        for idx,key in enumerate(self.series_labels):
            #Draw color box
            cr.set_source_rgba(*self.series_colors[idx])
            cr.rectangle(self.dimensions[HORZ] - self.borders[HORZ] - max_width - color_box_width - 10, 
                                self.borders[VERT] + color_box_height + (idx*max_height) ,
                                color_box_width, color_box_height)
            cr.fill()
            
            cr.set_source_rgba(0, 0, 0)
            cr.rectangle(self.dimensions[HORZ] - self.borders[HORZ] - max_width - color_box_width - 10, 
                                self.borders[VERT] + color_box_height + (idx*max_height),
                                color_box_width, color_box_height)
            cr.stroke()
            
            #Draw series labels
            cr.set_source_rgba(0, 0, 0)
            cr.move_to(self.dimensions[HORZ] - self.borders[HORZ] - max_width - 5, self.borders[VERT] + ((idx+1)*max_height))
            cr.show_text(key)

    def render_errors(self):
        cr = self.context
        cr.rectangle(self.borders[HORZ], self.borders[VERT], self.plot_width, self.plot_height)
        cr.clip()
        radius = self.dots
        x0 = self.borders[HORZ] - self.bounds[HORZ][0]*self.horizontal_step
        y0 = self.borders[VERT] - self.bounds[VERT][0]*self.vertical_step
        for index, serie in enumerate(self.data):
            cr.set_source_rgba(*self.series_colors[index])
            for number, _tuple in enumerate(serie):
                x = x0 + self.horizontal_step * _tuple[0]
                y = self.dimensions[VERT] - y0 - self.vertical_step * _tuple[1]
                if self.errors[HORZ]:
                    cr.move_to(x, y)
                    x1 = x - self.horizontal_step * self.errors[HORZ][0][number]
                    cr.line_to(x1, y)
                    cr.line_to(x1, y - radius)
                    cr.line_to(x1, y + radius)
                    cr.stroke()
                if self.errors[HORZ] and len(self.errors[HORZ]) == 2:
                    cr.move_to(x, y)
                    x1 = x + self.horizontal_step * self.errors[HORZ][1][number]
                    cr.line_to(x1, y)
                    cr.line_to(x1, y - radius)
                    cr.line_to(x1, y + radius)
                    cr.stroke()
                if self.errors[VERT]:
                    cr.move_to(x, y)
                    y1 = y + self.vertical_step   * self.errors[VERT][0][number]
                    cr.line_to(x, y1)
                    cr.line_to(x - radius, y1)
                    cr.line_to(x + radius, y1)
                    cr.stroke()
                if self.errors[VERT] and len(self.errors[VERT]) == 2:
                    cr.move_to(x, y)
                    y1 = y - self.vertical_step   * self.errors[VERT][1][number]
                    cr.line_to(x, y1)
                    cr.line_to(x - radius, y1)
                    cr.line_to(x + radius, y1)
                    cr.stroke()
                
                
    def render_plot(self):
        cr = self.context
        if self.discrete:
            #exit()
            cr.rectangle(self.borders[HORZ], self.borders[VERT], self.plot_width, self.plot_height)
            cr.clip()
            x0 = self.borders[HORZ] - self.bounds[HORZ][0]*self.horizontal_step
            y0 = self.borders[VERT] - self.bounds[VERT][0]*self.vertical_step
            radius = self.dots
            for number, serie in  enumerate (self.data):
                cr.set_source_rgba(*self.series_colors[number])
                for _tuple in serie :
                    if self.variable_radius:
                        radius = _tuple.content[2]*self.z_step
                        if self.circle_colors:
                            cr.set_source_rgba( *self.get_circle_color( _tuple.content[2]) )
                    x = x0 + self.horizontal_step*_tuple.content[0]
                    y = y0 + self.vertical_step*_tuple.content[1]
                    cr.arc(x, self.dimensions[VERT] - y, radius, 0, 2*math.pi)
                    cr.fill()
        else:
            #exit()
            cr.rectangle(self.borders[HORZ], self.borders[VERT], self.plot_width, self.plot_height)
            cr.clip()
            x0 = self.borders[HORZ] - self.bounds[HORZ][0]*self.horizontal_step
            y0 = self.borders[VERT] - self.bounds[VERT][0]*self.vertical_step
            radius = self.dots
            for number, serie in  enumerate (self.data):
                last_tuple = None
                cr.set_source_rgba(*self.series_colors[number])
                for _tuple in serie :
                    x = x0 + self.horizontal_step*_tuple.content[0]
                    y = y0 + self.vertical_step*_tuple.content[1]
                    if self.dots:
                        if self.variable_radius:
                            radius = _tuple.content[2]*self.z_step
                        cr.arc(x, self.dimensions[VERT] - y, radius, 0, 2*math.pi)
                        cr.fill()
                    if last_tuple :
                        old_x = x0 + self.horizontal_step*last_tuple.content[0]
                        old_y = y0 + self.vertical_step*last_tuple.content[1]
                        cr.move_to( old_x, self.dimensions[VERT] - old_y )
                        cr.line_to( x, self.dimensions[VERT] - y)
                        cr.set_line_width(self.series_widths[number])

                        # Display line as dash line 
                        if self.dash and self.dash[number]:
                            s = self.series_widths[number]
                            cr.set_dash([s*3, s*3], 0)
    
                        cr.stroke()
                        cr.set_dash([])
                    last_tuple = _tuple.copy()



class DotLinePlot(ScatterPlot):
    def __init__(self, 
                 surface=None,
                 data=None,
                 width=640,
                 height=480,
                 background=None,
                 border=0, 
                 axis = False,
                 dash = False,
                 dots = 0,
                 grid = False,
                 series_legend = False,
                 x_labels = None,
                 y_labels = None,
                 x_bounds = None,
                 y_bounds = None,
                 x_title  = None,
                 y_title  = None,
                 series_colors = None):
        
        ScatterPlot.__init__(self, surface, data, None, None, width, height, background, border, 
                             axis, dash, False, dots, grid, series_legend, x_labels, y_labels,
                             x_bounds, y_bounds, None, x_title, y_title, series_colors, None )


    def load_series(self, data, x_labels = None, y_labels = None, series_colors=None):
        Plot.load_series(self, data, x_labels, y_labels, series_colors)
        self.calc_boundaries()
        self.calc_labels()
        
    def calc_boundaries(self):
        #HORZ = 0, VERT = 1, NORM = 2
        min_data_value = [0,0,0]
        max_data_value = [0,0,0]
        
        if self.data[0][0].type in NUMTYPES:
            for group in self.data:
                for x, y in enumerate(group):
                    for index, item in enumerate([x,y.content]):
                        if item > max_data_value[index]:
                            max_data_value[index] = item
                        elif item < min_data_value[index]:
                            min_data_value[index] = item
                            
        else:
            for group in self.data:
                for point in group:
                    for index, item in enumerate(point.content):
                        if item > max_data_value[index]:
                            max_data_value[index] = item
                        elif item < min_data_value[index]:
                            min_data_value[index] = item  
        
        if not self.bounds[HORZ]:
            self.bounds[HORZ] = (min_data_value[HORZ], max_data_value[HORZ])
        if not self.bounds[VERT]:
            self.bounds[VERT] = (min_data_value[VERT], max_data_value[VERT])
        if not self.bounds[NORM]:
            self.bounds[NORM] = (min_data_value[NORM], max_data_value[NORM])
            
    
    def render_plot(self):
        cr = self.context
        if self.discrete:
            cr.rectangle(self.borders[HORZ], self.borders[VERT], self.plot_width, self.plot_height)
            cr.clip()
            x0 = self.borders[HORZ] - self.bounds[HORZ][0]*self.horizontal_step
            y0 = self.borders[VERT] - self.bounds[VERT][0]*self.vertical_step
            radius = self.dots
            for number, serie in  enumerate (self.data):
                cr.set_source_rgba(*self.series_colors[number])
                for _tuple in serie :
                    if self.variable_radius:
                        radius = _tuple.content[2]*self.z_step
                        if self.circle_colors:
                            cr.set_source_rgba( *self.get_circle_color( _tuple.content[2]) )
                    x = x0 + self.horizontal_step*_tuple.content[0]
                    y = y0 + self.vertical_step*_tuple.content[1]
                    cr.arc(x, self.dimensions[VERT] - y, radius, 0, 2*math.pi)
                    cr.fill()
        else:
            cr.rectangle(self.borders[HORZ], self.borders[VERT], self.plot_width, self.plot_height)
            cr.clip()
            x0 = self.borders[HORZ] - self.bounds[HORZ][0]*self.horizontal_step
            y0 = self.borders[VERT] - self.bounds[VERT][0]*self.vertical_step
            radius = self.dots
            for number, serie in  enumerate (self.data):
                last_tuple = None
                cr.set_source_rgba(*self.series_colors[number])
                for _tuple in enumerate(serie) :
                    x = x0 + self.horizontal_step*_tuple[0]
                    y = y0 + self.vertical_step*_tuple[1].content
                    if self.dots:
                        cr.arc(x, self.dimensions[VERT] - y, radius, 0, 2*math.pi)
                        cr.fill()
                    if last_tuple :
                        old_x = x0 + self.horizontal_step*last_tuple[0]
                        old_y = y0 + self.vertical_step*last_tuple[1].content
                        cr.move_to( old_x, self.dimensions[VERT] - old_y )
                        cr.line_to( x, self.dimensions[VERT] - y)
                        cr.set_line_width(self.series_widths[number])
                    
                        # Display line as dash line 
                        if self.dash and self.dash[number]:
                            s = self.series_widths[number]
                            cr.set_dash([s*3, s*3], 0)
                    
                        cr.stroke()
                        cr.set_dash([])
                    last_tuple = _tuple

class GanttChart (Plot) :
    def __init__(self,
                 surface = None,
                 data = None,
                 width = 640,
                 height = 480,
                 y_labels = None,
                 colors = None):
        self.bounds = {}
        self.max_value = {}
        Plot.__init__(self, surface, data, width, height,  x_labels = None, y_labels = y_labels, series_colors = colors)

    def load_series(self, data, x_labels=None, y_labels=None, series_colors=None):
        Plot.load_series(self, data, x_labels, y_labels, series_colors)
        self.calc_boundaries()

    def calc_boundaries(self):
        self.bounds[HORZ] = (0,len(self.data))
        for item in self.data:
            if hasattr(item, "__delitem__"):
                for sub_item in item:
                    end_pos = max(sub_item)
            else:
                end_pos = max(item)
        self.bounds[VERT] = (0,end_pos)

    def calc_extents(self, direction):
        self.max_value[direction] = 0
        if direction is HORZ:
            self.max_value[direction] = max(self.context.text_extents(group.name)[2] for group in self.data)
            print 'serie',self.max_value
            return
            
        if self.labels[direction]:
            self.max_value[direction] = max(self.context.text_extents(item)[2] for item in self.labels[direction])
        else:
            self.max_value[direction] = self.context.text_extents( str(self.bounds[direction][1] + 1) )[2]
            print self.max_value

    def calc_horz_extents(self):
        self.calc_extents(HORZ)
        self.borders[HORZ] = 100 + self.max_value[HORZ]

    def calc_vert_extents(self):
        self.calc_extents(VERT)
        self.borders[VERT] = self.dimensions[VERT]/(self.bounds[HORZ][1] + 1)

    def calc_steps(self):
        self.horizontal_step = (self.dimensions[HORZ] - self.borders[HORZ])/(len(self.labels[VERT]))
        self.vertical_step = self.borders[VERT]

    def render(self):
        self.calc_horz_extents()
        self.calc_vert_extents()
        self.calc_steps()
        self.render_background()

        self.render_labels()
        self.render_grid()
        self.render_plot()

    def render_background(self):
        cr = self.context
        cr.set_source_rgba(255,255,255)
        cr.rectangle(0,0,self.dimensions[HORZ], self.dimensions[VERT])
        cr.fill()
        for number,item in enumerate(self.data):
            linear = cairo.LinearGradient(self.dimensions[HORZ]/2, self.borders[VERT] + number*self.vertical_step, 
                                          self.dimensions[HORZ]/2, self.borders[VERT] + (number+1)*self.vertical_step)
            linear.add_color_stop_rgba(0,1.0,1.0,1.0,1.0)
            linear.add_color_stop_rgba(1.0,0.9,0.9,0.9,1.0)
            cr.set_source(linear)
            cr.rectangle(0,self.borders[VERT] + number*self.vertical_step,self.dimensions[HORZ],self.vertical_step)
            cr.fill()

    def render_grid(self):
        cr = self.context
        cr.set_source_rgba(0.7, 0.7, 0.7)
        cr.set_dash((1,0,0,0,0,0,1))
        cr.set_line_width(0.5)
        for number,label in enumerate(self.labels[VERT]):
            h = cr.text_extents(label)[3]
            cr.move_to(self.borders[HORZ] + number*self.horizontal_step, self.vertical_step/2 + h)
            cr.line_to(self.borders[HORZ] + number*self.horizontal_step, self.dimensions[VERT])
        cr.stroke()

    def render_labels(self):
        self.context.set_font_size(0.02 * self.dimensions[HORZ])

        self.render_horz_labels()
        self.render_vert_labels()

    def render_horz_labels(self):
        cr = self.context
        labels = self.labels[HORZ]
        for number, group in enumerate(self.data):
            label = ""
            if group.name is None:
                label = str(number)
            else:
                label = group.name
            cr.set_source_rgba(0.5, 0.5, 0.5)
            w,h = cr.text_extents(label)[2], cr.text_extents(label)[3]
            cr.move_to(40,self.borders[VERT] + number*self.vertical_step + self.vertical_step/2 + h/2)
            cr.show_text(label)
            
    def render_vert_labels(self):
        cr = self.context
        labels = self.labels[VERT]
        if not labels:
            labels = [str(i) for i in range(1, self.bounds[VERT][1] + 1)  ]
        for number,label in enumerate(labels):
            w,h = cr.text_extents(label)[2], cr.text_extents(label)[3]
            cr.move_to(self.borders[HORZ] + number*self.horizontal_step - w/2, self.vertical_step/2)
            cr.show_text(label)

    def render_rectangle(self, x0, y0, x1, y1, color):
        self.draw_shadow(x0, y0, x1, y1)
        self.draw_rectangle(x0, y0, x1, y1, color)

    def draw_rectangular_shadow(self, gradient, x0, y0, w, h):
        self.context.set_source(gradient)
        self.context.rectangle(x0,y0,w,h)
        self.context.fill()
    
    def draw_circular_shadow(self, x, y, radius, ang_start, ang_end, mult, shadow):
        gradient = cairo.RadialGradient(x, y, 0, x, y, 2*radius)
        gradient.add_color_stop_rgba(0, 0, 0, 0, shadow)
        gradient.add_color_stop_rgba(1, 0, 0, 0, 0)
        self.context.set_source(gradient)
        self.context.move_to(x,y)
        self.context.line_to(x + mult[0]*radius,y + mult[1]*radius)
        self.context.arc(x, y, 8, ang_start, ang_end)
        self.context.line_to(x,y)
        self.context.close_path()
        self.context.fill()

    def draw_rectangle(self, x0, y0, x1, y1, color):
        cr = self.context
        middle = (x0+x1)/2
        linear = cairo.LinearGradient(middle,y0,middle,y1)
        linear.add_color_stop_rgba(0,3.5*color[0]/5.0, 3.5*color[1]/5.0, 3.5*color[2]/5.0,1.0)
        linear.add_color_stop_rgba(1,*color)
        cr.set_source(linear)

        cr.arc(x0+5, y0+5, 5, 0, 2*math.pi)
        cr.arc(x1-5, y0+5, 5, 0, 2*math.pi)
        cr.arc(x0+5, y1-5, 5, 0, 2*math.pi)
        cr.arc(x1-5, y1-5, 5, 0, 2*math.pi)
        cr.rectangle(x0+5,y0,x1-x0-10,y1-y0)
        cr.rectangle(x0,y0+5,x1-x0,y1-y0-10)
        cr.fill()

    def draw_shadow(self, x0, y0, x1, y1):
        shadow = 0.4
        h_mid = (x0+x1)/2
        v_mid = (y0+y1)/2
        h_linear_1 = cairo.LinearGradient(h_mid,y0-4,h_mid,y0+4)
        h_linear_2 = cairo.LinearGradient(h_mid,y1-4,h_mid,y1+4)
        v_linear_1 = cairo.LinearGradient(x0-4,v_mid,x0+4,v_mid)
        v_linear_2 = cairo.LinearGradient(x1-4,v_mid,x1+4,v_mid)

        h_linear_1.add_color_stop_rgba( 0, 0, 0, 0, 0)
        h_linear_1.add_color_stop_rgba( 1, 0, 0, 0, shadow)
        h_linear_2.add_color_stop_rgba( 0, 0, 0, 0, shadow)
        h_linear_2.add_color_stop_rgba( 1, 0, 0, 0, 0)
        v_linear_1.add_color_stop_rgba( 0, 0, 0, 0, 0)
        v_linear_1.add_color_stop_rgba( 1, 0, 0, 0, shadow)
        v_linear_2.add_color_stop_rgba( 0, 0, 0, 0, shadow)
        v_linear_2.add_color_stop_rgba( 1, 0, 0, 0, 0)

        self.draw_rectangular_shadow(h_linear_1,x0+4,y0-4,x1-x0-8,8)
        self.draw_rectangular_shadow(h_linear_2,x0+4,y1-4,x1-x0-8,8)
        self.draw_rectangular_shadow(v_linear_1,x0-4,y0+4,8,y1-y0-8)
        self.draw_rectangular_shadow(v_linear_2,x1-4,y0+4,8,y1-y0-8)

        self.draw_circular_shadow(x0+4, y0+4, 4, math.pi, 3*math.pi/2, (-1,0), shadow)
        self.draw_circular_shadow(x1-4, y0+4, 4, 3*math.pi/2, 2*math.pi, (0,-1), shadow)
        self.draw_circular_shadow(x0+4, y1-4, 4, math.pi/2, math.pi, (0,1), shadow)
        self.draw_circular_shadow(x1-4, y1-4, 4, 0, math.pi/2, (1,0), shadow)

    def render_plot(self):
        for number,item in enumerate(self.data):
            for space in item:
                self.render_rectangle(self.borders[HORZ] + space.content[0]*self.horizontal_step, 
                                      self.borders[VERT] + number*self.vertical_step + self.vertical_step/4.0,
                                      self.borders[HORZ] + space.content[1]*self.horizontal_step, 
                                      self.borders[VERT] + number*self.vertical_step + 3.0*self.vertical_step/4.0, 
                                      self.series_colors[number])



# Function definition

def scatter_plot(name,
                 data   = None,
                 errorx = None,
                 errory = None,
                 width  = 640,
                 height = 480,
                 background = None,
                 border = 0,
                 axis = False,
                 dash = False,
                 discrete = False, 
                 dots = False,
                 grid = False,
                 series_legend = False,
                 x_labels = None,
                 y_labels = None,
                 x_bounds = None,
                 y_bounds = None,
                 z_bounds = None,
                 x_title  = None,
                 y_title  = None,
                 series_colors = None,
                 circle_colors = None):
    
    '''
        - Function to plot scatter data.
        
        - Parameters
        
        data - The values to be ploted might be passed in a two basic:
               list of points:       [(0,0), (0,1), (0,2)] or [(0,0,1), (0,1,4), (0,2,1)]
               lists of coordinates: [ [0,0,0] , [0,1,2] ] or [ [0,0,0] , [0,1,2] , [1,4,1] ]
               Notice that these kinds of that can be grouped in order to form more complex data 
               using lists of lists or dictionaries;
        series_colors - Define color values for each of the series
        circle_colors - Define a lower and an upper bound for the circle colors for variable radius
                        (3 dimensions) series
    '''
    
    plot = ScatterPlot( name, data, errorx, errory, width, height, background, border,
                        axis, dash, discrete, dots, grid, series_legend, x_labels, y_labels,
                        x_bounds, y_bounds, z_bounds, x_title, y_title, series_colors, circle_colors )
    plot.render()
    plot.commit()
    
    
def dot_line_plot(name,
                  data,
                  width,
                  height,
                  background = None,
                  border = 0,
                  axis = False,
                  dash = False,
                  dots = False,
                  grid = False,
                  series_legend = False,
                  x_labels = None,
                  y_labels = None,
                  x_bounds = None,
                  y_bounds = None,
                  x_title  = None,
                  y_title  = None,
                  series_colors = None):
    '''
        - Function to plot graphics using dots and lines.
        
        dot_line_plot (name, data, width, height, background = None, border = 0, axis = False, grid = False, x_labels = None, y_labels = None, x_bounds = None, y_bounds = None)

        - Parameters

        name - Name of the desired output file, no need to input the .svg as it will be added at runtim;
        data - The list, list of lists or dictionary holding the data to be plotted;
        width, height - Dimensions of the output image;
        background - A 3 element tuple representing the rgb color expected for the background or a new cairo linear gradient. 
                     If left None, a gray to white gradient will be generated;
        border - Distance in pixels of a square border into which the graphics will be drawn;
        axis - Whether or not the axis are to be drawn;
        dash - Boolean or a list or a dictionary of booleans indicating whether or not the associated series should be drawn in dashed mode;
        dots - Whether or not dots should be drawn on each point;
        grid - Whether or not the gris is to be drawn;
        series_legend - Whether or not the legend is to be drawn;
        x_labels, y_labels - lists of strings containing the horizontal and vertical labels for the axis;
        x_bounds, y_bounds - tuples containing the lower and upper value bounds for the data to be plotted;
        x_title - Whether or not to plot a title over the x axis.
        y_title - Whether or not to plot a title over the y axis.

        - Examples of use

        data = [0, 1, 3, 8, 9, 0, 10, 10, 2, 1]
        CairoPlot.dot_line_plot('teste', data, 400, 300)
        
        data = { "john" : [10, 10, 10, 10, 30], "mary" : [0, 0, 3, 5, 15], "philip" : [13, 32, 11, 25, 2] }
        x_labels = ["jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008" ]
        CairoPlot.dot_line_plot( 'test', data, 400, 300, axis = True, grid = True, 
                                  series_legend = True, x_labels = x_labels )
    '''
    plot = DotLinePlot( name, data, width, height, background, border,
                        axis, dash, dots, grid, series_legend, x_labels, y_labels,
                        x_bounds, y_bounds, x_title, y_title, series_colors )
    plot.render()
    plot.commit()
    
    
def gantt_chart(name, pieces, width, height, y_labels, colors):

    '''
        - Function to generate Gantt Charts.
        
        gantt_chart(name, pieces, width, height, x_labels, y_labels, colors):

        - Parameters
        
        name - Name of the desired output file, no need to input the .svg as it will be added at runtim;
        pieces - A list defining the spaces to be drawn. The user must pass, for each line, the index of its start and the index of its end. If a line must have two or more spaces, they must be passed inside a list;
        width, height - Dimensions of the output image;
        x_labels - A list of names for each of the vertical lines;
        y_labels - A list of names for each of the horizontal spaces;
        colors - List containing the colors expected for each of the horizontal spaces

        - Example of use

        pieces = [ (0.5,5.5) , [(0,4),(6,8)] , (5.5,7) , (7,8)]
        x_labels = [ 'teste01', 'teste02', 'teste03', 'teste04']
        y_labels = [ '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010' ]
        colors = [ (1.0, 0.0, 0.0), (1.0, 0.7, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0) ]
        CairoPlot.gantt_chart('gantt_teste', pieces, 600, 300, x_labels, y_labels, colors)
    '''

    plot = GanttChart(name, pieces, width, height, y_labels, colors)
    plot.render()
    plot.commit()
    
    
class CairoPlot(object):
    def __init__(self, serie=None):
        self.__serie = None
        self.__range = None
        if serie is not None:
            self.serie = serie
        
        # Create fsets for this properties
        self.x_labels = None
        self.y_labels = None
        self.x_title = None
        self.y_title = None
        self.colors = None
        self.background = None
        self.errorx = None
        self.errory = None
        
        # Flags
        self.axis = False
        self.grid = False
        self.dots = False
        self.series_legend=True
        self.dash = False
        
    @apply
    def serie():
        def fget(self):
            return self.__serie

        def fset(self, serie):
            if isinstance(serie, Serie):
                self.__serie = serie
            elif type(serie) is list and callable(serie[0]):
                if self.range is None:
                    raise Exception, "Must set a valid range before assingning a function"
                self.__serie = Serie()
                for item in serie:
                    g = Group()
                    g.x_range = self.range[:]
                    g.data_list = item
                    self.__serie.add_group(g)
                
            elif type(serie) is dict and callable(serie.values()[0]):
                if self.range is None:
                    raise Exception, "Must set a valid range before assingning a function"
                
                self.__serie = Serie()
                keys = serie.keys()
                keys.sort()
                for name in keys:
                    g = Group(name=name)
                    g.x_range = self.range[:]
                    g.data_list = serie[name]
                    self.__serie.add_group(g)
                
            else:
                self.__serie = Serie(serie)
                
        return property(**locals())
    
    @apply
    def range():
        def fget(self):
            return self.__range
        
        def fset(self, x_range):
            if type(x_range) is list and len(x_range) > 0:
                self.__range = x_range[:]
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
                
                self.__range = [start]
                while True:
                    start = start + step
                    if start > end:
                        break
                    self.__range.append(start)
            else:
                raise Exception, "x_range must be a list with one or more item or a tuple with 2 or 3 items"
            
        return property(**locals())
    
    def DefaultProperties(self):
        # Create fsets for this properties
        self.x_labels = None
        self.y_labels = None
        self.x_title = None
        self.y_title = None
        self.__range = None
        self.colors = None
        self.background = None
        self.errorx = None
        self.errory = None
        
        # Flags
        self.axis = False
        self.grid = False
        self.dots = False
        self.series_legend=True
        self.dash = False
        
    def PlotScatter(self,
                    name,
                    #data   = None,
                    #errorx = None,
                    #errory = None,
                    width  = 640,
                    height = 480,
                    #background = None,
                    border = 0,
                    #axis = False,
                    #dash = False,
                    discrete = False, 
                    #dots = False,
                    #grid = False,
                    #series_legend = False,
                    #x_labels = None,
                    #y_labels = None,
                    x_bounds = None,
                    y_bounds = None,
                    z_bounds = None,
                    #x_title  = None,
                    #y_title  = None,
                    series_colors = None,
                    circle_colors = None):
        
        plot = ScatterPlot(name, self.serie, self.errorx, self.errory, width, height,
                           self.background, border, self.axis, self.dash, discrete, self.dots,
                           self.grid, self.series_legend, self.x_labels, self.y_labels,
                           x_bounds, y_bounds, z_bounds, self.x_title, self.y_title,
                           series_colors, circle_colors)
        plot.render()
        plot.commit()
    
    def PlotDotLine(self,
                    name,
                    #data,
                    width,
                    height,
                    #background = None,
                    border = 0,
                    #axis = False,
                    #dash = False,
                    #dots = False,
                    #grid = False,
                    #series_legend = False,
                    #x_labels = None,
                    #y_labels = None,
                    x_bounds = None,
                    y_bounds = None,
                    #x_title  = None,
                    #y_title  = None,
                    series_colors = None):
        
        plot = DotLinePlot(name, self.serie, width, height, self.background, border,
                           self.axis, self.dash, self.dots, self.grid, self.series_legend,
                           self.x_labels, self.y_labels, x_bounds, y_bounds, self.x_title,
                           self.y_title, series_colors)
        plot.render()
        plot.commit()
    
    def PlotGanttChart(self, name, width, heigth):
        plot = GanttChart(name, self.serie, width, height, self.y_labels, self.colors)
        plot.render()
        plot.commit()
