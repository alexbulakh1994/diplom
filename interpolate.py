import numpy as np
import scipy.interpolate
import scipy.optimize

def func(param):
    m = X_t.shape[0]
    return np.sum((np.dot(X, param.T) - Y_t)**2)/2*m


Y_t = np.array([0.043864669522844, 0.0474646626618323, 0.0512417636214026, 0.0525199643025881, 0.0523689531480009, 0.0541360764551082,
                0.0614571024310766, 0.0692891722931811, 0.0725887824340051, 0.071314494951363, 0.0724829996614131,0.0711435652676975,
                0.0605516431409567,0.0574131888645759,0.054618666254454])

X_t = np.arange(0,165,12)
X_t = np.append(X_t, 165)

y_interp = scipy.interpolate.interp1d(X_t, Y_t)
Y_t = y_interp(np.arange(0,165,1))

X = np.zeros([165, 2])

X[:,0] = 1


params = scipy.optimize.fmin_cg(func, [0, 1])
print  params