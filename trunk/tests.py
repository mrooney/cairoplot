import CairoPlot
import cairo
import math

data = lambda x : math.sin(0.1*x)*math.cos(x)
CairoPlot.function_plot('function1', data, 800, 300, grid = True, h_bounds=(0,80), step = 0.1)
data = lambda x : x**2
CairoPlot.function_plot('function2', data, 400, 300, grid = True, h_bounds=(-10,10), step = 0.1)

#data = {'teste00' : [27], 'teste01' : [10], 'teste02' : [18], 'teste03' : [5], 'teste04' : [1], 'teste05' : [22], 'teste06' : [31], 'teste07' : [8], 'teste08' : [13], 'teste09' : [10]}
#data = [[0, 3, 11], [8, 9, 21], [13, 10, 9], [2, 30, 8]]
#colors = [(1,0.2,0), (1,0.7,0), (1,1,0)]
#data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#CairoPlot.bar_plot ('bar1', data, 400, 300, border = 20, grid = True, rounded_corners = False, colors = colors)
#CairoPlot.bar_plot ('bar2', data, 400, 300, border = 20, grid = True, rounded_corners = True, colors = colors)
#CairoPlot.bar_plot ('bar3D', data, 400, 300, border = 20, grid = True, three_dimension = True, colors = colors)

#data = [[1], [2], [3,4], [4], [5], [6], [7], [8], [9], [10]]
#CairoPlot.bar_plot ('bar2', data, 400, 300, border = 20, grid = True)
#data = [[3,4], [4,8], [5,3], [9,1]]
#v_labels = ["line1", "line2", "line3", "line4", "line5", "line6"]
#h_labels = ["group1", "group2", "group3", "group4"]
#CairoPlot.bar_plot ('bar', data, 600, 200, border = 20, grid = True)
#CairoPlot.bar_plot ('bar2', data, 600, 200, border = 20, grid = True, h_labels = h_labels)
#CairoPlot.bar_plot ('bar3', data, 600, 200, border = 20, grid = True, v_labels = v_labels)
#CairoPlot.bar_plot ('bar4', data, 600, 200, border = 20, grid = True, h_labels = h_labels, v_labels = v_labels)
#CairoPlot.bar_plot ('bar4', data, 600, 200, border = 20, grid = True, h_labels = h_labels, v_labels = v_labels, h_bounds = (0,20))
#teste_data = [0, 1, 3.5, 8.5, 9, 0, 10, 10, 2, 1]
#CairoPlot.dot_line_plot('teste', teste_data, 400, 300, axis = True, grid = True)
         
#teste_data_2 = {"john" : [-5, -2, 0, 1, 3], "mary" : [0, 0, 3, 5, 2], "philip" : [-2, -3, -4, 2, 1]}
#teste_h_legend = ["jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008"]
#teste_v_legend = ["jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008"]
#CairoPlot.dot_line_plot('teste2', teste_data_2, 400, 300, h_legend = teste_h_legend, v_legend = teste_v_legend, axis = True, grid = True)
#teste_data_2 = {"john" : [10, 10, 10, 10, 30], "mary" : [0, 0, 3, 5, 15], "philip" : [13, 32, 11, 25, 2]}
#teste_h_legend = ["jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008"]
#CairoPlot.dot_line_plot('teste3', teste_data_2, 400, 300, h_legend = teste_h_legend, axis = True, grid = True)

#background = cairo.LinearGradient(300, 0, 300, 400)
#background.add_color_stop_rgb(0,0.4,0.4,0.4)
#background.add_color_stop_rgb(1.0,0.1,0.1,0.1)

#teste_data = {"john" : 700, "mary" : 100, "philip" : 100 , "suzy" : 50, "yman" : 50}
#CairoPlot.pie_plot("pie_teste", teste_data, 600, 400, background = background )
#CairoPlot.donut_plot("donut_teste1", teste_data, 600, 400, background = background, gradient = True, shadow = True, inner_radius = 0.3)
#CairoPlot.donut_plot("donut_teste2", teste_data, 600, 400, gradient = True, shadow = True, inner_radius = 0.3)
#CairoPlot.donut_plot("donut_teste3", teste_data, 600, 400, gradient = False, shadow = False, inner_radius = 0.3)

#pieces = [ (0.5,5.5) , [(0,4),(6,8)] , (5.5,7) , (7,8)]
#h_legend = [ 'teste01', 'teste02', 'teste03', 'teste04']
#v_legend = [ '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010' ]
#colors = [ (1.0, 0.0, 0.0), (1.0, 0.7, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0) ]
#CairoPlot.gantt_chart('gantt1', pieces, 500, 350, h_legend, v_legend, colors)
#pieces = [ (0.5,5.5) , [(0,4),(6,8)] , (5.5,7) , (7,9)]
#h_legend = [ 'teste01', 'teste02', 'teste03', 'teste04']
#v_legend = [ '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010' ]
#colors = [ (1.0, 0.0, 0.0), (1.0, 0.7, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0) ]
#CairoPlot.gantt_chart('gantt2', pieces, 500, 350, h_legend, v_legend, colors)
