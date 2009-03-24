# Teste utilizando cairoplot
import cairoplot
from CairoPlot import scatter_plot, dot_line_plot, gantt_chart
from Series import Serie, Group, Data


test_scatter_plot = 0
test_dot_line_plot = 0
test_gantt_chart = 1

if test_scatter_plot:
    ######### Teste 1 ###########
    data = [ (-2,10), (0,0), (0,15), (1,5), (2,0), (3,-10), (3,5) ]
    cairoplot.scatter_plot ( 'scatter_1_default_cairoplot.png', data = data, width = 500, height = 500, border = 20, axis = True, grid = True )
    # Passagem de uma Serie para o scatter_plot
    # lista de pontos
    scatter_plot ( 'scatter_1_default_series.png', data = Serie([[ (-2,10), (0,0), (0,15), (1,5), (2,0), (3,-10), (3,5) ]]), width = 500, height = 500, border = 20, axis = True, grid = True )
    
    ######### Teste 2 ###########
    #lists of coordinates x,y
    data = [[1,2,3,4,5],[1,1,1,1,1]]
    cairoplot.scatter_plot ( 'scatter_2_lists_cairoplot.png', data = data, width = 500, height = 500, border = 20, axis = True, grid = True )
    # Atribuicao de uma serie atravez de uma atributo
    #lists of coordinates x,y
    data = Serie()
    data.group_list = [[[1,2,3,4,5],[1,1,1,1,1]]]
    # O mesmo pode ser feito passando diretamente um grupo:
    data.group_list = Group([[1,2,3,4,5],[1,1,1,1,1]])
    # Dentro da instancia de Serie o grupo sera convertido para uma serie. O mesmo se aplica para um dado (Data)
    scatter_plot ( 'scatter_2_lists_series.png', data = data, width = 500, height = 500, border = 20, axis = True, grid = True )
    
    ######### Teste 3 ###########
    #lists of coordinates x,y,z
    data = [[0.5,1,2,3,4,5],[0.5,1,1,1,1,1],[10,6,10,20,10,6]]
    colors = [ (0,0,0,0.25), (1,0,0,0.75) ]
    cairoplot.scatter_plot ( 'scatter_3_lists_cairoplot.png', data = data, width = 500, height = 500, border = 20, axis = True, discrete = True,
                             grid = True, circle_colors = colors )
    # Podemos passar um grupo diretamente para o scatter_plot
    #lists of coordinates x,y,z
    colors = [ (0,0,0,0.25), (1,0,0,0.75) ] 
    scatter_plot ( 'scatter_3_lists_series.png', data = Group([[0.5,1,2,3,4,5],[0.5,1,1,1,1,1],[10,6,10,20,10,6]]), width = 500, height = 500,
                  border = 20, axis = True, discrete = True, grid = True, circle_colors = colors )
    
    
    ######### Teste 4 ###########
    cairoplot.scatter_plot ( 'scatter_4_lists_cairoplot.png', data = [[(1,1,20), (2,1,10)]], width = 500, height = 500,
                  border = 20, axis = True, discrete = True, grid = True, circle_colors = colors )    
    # ou um dado/lista de dados. O scatter_plot se encarrega da conversao para uma serie
    scatter_plot ( 'scatter_4_lists_series.png', data = [Data((1,1,20)), Data((2,1,10))], width = 500, height = 500,
                  border = 20, axis = True, discrete = True, grid = True, circle_colors = colors )
    
    
    ######### Teste 5 ###########
    data = [(-1, -16, 12), (-12, 17, 11), (-4, 6, 5), (4, -20, 12), (13, -3, 21), (7, 14, 20), (-11, -2, 18), (19, 7, 18), (-10, -19, 15),
            (-17, -2, 6), (-9, 4, 10), (14, 11, 16), (13, -11, 18), (20, 20, 16), (7, -8, 15), (-16, 17, 16), (16, 9, 9), (-3, -13, 25),
            (-20, -6, 17), (-10, -10, 12), (-7, 17, 25), (10, -10, 13), (10, 13, 20), (17, 6, 15), (18, -11, 14), (18, -12, 11), (-9, 11, 14),
            (17, -15, 25), (-2, -8, 5), (5, 20, 20), (18, 20, 23), (-20, -16, 17), (-19, -2, 9), (-11, 19, 18), (17, 16, 12), (-5, -20, 15),
            (-20, -13, 10), (-3, 5, 20), (-1, 13, 17), (-11, -9, 11)]
    colors = [ (0,0,0,0.25), (1,0,0,0.75) ]
    cairoplot.scatter_plot ( 'scatter_2_variable_radius_cairoplot.png', data = data, width = 500, height = 500, border = 20, 
                             axis = True, discrete = True, dots = 2, grid = True, 
                             x_title = "x axis", y_title = "y axis", circle_colors = colors )
    
    # tambem temos retrocompatibilidade
    data = [[(-1, -16, 12), (-12, 17, 11), (-4, 6, 5), (4, -20, 12), (13, -3, 21), (7, 14, 20), (-11, -2, 18), (19, 7, 18), (-10, -19, 15),
            (-17, -2, 6), (-9, 4, 10), (14, 11, 16), (13, -11, 18), (20, 20, 16), (7, -8, 15), (-16, 17, 16), (16, 9, 9), (-3, -13, 25),
            (-20, -6, 17), (-10, -10, 12), (-7, 17, 25), (10, -10, 13), (10, 13, 20), (17, 6, 15), (18, -11, 14), (18, -12, 11), (-9, 11, 14),
            (17, -15, 25), (-2, -8, 5), (5, 20, 20), (18, 20, 23), (-20, -16, 17), (-19, -2, 9), (-11, 19, 18), (17, 16, 12), (-5, -20, 15),
            (-20, -13, 10), (-3, 5, 20), (-1, 13, 17), (-11, -9, 11)]]
    colors = [ (0,0,0,0.25), (1,0,0,0.75) ]
    scatter_plot ( 'scatter_2_variable_radius_series.png', data = data, width = 500, height = 500, border = 20, 
                   axis = True, discrete = True, dots = 2, grid = True, 
                   x_title = "x axis", y_title = "y axis", circle_colors = colors )
    
    
if test_dot_line_plot:
    ######### Teste 1 ###########
    #Default plot
    data = [ 0, 1, 3.5, 8.5, 9, 0, 10, 10, 2, 1 ]
    cairoplot.dot_line_plot( "dot_line_1_default_cairoplot", data, 400, 300, border = 50, axis = True, grid = True,
                             x_title = "x axis", y_title = "y axis" )
    data = Serie([ 0, 1, 3.5, 8.5, 9, 0, 10, 10, 2, 1 ])
    dot_line_plot( "dot_line_1_default_series", data, 400, 300, border = 50, axis = True, grid = True,
                             x_title = "x axis", y_title = "y axis" )


    ######### Teste 2 ###########
    #Labels
    data = { "john" : [-5, -2, 0, 1, 3], "mary" : [0, 0, 3, 5, 2], "philip" : [-2, -3, -4, 2, 1] }
    x_labels = [ "jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008" ]
    y_labels = [ "very low", "low", "medium", "high", "very high" ]
    cairoplot.dot_line_plot( "dot_line_2_dictionary_labels_cairoplot", data, 400, 300, x_labels = x_labels, 
                             y_labels = y_labels, axis = True, grid = True,
                             x_title = "x axis", y_title = "y axis", series_legend=True )
    
    data = Serie({ "john" : [-5, -2, 0, 1, 3], "mary" : [0, 0, 3, 5, 2], "philip" : [-2, -3, -4, 2, 1] })
    #TO-DO: 
    x_labels = [ "jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008" ]
    y_labels = [ "very low", "low", "medium", "high", "very high" ]
    dot_line_plot( "dot_line_2_dictionary_labels_series", data, 400, 300, x_labels = x_labels, 
                   y_labels = y_labels, axis = True, grid = True,
                   x_title = "x axis", y_title = "y axis", series_legend=True )
    
    
    ######### Teste 3 ###########
    #Series legend
    data = { "john" : [10, 10, 10, 10, 30], "mary" : [0, 0, 3, 5, 15], "philip" : [13, 32, 11, 25, 2] }
    x_labels = [ "jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008" ]
    cairoplot.dot_line_plot( 'dot_line_3_series_legend_cairoplot', data, 400, 300, x_labels = x_labels, 
                             axis = True, grid = True, series_legend = True )
    
    data = Serie({ "john" : [10, 10, 10, 10, 30], "mary" : [0, 0, 3, 5, 15], "philip" : [13, 32, 11, 25, 2] })
    x_labels = [ "jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008" ]
    dot_line_plot( 'dot_line_3_series_legend_series', data, 400, 300, x_labels = x_labels, 
                   axis = True, grid = True, series_legend = True )
    
if test_gantt_chart:
    #Default Plot
    pieces = [ (0.5,5.5) , [(0,4),(6,8)] , (5.5,7) , (7,9)]
    x_labels = [ 'label 01', 'label 02 tem que ser grande', 'l03', 'label 04']
    y_labels = [ '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010' ]
    colors = [ (1.0, 0.0, 0.0), (1.0, 0.7, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0) ]
    cairoplot.gantt_chart('gantt_1_default_cairoplot.png', pieces, 500, 350, x_labels, y_labels, colors)

    pieces = Serie({'label 01':(0.5,5.5) , 'label 02 tem que ser grande':[(0,4),(6,8)] , 'l03':(5.5,7) , 'label 04':(7,9)})
    gantt_chart('gantt_1_default_series.png', pieces, 500, 350, y_labels, colors)


raw_input()
