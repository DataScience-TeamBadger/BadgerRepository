# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:04:06 2017

@author: Michael von der Lippe
"""

# Import NumPy
import numpy as np

# Import PyQtGraph library
import pyqtgraph as pg

# Import Model superclass
import models.Model

class coverage(models.Model.Model):

    def __init__(self, name, coverage_data):
        super(coverage, self).__init__(name)


        self.X = np.asarray(coverage_data[0])
        self.Y = np.asarray(coverage_data[1])

        self.plot.plot(self.X, self.Y, pen=None, symbol='o')
