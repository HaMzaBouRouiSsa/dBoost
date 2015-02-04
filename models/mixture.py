import numbers
from utils.tupleops import sys
from utils.autoconv import autoconv
from math import erf,sqrt

class Mixture:
    ID = "mixture"

    def __init__(self, n_components, cutoff):
        self.n_components = n_components
        self.cutoff = cutoff

    def reset(self):
        self.gmms    = None
        self.cutoff  = None
        self.keep    = None

    @staticmethod
    def register(parser):
        parser.add_argument("--" + Mixture.ID, nargs = 2, metavar = ("n_subpops", "threshold"),
                            help = "Use a gaussian mixture model, reporting values whose probability is " +
                            "below the threshold, as predicted by a model of the data comprised of n_subpops "+
                            "gaussians. Suggested values: 2, 0.3.")

    @staticmethod
    def from_parse(params):
        return Mixture(*map(autoconv, params))

    def mahalanobis(self, x, gmm, component):
        mean = gmm.means_[component]
        covar = gmm.covars_[component]
        u = x - mean
        v = u.transpose()

        return sqrt(v.dot(((1 / covar) * u).transpose()))

    def make_gmm(self, to_fit):
        from sklearn import mixture
        gmm = mixture.GMM(n_components = self.n_components)
        gmm.fit(to_fit)
        return gmm
        
    def fit(self, Xs, analyzer):
        from matplotlib import pyplot

        correlations = zip(*(X[0] for X in Xs))
        self.gmms = [self.make_gmm(to_fit) for to_fit in correlations]

        # TODO: add command line option to show graph
        # lp, resp = self.gmms[i].score_samples(to_fit)
        # ps = [self.test_one(x, i) for x in to_fit]
        # pyplot.hist(ps, bins = 30)
        # pyplot.show()

    def test_one(self, xi, gmm_pos):
        from numpy import argmax
        gmm = self.gmms[gmm_pos]
        _, resp = gmm.score_samples([xi])
        explain = argmax(resp)
        distance = self.mahalanobis(xi, gmm, explain)
        return gmm.weights_[explain] *  erf(distance / sqrt(2))

    def find_discrepancies(self, X, index):
        correlations = X[0]
        discrepancies = []

        for id, (correlation, gmm_pos, cutoff) in enumerate(zip(correlations, range(len(self.gmms)), range(len(self.gmms)))):
            if self.test_one(correlation, gmm_pos) < self.cutoff:
                discrepancies.append(((0, id),))

        return discrepancies

    def more_info(self, discrepancy, description, X, indent = "", pipe = sys.stdout):
        pass #TODO
