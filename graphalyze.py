import numpy as np
import matplotlib.pyplot as plt

class OutOfBoundsError(ArithmeticError):
    def __init__(self, val, bounds, *args, **kwargs):
        super(OutOfBoundsError, self).__init__(*args, **kwargs)
        self.val = val
        self.bounds = bounds

    def __str__(self):
        return "Value out of bounds: {0} not within [{1}, {2}].".format(self.val, *self.bounds)


class GraphicalAnalysis(object):
    def __init__(self, func, x_min=0, x_max=1, y_min=0, y_max=1, samples=400):
        self._limits = [x_min, x_max, y_min, y_max]
        self._func = func
        self._x = np.linspace(x_min, x_max, samples)
        self._figure = plt.figure()
        self._figure.canvas.mpl_connect('button_press_event', self._mouse_clicked)
        self._figure.canvas.mpl_connect('motion_notify_event', self._mouse_moved)
        self._figure.canvas.mpl_connect('key_press_event', self._key_pressed)
        self._redraw()

    def clear(self):
        self._figure.gca().cla()
        self._line = None
        self._dots = None
        self._indicator = None
        self._orbit = []
        self._figure.canvas.draw()

    @property
    def f(self):
        return self._func

    @f.setter
    def f(self, val):
        if self._func != val:
            self._func = val
            self._redraw()

    def _draw_graph(self):
        ax = self._figure.gca()
        ax.plot(self._x, self._func(self._x), '-b')
        self._figure.canvas.draw()

    def _draw_identity(self):
        ax = self._figure.gca()
        ax.plot(self._x, self._x, '-k')
        self._figure.canvas.draw()

    def _make_orbit(self, x0):
        self._orbit = [x0]
        while True:
            x = self._orbit[-1]
            y = self._func(x)
            if y < self._limits[0] or y > self._limits[1]:
                raise OutOfBoundsError(y, self._limits[0:2])
            if abs(x - y) < 1e-3 or len(self._orbit) > 500:
                break
            self._orbit.append(y)

    def _draw_orbit(self):
        x, y = [], []
        for i in xrange(len(self._orbit) - 1):
            x.append(self._orbit[i])
            x.append(self._orbit[i])
            y.append(self._orbit[i])
            y.append(self._orbit[i + 1])
        x.append(self._orbit[-1])
        y.append(self._orbit[-1])
        ax = self._figure.gca()
        if self._line is not None and self._dots is not None:
            self._line.set_data(x, y)
            self._dots.set_data(self._orbit, self._orbit)
        else:
            self._line = ax.plot(x, y, 'r-')[0]
            self._dots = ax.plot(self._orbit, self._orbit, 'ro')[0]
        self._figure.canvas.draw()

    def _draw_indicator(self, x):
        if self._indicator is not None:
            self._indicator.set_data([x, x], self._limits[2:4])
        else:
            ax = self._figure.gca()
            self._indicator = ax.plot([x, x], self._limits[2:4], 'c:')[0]
        self._figure.canvas.draw()

    def _mouse_clicked(self, event):
        if event.inaxes == self._figure.gca():
            self.run(event.xdata)

    def _mouse_moved(self, event):
        if event.inaxes == self._figure.gca():
            self._draw_indicator(event.xdata)

    def _key_pressed(self, event):
        if event.key == 'escape':
            plt.close()
        elif event.key == 'up':
            self._func.increase_param()
            self._redraw()
        elif event.key == 'down':
            self._func.decrease_param()
            self._redraw()

    def _redraw(self):
        self.clear()
        ax = self._figure.gca()
        ax.axis(self._limits)
        ax.set_title(r'$\mu = ' + str(self._func.param) + r'$')
        self._draw_graph()
        self._draw_identity()

    def run(self, x0):
        self._make_orbit(x0)
        self._draw_orbit()

class LogisticFamily(object):
    def __init__(self, mu=2.5):
        self._mu = mu

    def __call__(self, x):
        return self._mu * x * (1.0 - x)

    @property
    def mu(self):
        return self._mu

    @mu.setter
    def mu(self, val):
        self._mu = val

    param = mu

    def increase_param(self, amount=0.1):
        self._mu += amount

    def decrease_param(self, amount=0.1):
        self._mu -= amount

if __name__ == '__main__':
    g = GraphicalAnalysis(LogisticFamily(2))
    plt.show()
