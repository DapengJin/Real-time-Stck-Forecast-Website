# uses the previous homework written by Chengtian Liu
from __future__ import print_function
import sys
import numpy as np
# import matplotlib.pyplot as plt
import csv
from tkinter.filedialog import askopenfilename, asksaveasfile


def get_file(filename: str=None):
    if not filename:
        # Obtain and return the file name
        filename = askopenfilename()
    return open(filename, 'r')


def shape_input(x_vec, y_vec):
    x_vec = x_vec[-10:]
    y_vec = y_vec[-10:]
    y_vec = [i[0] for i in y_vec]
    return y_vec


class BayesianCurveFitting(object):
    def __init__(self, alpha=None, beta=None, polynomial=None):
        self.alpha = 5 * pow(10, -3) if not alpha else alpha
        self.beta = 11.1 if not beta else beta
        self.M = 3 if not polynomial else polynomial

    def variance(self, new_x, x_vec):
        S = self.matrix_S(x_vec)
        return (1 / self.beta) + (self.phi(new_x).T.dot(S).dot(self.phi(new_x)))[0][0]

    def phi(self, x:int):
        """
        This function calculates phi(x), where element phi_i(x) = x**i for i = 0,1,...,M
        :param x: a integer
        :return: np array phi(x)
        """
        dimension = self.M + 1  # We are including a constant here.
        p = [0] * dimension
        for i in range(dimension):
            p[i] += pow(x, i)
        p = np.array(p)
        p = p.reshape(p.shape + (1,))
        return p

    def mean(self, new_x, y_vec, x_vec):
        # return the mean value
        sum_vec_x = 0
        for i in range(len(x_vec)):
            sum_vec_x += self.phi(x_vec[i][0]) * y_vec[i][0]
        S = self.matrix_S(x_vec)
        return self.beta * ((self.phi(new_x).T.dot(S)).dot(sum_vec_x))[0][0]

    def matrix_S(self, x_vec):
        # return S matrix
        first_expr = self.alpha * np.eye(self.M + 1)
        second_expr = 0
        for i in range(len(x_vec)):
            second_expr += self.phi(x_vec[i][0]).dot(self.phi(x_vec[i][0]).T)
        return np.linalg.inv(first_expr + self.beta * second_expr)

    def predict(self, x_vec: list=None, new_x=None, y_vec: list=None):
        """
        :param x_vec: x values.
        :param new_x: the datapoint x to be predicted.
        :param y_vec: y values.
        :return: a predicted value.
        """
        if not y_vec:
            print("Error, no y values.")
            return
        else:
            y_vec = np.array([np.array([i]) for i in y_vec])
        if not x_vec:
            x_vec = np.array([np.array([float(i)]) for i in range(len(y_vec))])
            new_x = x_vec[-1][0] + 1
        else:
            assert len(x_vec) == len(y_vec)
            x_vec = np.array([np.array([i]) for i in x_vec])

        means = self.mean(new_x, y_vec, x_vec)
        variance = self.variance(new_x, x_vec)
        variances = (means - variance, means + variance)

        # print("means = ", means)
        # print("variance = ", variance)
        # x_vec_plot = np.append(x_vec, x_vec[-1][0]+1)
        # y_vec_plot = np.append(y_vec, means)
        # plt.figure()
        # plt.plot(x_vec_plot, y_vec_plot, c='green')
        # plt.scatter(x_vec_plot, y_vec_plot, c='red')
        # # ax.plot(new_x, miny, c='red')
        # # ax.plot(new_x, maxy, c='red')
        # plt.show()
        # plt.close()
        return means, variance

    def read_csv(self, filename: str = None, y_in_column: int = 4):
        """
        :param filename: The file name to load. Default is None, and will pop up a window to choose a file.
        :param y_in_column: The ith column for stock price y.
        :return: data blob
        """
        infile = get_file(filename)
        reader = csv.reader(infile, delimiter=",")
        if sys.version_info[0] == 3:
            reader.__next__()
        elif sys.version_info[0] == 2:
            reader.next()
        y_vec = []
        for line in reader:
            y_vec.append(np.array([float(line[y_in_column])]))
        x_vec = np.array([np.array([float(i)]) for i in range(len(y_vec))])
        y_vec = np.array(y_vec)

        # the first 15 points are moved for estimating the first m(x)
        data_init = shape_input(x_vec, y_vec)
        return data_init


if __name__ == '__main__':
    ###########
    # My result
    model = BayesianCurveFitting(alpha=5 * 10 ** (-3), beta=11.1, polynomial=3)
    ticker = 'NVDA'
    d_init = model.read_csv(filename='csv/'+ticker+'_historical.csv', y_in_column=4)
    print("Result of Estimation:")
    model.predict(y_vec=d_init)

