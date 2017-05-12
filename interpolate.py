import numpy as np
import scipy.interpolate
import scipy.optimize


class FunctionIndenfy(object):
    def __init__(self, data, parent=None):
        object.__init__(self)
        self.X_data = data['x']
        self.Y_data = data['y']

    def func(self, param):
        m = self.X_data.shape[0]
        return np.sum((np.dot(self.X_data, param.T) - self.Y_data)**2)/2*m

    def calcLinearFuncValues(self, params):
        return params[0] + params[1]*self.X_data[:,1]

    def LinearParamIndentify(self):
        X = np.zeros([self.X_data.shape[0], 2])
        X[:, 0] = 1
        X[:, 1] = self.X_data
        self.X_data = X

        params = scipy.optimize.fmin_cg(self.func, [0, 1])
        print  params
        return params

