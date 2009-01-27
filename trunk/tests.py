import CairoPlot
import cairo
import math

test_bar_plot = 0
test_scatter_plot = True
test_donut_plot = 0
test_dot_line_plot = 0
test_function_plot = 0
test_gantt_chart = 0
test_pie_plot = 0

if test_bar_plot:
    #Passing a dictionary
    data = { 'teste00' : [27], 'teste01' : [10], 'teste02' : [18], 'teste03' : [5], 'teste04' : [1], 'teste05' : [22] }
    CairoPlot.bar_plot ( 'bar_0_dictionary', data, 400, 300, border = 20, grid = True, rounded_corners = True )

    #Using default, rounded corners and 3D visualization
    data = [ [0, 3, 11], [8, 9, 21], [13, 10, 9], [2, 30, 8] ]
    colors = [ (1,0.2,0), (1,0.7,0), (1,1,0) ]
    CairoPlot.bar_plot ( 'bar_1_default', data, 400, 300, border = 20, grid = True, rounded_corners = False, colors = colors )
    CairoPlot.bar_plot ( 'bar_2_rounded', data, 400, 300, border = 20, grid = True, rounded_corners = True, colors = colors )
    CairoPlot.bar_plot ( 'bar_3_3D', data, 400, 300, border = 20, grid = True, three_dimension = True, colors = colors )

    #Mixing groups and columns
    data = [ [1], [2], [3,4], [4], [5], [6], [7], [8], [9], [10] ]
    CairoPlot.bar_plot ( 'bar_4_group', data, 400, 300, border = 20, grid = True )

    #Using no labels, horizontal and vertical labels
    data = [[3,4], [4,8], [5,3], [9,1]]
    v_labels = [ "line1", "line2", "line3", "line4", "line5", "line6" ]
    h_labels = [ "group1", "group2", "group3", "group4" ]
    CairoPlot.bar_plot ( 'bar_5_no_labels', data, 600, 200, border = 20, grid = True )
    CairoPlot.bar_plot ( 'bar_6_h_labels', data, 600, 200, border = 20, grid = True, h_labels = h_labels )
    CairoPlot.bar_plot ( 'bar_7_v_labels', data, 600, 200, border = 20, grid = True, v_labels = v_labels )
    CairoPlot.bar_plot ( 'bar_8_hv_labels', data, 600, 200, border = 20, grid = True, h_labels = h_labels, v_labels = v_labels )

if test_scatter_plot:
    #FIXME: Correct comments
    #Default data
    data = [ (-2,10), (0,0), (0,15), (1,5), (2,0), (3,-10), (3,5) ]
    CairoPlot.scatter_plot ( 'cross_1_default', data, 500, 500, border = 20, axis = True, grid = True )
    
    #Two Default data
    data = [ [ (0,0), (-2,10), (0,15), (1,5), (2,0), (3,-10), (3,5) ],
             [ (0,2), (-2,12), (0,17), (1,7), (2,2), (3,-8),  (3,7) ]  ]
    CairoPlot.scatter_plot ( 'cross_2_default', data, 500, 500, border = 20, axis = True, grid = True )
    
    #Dictionary of Default data
    data = { 'data1' : [ (0,0), (0,10), (0,15), (1,5), (2,0), (3,-10), (3,5) ],
             'data2' : [ (2,2), (2,12), (2,17), (3,7), (4,2), (5,-8),  (5,7) ]  }
    CairoPlot.scatter_plot ( 'cross_3_default', data, 500, 500, border = 20, axis = True, grid = True )
    
    #Two lists data
    data = [ [0, 0, 0, 1, 2, 3, 3], [0, 10, 15, 5, 0, -10, 5] ]
    CairoPlot.scatter_plot ( 'cross_4_two_lists', data, 500, 500, border = 20, axis = True, discrete = True, dots = True, grid = True )
    
    #Two groups of two lists data
    data = [ [ [0, 0, 0, 1, 2, 3, 3], [0, 10, 15, 5, 0, -10, 5] ],
             [ [2, 2, 2, 3, 4, 5, 5], [2, 12, 17, 7, 2, -8, 7] ]  ]
    CairoPlot.scatter_plot ( 'cross_5_two_lists', data, 500, 500, border = 20, axis = True, discrete = True, dots = True, grid = True )
    
    #Dictionary
    data = { 'data1' : [ [0, 0, 0, 1, 2, 3, 3], [0, 10, 15, 5, 0, -10, 5] ],
             'data2' : [ [2, 2, 2, 3, 4, 5, 5], [2, 12, 17, 7, 2, -8, 7] ]  }
    CairoPlot.scatter_plot ( 'cross_6_two_lists', data, 500, 500, border = 20, axis = True, discrete = True, dots = True, grid = True )
    
    data = [(-1, -16, 12), (-12, 17, 11), (-4, 6, 5), (4, -20, 12), (13, -3, 21), (7, 14, 20), (-11, -2, 18), (19, 7, 18), (-10, -19, 15),
            (-17, -2, 6), (-9, 4, 10), (14, 11, 16), (13, -11, 18), (20, 20, 16), (7, -8, 15), (-16, 17, 16), (16, 9, 9), (-3, -13, 25),
            (-20, -6, 17), (-10, -10, 12), (-7, 17, 25), (10, -10, 13), (10, 13, 20), (17, 6, 15), (18, -11, 14), (18, -12, 11), (-9, 11, 14),
            (17, -15, 25), (-2, -8, 5), (5, 20, 20), (18, 20, 23), (-20, -16, 17), (-19, -2, 9), (-11, 19, 18), (17, 16, 12), (-5, -20, 15),
            (-20, -13, 10), (-3, 5, 20), (-1, 13, 17), (-11, -9, 11)]
    colors = [ (0,0,0,0.25), (1,0,0,0.75) ]
    CairoPlot.scatter_plot ( 'cross_7_real_data', data, 500, 500, border = 20, axis = True, discrete = True, dots = True, grid = True, circle_colors = colors, radius = 2 )
    
if test_donut_plot :
    #Define a new backgrond
    background = cairo.LinearGradient(300, 0, 300, 400)
    background.add_color_stop_rgb(0,0.4,0.4,0.4)
    background.add_color_stop_rgb(1.0,0.1,0.1,0.1)
    
    data = {"john" : 700, "mary" : 100, "philip" : 100 , "suzy" : 50, "yman" : 50}
    #Default plot, gradient and shadow, different background
    CairoPlot.donut_plot( "donut_1_default", data, 600, 400, inner_radius = 0.3 )
    CairoPlot.donut_plot( "donut_2_gradient_shadow", data, 600, 400, gradient = True, shadow = True, inner_radius = 0.3 )
    CairoPlot.donut_plot( "donut_3_background", data, 600, 400, background = background, gradient = True, shadow = True, inner_radius = 0.3 )

if test_dot_line_plot:
    #Default plot
    data = [ 0, 1, 3.5, 8.5, 9, 0, 10, 10, 2, 1 ]
    CairoPlot.dot_line_plot( "dot_line_1_default", data, 400, 300, axis = True, grid = True )

    #Labels
    data = { "john" : [-5, -2, 0, 1, 3], "mary" : [0, 0, 3, 5, 2], "philip" : [-2, -3, -4, 2, 1] }
    h_labels = [ "jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008" ]
    v_labels = [ "very low", "low", "medium", "high", "very high" ]
    CairoPlot.dot_line_plot( "dot_line_2_dictionary_labels", data, 400, 300, h_labels = h_labels, 
                             v_labels = v_labels, axis = True, grid = True )
    
    #Series legend
    data = { "john" : [10, 10, 10, 10, 30], "mary" : [0, 0, 3, 5, 15], "philip" : [13, 32, 11, 25, 2] }
    h_labels = [ "jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008" ]
    CairoPlot.dot_line_plot( 'dot_line_3_series_legend', data, 400, 300, h_labels = h_labels, 
                             axis = True, grid = True, series_legend = True )

if test_function_plot :
    #Default Plot
    data = lambda x : x**2
    CairoPlot.function_plot( 'function_1_default', data, 400, 300, grid = True, h_bounds=(-10,10), step = 0.1 )
    
    #Discrete Plot
    data = lambda x : math.sin(0.1*x)*math.cos(x)
    CairoPlot.function_plot( 'function_2_discrete', data, 800, 300, grid = True, dots = True, h_bounds=(0,80), step = 0.9, discrete = True )

    #Labels test
    data = lambda x : [1,2,3,4][x]
    h_labels = [ "4", "3", "2", "1" ]
    CairoPlot.function_plot( 'function_3_labels', data, 400, 300, discrete = True, dots = True, grid = True, h_labels = h_labels, h_bounds=(0,4), step = 1 )
    
    #Multiple functions
    data = [ lambda x : 1, lambda y : y**2, lambda z : -z**2 ]
    colors = [ (1.0, 0.0, 0.0 ), ( 0.0, 1.0, 0.0 ), ( 0.0, 0.0, 1.0 ) ]
    CairoPlot.function_plot( 'function_4_multi_functions', data, 400, 300, grid = True, series_colors = colors, step = 0.1 )

if test_gantt_chart :
    #Default Plot
    pieces = [ (0.5,5.5) , [(0,4),(6,8)] , (5.5,7) , (7,9)]
    h_labels = [ 'teste01', 'teste02', 'teste03', 'teste04']
    v_labels = [ '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010' ]
    colors = [ (1.0, 0.0, 0.0), (1.0, 0.7, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0) ]
    CairoPlot.gantt_chart('gantt_1_default', pieces, 500, 350, h_labels, v_labels, colors)


if test_pie_plot :
    #Define a new backgrond
    background = cairo.LinearGradient(300, 0, 300, 400)
    background.add_color_stop_rgb(0.0,0.7,0.0,0.0)
    background.add_color_stop_rgb(1.0,0.3,0.0,0.0)

    #Plot data
    data = {"orcs" : 100, "goblins" : 230, "elves" : 50 , "demons" : 43, "humans" : 332}
    CairoPlot.pie_plot( "pie_1_default", data, 600, 400 )
    CairoPlot.pie_plot( "pie_2_gradient_shadow", data, 600, 400, gradient = True, shadow = True )
    CairoPlot.pie_plot( "pie_3_background", data, 600, 400, background = background, gradient = True, shadow = True )
