import numpy as np
import scipy.interpolate
import scipy.optimize

class FunctionIndenfy(object):
    def __init__(self, data, shift, parent=None):
        object.__init__(self)
        rowLen = data['x'].shape[0]
        self.X_data = data['x'][shift:]
        self.Y_data = data['y'][0:rowLen-shift]
        self.optimal_shift = shift

    def func(self, param):
        m = self.X_data.shape[0]
        crossValidSize = m*0.8
        return np.sum((np.dot(self.X_data[0:crossValidSize,:], param.T) - self.Y_data[0:crossValidSize])**2)/(2*crossValidSize)

    def NonLinearfunc(self, param):
        m = self.X_data.shape[0]
        crossValidSize = m*0.8
        return np.sum((np.dot(self.X_data[0:crossValidSize,:], param.T) - np.log(self.Y_data[0:crossValidSize]))**2)/(2*crossValidSize)

    def calcLinearFuncValues(self, params):
        return params[0] + params[1]*self.X_data[:,1]

    def calcNonLinearFuncValues(self, params):
        return np.exp(params[0] + params[1]*self.X_data[:,1])

    def Error(self, params, type):
        if type == 0:
            regressionValues = self.calcLinearFuncValues(params)
            return  (np.sum((self.Y_data - regressionValues)**2)) / (2 * len(self.Y_data))
        else:
            regressionValues = self.calcNonLinearFuncValues(params)
            return np.sum((self.Y_data - regressionValues) ** 2) / (2 * len(self.Y_data))

    def LinearParamIndentify(self, plot_type):
        X = np.zeros([self.X_data.shape[0], 2])
        X[:, 0] = 1
        X[:, 1] = self.X_data
        self.X_data = X

        if plot_type == 0:
            params = scipy.optimize.fmin_cg(self.func, [0, 1])
        else:
            params =  scipy.optimize.fmin_cg(self.NonLinearfunc, [0, 1])

        print  params
        return params

