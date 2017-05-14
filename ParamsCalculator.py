import numpy as np
import scipy.interpolate
import interpolate

def calculateModelParameters(data, parameterNumber, paramIndex):
    parameters = np.zeros([data.shape[0], parameterNumber])

    parameters[:, 0] = (data[:,1]*data[:,18])/((data[:,8] + data[:,12])*data[:,18])
    parameters[:, 1] = (data[:,0]*data[:,18]*((100 - data[:,19])/100))/((data[:,8] + data[:,12])*data[:,18])
    parameters[:, 2] = (data[:,0]*data[:,18]*(data[:,19]/100))/((data[:,8] + data[:,12])*data[:,18])
    parameters[:, 3] = data[:,4]/data[:,9]
    parameters[:, 4] = (data[:, 3] * ((100 - data[:, 19])/100)) / (data[:, 8] * 0.24)
    parameters[:, 5] = (data[:, 3] * (data[:, 19]/100)) / (data[:, 8] * 0.76)
    parameters[:, 6] = data[:, 6] / data[:, 14]
    parameters[:, 7] = (data[:, 5] * ((100 - data[:,19])/100)) / (data[:, 13] * 0.24)
    parameters[:, 8] = (data[:, 5] * (data[:, 19] / 100)) / (data[:, 13] * 0.76)

    shiftValue = -data[0:-1,18] + data[1:,18] + data[0:-1,11] - data[1:,11] + data[0:-1,14] - data[1:,14];

    parameters[0:-1, 9] = (shiftValue + data[0:-1,20]) / data[0:-1,18]
    parameters[-1: 9] = 0

    return {
        'y': parameters[:, paramIndex],
        'x': np.arange(0, parameters.shape[0], 1)
    }

def calcOptimalShiftParams(data, parameterNumber, paramIndex, plot_type):
    parameters =  calculateModelParameters(data, parameterNumber, paramIndex)['y']
    parameterInterval = 12

    Y_t = np.array([0.043864669522844, 0.0474646626618323, 0.0512417636214026, 0.0525199643025881, 0.0523689531480009,
                    0.0541360764551082,
                    0.0614571024310766, 0.0692891722931811, 0.0725887824340051, 0.071314494951363, 0.0724829996614131,
                    0.0711435652676975,
                    0.0605516431409567, 0.0574131888645759, 0.054618666254454])

    X_t = np.arange(0, data.shape[0], parameterInterval)
    X_t = np.append(X_t, 165)

    y_interp = scipy.interpolate.interp1d(X_t, Y_t)
    Y = y_interp(np.arange(0, 165, 1))
    return findShiftParameters(parameters, Y,plot_type)

def findShiftParameters(Y_data, X_data, plot_type):
    shiftInterval = 6
    shiftRange = np.arange(0,48,shiftInterval)
    errorRange = np.zeros(len(shiftRange))

    data = {
        'y': Y_data,
        'x': X_data
    }

    paramIndentityFactory = interpolate.FunctionIndenfy(data, 0)
    zeroShiftParams = paramIndentityFactory.LinearParamIndentify(plot_type)

    print 'plot type is : ' + str(plot_type)

    if plot_type == 0:
        data['predict_y'] = paramIndentityFactory.calcLinearFuncValues(zeroShiftParams)
    else:
        data['predict_y'] = paramIndentityFactory.calcNonLinearFuncValues(zeroShiftParams)

    for shift in shiftRange:
        paramIndentityFactory = interpolate.FunctionIndenfy(data, shift)
        currParam = paramIndentityFactory.LinearParamIndentify(plot_type)
        errorRange[shift/shiftInterval] = paramIndentityFactory.Error(currParam, 0)

    print errorRange
    data['errors'] = errorRange
    return data


