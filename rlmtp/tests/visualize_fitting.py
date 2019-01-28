from rlmtp.filtering import reduce_data
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0., 2 * 3.14, 100)
noise = np.random.rand(len(x)) / 20.
y = np.sin(x) + noise


x = np.linspace(0., 100, 100)
noise = np.random.rand(len(x)) * 5.
y = 1. * x + noise

t = np.linspace(0., 1., 100)
anchors = [0, 10, 20, 80]

[xn, yn, tn] = reduce_data(x, y, t, anchors, 20, 1)

plt.figure()
#plt.plot(x, y, 'o', c='0.63', ms=2)
plt.plot(x, y, '-', c='0.63', ms=2)
plt.plot(xn, yn, 'ko')
plt.plot(x[anchors], y[anchors], 'ro', label='Anchors')
plt.plot(xn[[1, 3, 5, 7, 9]], yn[[1, 3, 5, 7, 9]], 'bo', label='Fitted')
plt.plot(xn, yn, 'k')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.tight_layout()
plt.savefig('./output/filter_visualize.pdf')
plt.show()
