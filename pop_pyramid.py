# -*- coding: utf-8 -*-
# Numpy functions for image creation
import numpy as np
# Matplotlib Figure object
from matplotlib.figure import Figure
# import the Qt4Agg FigureCanvas object, that binds Figure to Qt4Agg backend. It also inherits from QWidget
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import math
import matplotlib.pyplot as plt
import matplotlib as mpl

   
    
class Qt4MplCanvas(FigureCanvas): 
         """Class to represent the FigureCanvas widget""" 
         def __init__(self,name, men_pop, women_pop, year):
             
            mpl.rcParams['font.family'] = 'DejaVu Sans' #set font
            
            self.men_pop   = np.array(men_pop) 
            self.women_pop = np.array(women_pop)
            self.perc_men_pop = 100*self.men_pop.astype('float')/sum(self.men_pop.astype('float') + self.women_pop.astype('float')) #men age group population as percent of total population  
            self.perc_women_pop = 100*self.women_pop.astype('float')/sum(self.men_pop.astype('float') + self.women_pop.astype('float') )#women age group population as percent of total population  
            self.name = name 
            self.year = str(year)
             
            # Standard Matplotlib code to generate the plot
            self.fig  = Figure()
            self.axes = self.fig.add_subplot(111)


            self.maxvalue  = max(max(self.perc_men_pop), max(self.perc_women_pop))#max value of men and women

            self.roundmax  = int(math.ceil(self.maxvalue)) #round up to integer e.g 4.2->5

            self.positiveX = range(0,self.roundmax+1,1)
            self.negativeX = range(0,-self.roundmax-1,-1)[::-1]     
            self.xtickslist = self.negativeX + [i for i in self.positiveX if i not in self.negativeX]


            self.X = np.arange(len(self.perc_men_pop))
            self.axes.barh(self.X, self.perc_women_pop, color = 'lightpink', label=u"Θήλεις", height=1, left=0)
            self.axes.barh(self.X, -self.perc_men_pop, color = 'lightblue', label=u'´Αρρενες', height=1,left=0)
        
            self.mylabels=["%i-%i" %(i,i+4) for i in range(0,85,5)]
            self.mylabels.append("85+")
        
            self.xticks=np.array(self.xtickslist)
        
            self.axes.set_xticks(self.xticks, minor=False)
            self.axes.set_xticklabels(np.absolute(self.xticks))
            self.axes.set_yticklabels(self.mylabels)
            self.axes.set_yticks(np.arange(0.5,len(self.mylabels), 1));
            self.axes.set_title(u"Πληθυσμιακή πυραμίδα \n %s \n Έτος %s" % (self.name,self.year),fontsize=14 )
        
            self.axes.set_ylabel(u"Ηλικιακή ομάδα")
            self.axes.set_xlabel(u"(%)")
            self.axes.legend()
        

            self.axes.xaxis.grid() #vertical lines

            

            # initialize the canvas where the Figure renders into
            FigureCanvas.__init__(self, self.fig)