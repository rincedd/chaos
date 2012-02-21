from matplotlib.backend_bases import MouseEvent, KeyEvent
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
        self.limits = [x_min, x_max, y_min, y_max]
        self.func = func
        self.x = np.linspace(x_min, x_max, samples)
        self.line = None
        self.indicator = None
        self.figure = plt.figure()
        self.figure.canvas.mpl_connect('key_press_event', self)
        self.figure.canvas.mpl_connect('button_press_event', self)
        self.figure.canvas.mpl_connect('motion_notify_event', self)
        self._draw_graph()
        self._draw_identity()

    def _draw_graph(self):
        ax = self.figure.gca()
        ax.axis(self.limits)
        ax.plot(self.x, self.func(self.x), '-b')
        self.figure.canvas.draw()

    def _draw_identity(self):
        ax = self.figure.gca()
        ax.plot(self.x, self.x, '-k')
        self.figure.canvas.draw()

    def _make_orbit(self, x0):
        self.orbit = [x0]
        while True:
            x = self.orbit[-1]
            y = self.func(x)
            if y < self.limits[0] or y > self.limits[1]:
                raise OutOfBoundsError(y, self.limits[0:2])
            if abs(x - y) < 1e-3 or len(self.orbit) > 500:
                break
            self.orbit.append(y)

    def _draw_orbit(self):
        x, y = [], []
        for i in xrange(len(self.orbit) - 1):
            x.append(self.orbit[i])
            x.append(self.orbit[i])
            y.append(self.orbit[i])
            y.append(self.orbit[i + 1])
        x.append(self.orbit[-1])
        y.append(self.orbit[-1])
        ax = self.figure.gca()
        if self.line is not None:
            self.line.set_data(x, y)
            self.dots.set_data(self.orbit, self.orbit)
        else:
            self.line = ax.plot(x, y, 'r-')[0]
            self.dots = ax.plot(self.orbit, self.orbit, 'ro')[0]
        self.figure.canvas.draw()

    def _draw_indicator(self, x):
        if self.indicator is not None:
            self.indicator.set_data([x, x], self.limits[2:4])
        else:
            ax = self.figure.gca()
            self.indicator = ax.plot([x, x], self.limits[2:4], 'c:')[0]
        self.figure.canvas.draw()

    def __call__(self, event):
        if isinstance(event, KeyEvent):
            if event.key == 'escape':
                plt.close()
        elif isinstance(event, MouseEvent):
            if event.inaxes == self.figure.gca():
                if event.button is None:
                    self._draw_indicator(event.xdata)
                else:
                    self.run(event.xdata)

    def run(self, x0):
        self._make_orbit(x0)
        self._draw_orbit()

if __name__ == '__main__':
    def quad(x, mu):
        return mu * x * (1 - x)

    g = GraphicalAnalysis(lambda x: quad(x, 3.7))
    plt.show()