#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CairoPlot.py
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

#Contributor: João S. O. Bueno

__version__ = 1.1

import cairo
import math
import random

HORZ = 0
VERT = 1

def other_direction(direction):
    "explicit is better than implicit"
    if direction == HORZ:
        return VERT
    else:
        return HORZ

class Plot(object):
    def __init__(self, 
                 surface=None,
                 data=None,
                 width=640,
                 height=480,
                 background=None,
                 border = 0,
                 h_labels = None,
                 v_labels = None):
        self.create_surface(surface, width, height)
        self.width = width
        self.height = height
        self.context = cairo.Context(self.surface)
        self.load_series(data, h_labels, v_labels)

        self.labels={}
        self.labels[HORZ] = h_labels
        self.labels[VERT] = v_labels

        self.font_size = 10
        
        self.set_background (background)
        self.border = 0
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
        if not type(surface) in (str, unicode): 
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
    
    #def __del__(self):
    #    self.commit()

    def commit(self):
        try:
            self.context.show_page()
            if self.filename.endswith(".png"):
                self.surface.write_to_png(self.filename)
            else:
                self.surface.finish()
        except cairo.Error:
            pass
        
    def load_series (self, data, h_labels=None, v_labels=None):
        #FIXME: implement Series class for holding series data,
        # labels and presentation properties
        
        #data can be a list, a list of lists or a dictionary with 
        #each item as a labeled data series.
        #we should (for teh time being) create a list of lists
        #and set labels for teh series rom  teh values provided.
        
        self.series_labels = []
        self.data = []
        #if we have labeled series:
        if hasattr(data, "keys"):
            #dictionary:
            self.series_labels = data.keys()
            for key in self.series_labels:
                self.data.append(data[key])
        #if we have a series of series:
        elif hasattr(data[0], "__getitem__"):
            self.data = data
            self.series_labels = range(len(data))
        else:
            self.data = [data]
            self.series_labels = None
        #FIXME: select some pre-sets and allow these to be parametrized:
        random.seed(1)
        self.series_colors = [[random.random() for i in range(3)]  for series in self.data]
        self.series_widths = [1.0 for series in self.data]

    def get_width(self):
        return self.surface.get_width()
    def get_height(self):
        return self.surface.get_height()

    def set_background(self, background):
        if background is None:
            self.background = cairo.LinearGradient(self.width / 2, 0, self.width / 2, self.height)
            self.background.add_color_stop_rgb(0,1.0,1.0,1.0)
            self.background.add_color_stop_rgb(1.0,0.9,0.9,0.9)
        else:
            if type(background) in (cairo.LinearGradient, tuple):
                self.background = background
            else:
                raise TypeError ("Background should be either cairo.LinearGradient or a 3-tuple, not %s" % type(background))
        
    def render_background(self):
        if isinstance (self.background, cairo.LinearGradient):
            self.context.set_source(self.background)
        else:
            self.context.set_source_rgb(*self.background)
        self.context.rectangle(0,0, self.width, self.height)
        self.context.fill()
        
    def render_bounding_box(self):
        self.context.set_source_rgb(*self.line_color)
        self.context.set_line_width(self.line_width)
        self.context.rectangle(self.border, self.border,
                               self.width - 2 * self.border,
                               self.height - 2 * self.border)

    def render(self):
        pass

class DotLinePlot(Plot):
    def __init__(self, 
                 surface=None,
                 data=None,
                 width=640,
                 height=480,
                 background=None,
                 border=0, 
                 axis = False,
                 grid = False,
                 h_labels = None,
                 v_labels = None,
                 h_bounds = None,
                 v_bounds = None):
        
        self.bounds = {}
        self.bounds[HORZ] = h_bounds
        self.bounds[VERT] = v_bounds
        
        Plot.__init__(self, surface, data, width, height, background, border, h_labels, v_labels)
        self.axis = axis
        self.grid = grid

        self.max_value = {}
        
        self.h_label_angle = math.pi / 2.5

    def load_series(self, data, h_labels = None, v_labels = None):
        Plot.load_series(self, data, h_labels, v_labels)
        self.calc_boundaries()
    
    def calc_boundaries(self):
        
        if not self.bounds[HORZ]:
            self.bounds[HORZ] = (0, max([len(series) for series in (self.data)]))
            
        if not self.bounds[VERT]:
            max_data_value = min_data_value = 0
            for series in self.data:
                if max(series) > max_data_value:
                    max_data_value = max(series)
                if min(series) < min_data_value:
                    min_data_value = min(series)
            self.bounds[VERT] = (min_data_value, max_data_value)


    def calc_extents(self, direction):

        self.max_value[direction] = 0
        if self.labels[direction]:
            widest_word = max(self.labels[direction], lambda item: self.context.text_extents(item)[2])
            self.max_value[direction] = self.context.text_extents(widest_word)[2]
            self.borders[other_direction(direction)] = self.max_value[direction] + self.border
        else:
            self.max_value[direction] = self.context.text_extents(str(self.bounds[direction][1]))[2]
            self.borders[other_direction(direction)] = self.max_value[direction] + self.border + 20
            
    def calc_horz_extents(self):
        self.calc_extents(HORZ)
        
    def calc_vert_extents(self):
        self.calc_extents(VERT)
        
    
    def render_axis(self):
        cr = self.context
        h_border = self.borders[HORZ]
        v_border = self.borders[VERT]
        cr.set_source_rgb(*self.line_color)

        cr.move_to(h_border, self.height - v_border)
        cr.line_to(h_border, v_border)
        cr.stroke()

        cr.move_to(h_border, self.height - v_border)
        cr.line_to(self.width - h_border, self.height - v_border)
        cr.stroke()
    
    def render_labels(self):

        self.context.set_font_size(self.font_size * 0.8)
        
        self.render_horz_labels()
        self.render_vert_labels()
    
    def render_horz_labels(self):
        cr = self.context
        labels = self.labels[HORZ]
        if not labels:
            labels = [str(i) for i in range(self.bounds[HORZ][0], self.bounds[HORZ][1])]
        border = self.borders[HORZ]
        
        step = (self.width - 2 * border) / len(labels)
        x = border
        for item in labels:
            cr.set_source_rgb(*self.label_color)
            width = cr.text_extents(item)[2]
            cr.move_to(x, self.height - self.borders[VERT] + 10)
            cr.rotate(self.h_label_angle)
            cr.show_text(item)
            cr.rotate(-self.h_label_angle)
            #FIXME: render grid in a separate method
            if self.grid and x != border:
                cr.set_source_rgb(*self.grid_color)
                cr.move_to(x, self.height - self.borders[VERT])
                cr.line_to(x, self.borders[VERT])
                cr.stroke()
            x += step
    
    def render_vert_labels(self):
        cr = self.context
        labels = self.labels[VERT]
        if not labels:
            amplitude = self.bounds[VERT][1] - self.bounds[VERT][0]
            #if vertical labels need decimal points
            if amplitude % 10:
                label_type = lambda x : int(x)
            else:
                label_type = lambda x: float(x)
            labels = [str(
                        label_type(
                            self.bounds[VERT][0] +
                            (amplitude * i / 10.0)
                                  )                
                         ) for i in range(10) ]
        border = self.borders[VERT]
        
        step = (self.height - 2 * border)/ len(labels)
        y = self.height - border
        for item in labels:
            cr.set_source_rgb(*self.label_color)
            width = cr.text_extents(item)[2]
            cr.move_to(self.borders[HORZ] - width - 5,y)
            cr.show_text(item)
            #FIXME: render grid in a separate method
            if self.grid and y != self.height - border:
                cr.set_source_rgb(*self.grid_color)
                cr.move_to(self.borders[HORZ], y)
                cr.line_to(self.width - self.borders[HORZ], y)
                cr.stroke()
            y -=step
    
    
    def render(self):
        self.calc_horz_extents()
        self.calc_vert_extents()
            
        self.render_background()
        self.render_bounding_box()
        
        if self.axis:
            self.render_axis()

        self.render_labels()
        
        self.render_plot()
        
    def render_series_labels(self):
        #FIXME: implement this
        for key in self.series_labels:
            pass
            #This was not working in Rodrigo's original code anyway 

    def render_plot(self):
        #render_series_labels
        largest_series_length = len(max(self.data, key=len))
        #FIXME: plot_width and plot_height should be object properties and be re-used.
        plot_width = self.width - 2* self.borders[HORZ]
        plot_height = self.height - 2 * self.borders[VERT]
        plot_top = self.height - self.borders[VERT]
        
        series_amplitude = self.bounds[VERT][1] - self.bounds[VERT][0]
        
        horizontal_step = float (plot_width) / largest_series_length
        vertical_step = float (plot_height) / series_amplitude
        last = None
        cr = self.context
        for number, series in  enumerate (self.data):
            cr.set_source_rgb(*self.series_colors[number])
            x = self.borders[HORZ]
            last = None
            #FIXME: separate plotting of lines, dots and area

            for value in series:
                if last != None:
                    cr.move_to(x - horizontal_step, plot_top - int(last * vertical_step))
                    cr.line_to(x, plot_top - int(value * vertical_step))
                    cr.set_line_width(self.series_widths[number])
                    cr.stroke()
                cr.new_path()
                cr.arc(x, plot_top - int(value * vertical_step), 3, 0, 2.1 * math.pi)
                cr.close_path()
                cr.fill()
                x += horizontal_step
                last = value


        

def dot_line_plot(name,
                  data,
                  width,
                  height,
                  background = None,
                  border = 0,
                  axis = False,
                  grid = False,
                  h_legend = None,
                  v_legend = None,
                  h_bounds = None,
                  v_bounds = None):
    '''
        Function to plot graphics using dots and lines.
        dot_line_plot (name, data, width, height, background = None, border = 0, axis = False, grid = False, h_legend = None, v_legend = None, h_bounds = None, v_bounds = None)

        Parameters

        name - Name of the desired output file, no need to input the .svg as it will be added at runtim;
        data - The list, list of lists or dictionary holding the data to be plotted;
        width, height - Dimensions of the output image;
        background - A 3 element tuple representing the rgb color expected for the background. If left None, a gray to white gradient will be generated;
        border - Distance in pixels of a square border into which the graphics will be drawn;
        axis - Whether or not the axis are to be drawn;
        grid - Whether or not the gris is to be drawn;
        h_legend, v_legend - lists of strings containing the horizontal and vertical legends for the axis;
        h_bounds, v_bounds - tuples containing the lower and upper value bounds for the data to be plotted.

        Examples of use

        teste_data = [0, 1, 3, 8, 9, 0, 10, 10, 2, 1]
        CairoPlot.dot_line_plot('teste', teste_data, 400, 300)
        
        teste_data_2 = {"john" : [10, 10, 10, 10, 30], "mary" : [0, 0, 3, 5, 15], "philip" : [13, 32, 11, 25, 2]}
        teste_h_legend = ["jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008"]
        CairoPlot.dot_line_plot('teste2', teste_data_2, 400, 300, axis = True, grid = True, h_legend = teste_h_legend)
    '''
    plot = DotLinePlot(name, data, width, height, background, border,
                       axis, grid, h_legend, v_legend, h_bounds, v_bounds)
    plot.render()
    plot.commit()



def pizza_plot(name, data, width, height, background = None):

    '''
        Function to plot pizza graphics.
        pizza_plot(name, data, width, height, background = None)

        Parameters
        
        name - Name of the desired output file, no need to input the .svg as it will be added at runtim;
        data - The list, list of lists or dictionary holding the data to be plotted;
        width, height - Dimensions of the output image;
        background - A 3 element tuple representing the rgb color expected for the background. If left None, a gray to white gradient will be generated;

        Examples of use
        
        teste_data = {"john" : 123, "mary" : 489, "philip" : 890 , "suzy" : 235}
        CairoPlot.pizza_plot("pizza_teste", teste_data, 500, 500)
        
    '''

    surface = cairo.SVGSurface(name + '.svg', width, height)
    print width, height
    cr = cairo.Context(surface)

    if background != None:
        cr.set_source_rgb(background[0], background[1], background[2])
        cr.rectangle(0,0,width,height)
        cr.fill()
    else:
        linear = cairo.LinearGradient(width/2, 0, width/2, height)
        linear.add_color_stop_rgb(0,1.0,1.0,1.0)
        linear.add_color_stop_rgb(1.0,0.9,0.9,0.9)
        cr.set_source(linear)
        cr.rectangle(0,0, width, height)
        cr.fill()
 
    angle = 0
    next_angle = 0
    cr.set_line_width(2.0)
    x0 = width/2
    y0 = height/2
    n = 0
    for key in data.keys():
        n += data[key]

    for key in data.keys():
        next_angle = angle + 2.0*math.pi*data[key]/n
    
        radius = width/3 if width < height else height/3
        print radius
        cr.set_source_rgb(random.random(), random.random(), random.random())
    
        w = cr.text_extents(key)[2]
        if (angle + next_angle)/2 < math.pi/2 or (angle + next_angle)/2 > 3*math.pi/2:
            cr.move_to(x0 + (radius+10)*math.cos((angle+next_angle)/2), y0 + (radius+10)*math.sin((angle+next_angle)/2) )
        else:
            cr.move_to(x0 + (radius+10)*math.cos((angle+next_angle)/2) - w, y0 + (radius+10)*math.sin((angle+next_angle)/2) )
        cr.show_text(key)

        cr.move_to(x0,y0)
        cr.line_to(x0+radius*math.cos(angle), y0+radius*math.sin(angle))
        cr.arc(x0, y0, radius, angle, angle + 2.0*math.pi*data[key]/n)
        cr.line_to(x0,y0)
        cr.close_path()
        cr.fill()
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.move_to(x0,y0)
        cr.line_to(x0+radius*math.cos(angle), y0+radius*math.sin(angle))
        cr.arc(x0, y0, radius, angle, angle + 2.0*math.pi*data[key]/n)
        cr.line_to(x0,y0)
        cr.close_path()
        cr.stroke()
        angle = next_angle


def drawRectangle(cr, x0, y0, x1, y1, color):
    mid = (x0+x1)/2
    linear = cairo.LinearGradient(mid,y0,mid,y1)
    linear.add_color_stop_rgb(0,3.5*color[0]/5.0, 3.5*color[1]/5.0, 3.5*color[2]/5.0)
    linear.add_color_stop_rgb(1,color[0],color[1],color[2])
    cr.set_source(linear)

    cr.arc(x0+5, y0+5, 5, 0, 2*math.pi)
    cr.arc(x1-5, y0+5, 5, 0, 2*math.pi)
    cr.arc(x0+5, y1-5, 5, 0, 2*math.pi)
    cr.arc(x1-5, y1-5, 5, 0, 2*math.pi)
    cr.rectangle(x0+5,y0,x1-x0-10,y1-y0)
    cr.rectangle(x0,y0+5,x1-x0,y1-y0-10)
    cr.fill()

def drawShadow(cr, x0, y0, x1, y1):
    shadow = 0.4
    h_mid = (x0+x1)/2
    v_mid = (y0+y1)/2
    h_linear_1 = cairo.LinearGradient(h_mid,y0-4,h_mid,y0+4)
    h_linear_2 = cairo.LinearGradient(h_mid,y1-4,h_mid,y1+4)
    v_linear_1 = cairo.LinearGradient(x0-4,v_mid,x0+4,v_mid)
    v_linear_2 = cairo.LinearGradient(x1-4,v_mid,x1+4,v_mid)
    radial_00 = cairo.RadialGradient(x0+4, y0+4, 0, x0+4, y0+4, 8)
    radial_01 = cairo.RadialGradient(x1-4, y0+4, 0, x1-4, y0+4, 8)
    radial_10 = cairo.RadialGradient(x0+4, y1-4, 0, x0+4, y1-4, 8)
    radial_11 = cairo.RadialGradient(x1-4, y1-4, 0, x1-4, y1-4, 8)


    h_linear_1.add_color_stop_rgba( 0, 0, 0, 0, 0)
    h_linear_1.add_color_stop_rgba( 1, 0, 0, 0, shadow)
    h_linear_2.add_color_stop_rgba( 0, 0, 0, 0, shadow)
    h_linear_2.add_color_stop_rgba( 1, 0, 0, 0, 0)
    v_linear_1.add_color_stop_rgba( 0, 0, 0, 0, 0)
    v_linear_1.add_color_stop_rgba( 1, 0, 0, 0, shadow)
    v_linear_2.add_color_stop_rgba( 0, 0, 0, 0, shadow)
    v_linear_2.add_color_stop_rgba( 1, 0, 0, 0, 0)
    cr.set_source(h_linear_1)
    #cr.set_source_rgb(0,0,1)
    cr.rectangle(x0+4,y0-4,x1-x0-8,8)
    cr.fill()
    cr.set_source(h_linear_2)
    #cr.set_source_rgb(0,0,1)
    cr.rectangle(x0+4,y1-4,x1-x0-8,8)
    cr.fill()
    cr.set_source(v_linear_1)
    #cr.set_source_rgb(0,0,1)
    cr.rectangle(x0-4,y0+4,8,y1-y0-8)
    cr.fill()
    cr.set_source(v_linear_2)
    #cr.set_source_rgb(0,0,1)
    cr.rectangle(x1-4,y0+4,8,y1-y0-8)
    cr.fill()

    radial_00.add_color_stop_rgba(0, 0, 0, 0, shadow)
    radial_00.add_color_stop_rgba(1, 0, 0, 0, 0)
    radial_01.add_color_stop_rgba(0, 0, 0, 0, shadow)
    radial_01.add_color_stop_rgba(1, 0, 0, 0, 0)
    radial_10.add_color_stop_rgba(0, 0, 0, 0, shadow)
    radial_10.add_color_stop_rgba(1, 0, 0, 0, 0)
    radial_11.add_color_stop_rgba(0, 0, 0, 0, shadow)
    radial_11.add_color_stop_rgba(1, 0, 0, 0, 0)
    #cr.set_source_rgb(0,0,1)
    cr.set_source(radial_00)
    cr.move_to(x0+4,y0+4)
    cr.line_to(x0,y0+4)
    cr.arc(x0+4, y0+4, 8, math.pi, 3*math.pi/2)
    cr.line_to(x0+4,y0+4)
    cr.close_path()
    cr.fill()
    #cr.set_source_rgb(0,0,1)
    cr.set_source(radial_01)
    cr.move_to(x1-4,y0+4)
    cr.line_to(x1-4,y0)
    cr.arc(x1-4, y0+4, 8, 3*math.pi/2, 2*math.pi)
    cr.line_to(x1-4,y0+4)
    cr.close_path()
    cr.fill()
    #cr.set_source_rgb(0,0,0)
    cr.set_source(radial_10)
    cr.move_to(x0+4,y1-4)
    cr.line_to(x0+4,y1)
    cr.arc(x0+4, y1-4, 8, math.pi/2, math.pi)
    cr.line_to(x0+4,y1-4)
    cr.close_path()
    cr.fill()
    #cr.set_source_rgb(0,0,0)
    cr.set_source(radial_11)
    cr.move_to(x1-4,y1-4)
    cr.line_to(x1,y1-4)
    cr.arc(x1-4, y1-4, 8, 0, math.pi/2)
    cr.line_to(x1-4,y1-4)
    cr.close_path()
    cr.fill()

def gantt_chart(name, pieces, width, height, h_legend, v_legend, colors):

    '''
        Function to generate Gantt Diagrams.
        gantt_chart(name, pieces, width, height, h_legend, v_legend, colors):

        Parameters
        
        name - Name of the desired output file, no need to input the .svg as it will be added at runtim;
        pieces - A list defining the spaces to be drawn. The user must pass, for each line, the index of its start and the index of its end. If a line must have two or more spaces, they must be passed inside a list;
        width, height - Dimensions of the output image;
        h_legend - A list of names for each of the vertical lines;
        v_legend - A list of names for each of the horizontal spaces;
        colors - List containing the colors expected for each of the horizontal spaces

        Example of use

        pieces = [ (0.5,5.5) , [(0,4),(6,8)] , (5.5,7) , (7,8)]
        h_legend = [ 'teste01', 'teste02', 'teste03', 'teste04']
        v_legend = [ '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010' ]
        colors = [ (1.0, 0.0, 0.0), (1.0, 0.7, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0) ]
        CairoPlot.gantt_chart('gantt_teste', pieces, 600, 300, h_legend, v_legend, colors)
        
    '''

    surface = cairo.SVGSurface(name + '.svg', width, height)
    cr = cairo.Context(surface)
    cr.set_source_rgb(1.0, 1.0, 1.0)
    cr.rectangle(0,0,width,height)
    cr.fill()
    cr.set_font_size(0.02*width)
    max_word = ''
    for word in h_legend:
        max_word = word if word != None and len(word) > len(max_word) else max_word
    h_border = 100 + cr.text_extents(max_word)[2]
    horizontal_step = (width-h_border)/len(v_legend)
    vertical_step = height/(len(h_legend) + 1)
    v_border = vertical_step

    for line in pieces:
        linear = cairo.LinearGradient(width/2, v_border + pieces.index(line)*vertical_step, width/2, v_border + (pieces.index(line) + 1)*vertical_step)
        linear.add_color_stop_rgb(0,1.0,1.0,1.0)
        linear.add_color_stop_rgb(1.0,0.9,0.9,0.9)
        cr.set_source(linear)
        cr.rectangle(0,v_border + pieces.index(line)*vertical_step,width,vertical_step)
        cr.fill()

    cr.set_font_size(0.015*width)
    cr.set_source_rgb(0.7, 0.7, 0.7)
    cr.set_dash((1,0,0,0,0,0,1))
    cr.set_line_width(0.5)
    for word in v_legend:
        w,h = cr.text_extents(word)[2], cr.text_extents(word)[3]
        cr.move_to(h_border + v_legend.index(word)*horizontal_step-w/2, vertical_step/2)
        cr.show_text(word)
        cr.move_to(h_border + v_legend.index(word)*horizontal_step, vertical_step/2 + h)
        cr.line_to(h_border + v_legend.index(word)*horizontal_step, height)
    cr.stroke()

    cr.set_font_size(0.02*width)
    for line in pieces:
        word = h_legend[pieces.index(line)]
        if word != None:
            cr.set_source_rgb(0.5, 0.5, 0.5)
            w,h = cr.text_extents(word)[2], cr.text_extents(word)[3]
            cr.move_to(40,v_border + pieces.index(line)*vertical_step + vertical_step/2 + h/2)
            cr.show_text(word)

        if type(line) == type([]):
            for space in line:
                drawShadow(cr, h_border + space[0]*horizontal_step, v_border + pieces.index(line)*vertical_step + vertical_step/4.0, 
                               h_border + space[1]*horizontal_step, v_border + pieces.index(line)*vertical_step + 3.0*vertical_step/4.0)
                drawRectangle(cr, h_border + space[0]*horizontal_step, v_border + pieces.index(line)*vertical_step + vertical_step/4.0, 
                                  h_border + space[1]*horizontal_step, v_border + pieces.index(line)*vertical_step + 3.0*vertical_step/4.0, colors[pieces.index(line)])
        else:
            space = line
            drawShadow(cr, h_border + space[0]*horizontal_step, v_border + pieces.index(line)*vertical_step + vertical_step/4.0, 
                           h_border + space[1]*horizontal_step, v_border + pieces.index(line)*vertical_step + 3.0*vertical_step/4.0)
            drawRectangle(cr, h_border + space[0]*horizontal_step, v_border + pieces.index(line)*vertical_step + vertical_step/4.0, 
                              h_border + space[1]*horizontal_step, v_border + pieces.index(line)*vertical_step + 3.0*vertical_step/4.0, colors[pieces.index(line)])

