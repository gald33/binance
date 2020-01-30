import numpy as np
from pprint import pprint

class Sma_handler:
    def __init__(self):
        pass
    def sma(self, x, N):
        cumsum = np.cumsum(np.insert(x, 0, 0))
        li = list((cumsum[N:] - cumsum[:-N]) / float(N))
        # pad list at the beginning
        return [None] * (len(x) - len(li)) + li

class Peak:
    def __init__(self, i, value, delta):
        self.delta = delta
        self.high = value + delta

        self.low = value - delta
        self.value = value
        self.count = 1
        self.list_of_indices = [i]
    def in_range(self, new_value):
        if new_value < self.high and new_value > self.low:
            return True

    def new_high(self, new_value):
        self.high = new_value + self.delta
        self.value = (self.low + self.high)/2

    def new_low(self, new_value):
        self.low = new_value + self.delta
        self.value = (self.low + self.high)/2

    def new_range(self, i, new_value):
        self.count += 1
        self.list_of_indices.append(i)
        if new_value > self.value:
            self.new_high(new_value)
        if new_value < self.value:
            self.new_low(new_value)

class Line:
    def __init__(self, x0, x1, y0, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.a = self.line_gradient()
        self.b = self.line_intersect()

    def line_gradient(self):
        return float(self.y1 - self.y0) / float(self.x1 - self.x0)

    def line_intersect(self):
        return self.y0 - self.a * self.x0

    def line_value(self, x):
        return self.a * x + self.b


class Peak_handler:
    def __init__(self, values):
        self.values = values
        self.max_peaks = {}
        self.min_peaks = {}
        self.max_lines = []
        self.min_lines = []
        self.global_max = 0

    def find_peaks(self, num_of_periods, delta_factor):
        max_values = []
        min_values = []
        delta = 0
        for i in xrange(len(self.values)-1 - num_of_periods, len(self.values)-1, 1):
            # update delta
            if self.values[i] > self.global_max:
                self.global_max = self.values[i]
                delta = self.global_max * delta_factor
                # print 'i,gm',i,self.global_max
            # is this a new max
            if self.values[i-1] < self.values[i] and self.values[i+1] < self.values[i]:
                found_max = False
                for peak in max_values:
                    if peak.in_range(self.values[i]):
                        peak.new_range(i, self.values[i])
                        found_max = True
                        break
                if not found_max:
                    self.max_peaks[i] = Peak(i, self.values[i], delta)
                    max_values.append(self.max_peaks[i])
            # is this new min
            elif self.values[i-1] > self.values[i] and self.values[i+1] > self.values[i]:
                found_min = False
                for peak in min_values:
                    if peak.in_range(self.values[i]):
                        peak.new_range(i, self.values[i])
                        found_min = True
                        break
                if not found_min:
                    self.min_peaks[i] = Peak(i, self.values[i], delta)
                    min_values.append(self.min_peaks[i])
        return max_values, min_values

    # find lines between maxs (or mins, later) with that aren't cut by other point. delta is the allowed small cut
    def find_lines(self, delta_factor):
        delta = delta_factor * self.global_max
        for i in self.max_peaks:
            for j in self.max_peaks:
                if i < j:
                    # compare all the values in the middle with the line value
                    line = Line(i, j, self.max_peaks[i].value, self.max_peaks[j].value)
                    for x in xrange(i+1, len(self.values), 1):
                        if line.line_value(x) >= self.values[x] - delta or line.line_value(x) >= self.values[x] + delta:
                            pass
                        else:
                            break
                    # if didn't break, it's a good line
                    self.max_lines.append(line)
                    print 'line found'
        return self.max_lines

    #mark as all values of a list, used for drawing resistance and support
    def value_to_list(self, value, original_list):
        return [value] * len(original_list)

    def line_to_list(self, line, original_list):
        li = []
        for x in xrange(len(original_list)):
            li.append(line.line_value(x))
        return li


