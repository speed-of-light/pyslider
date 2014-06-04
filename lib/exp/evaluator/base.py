class Evaluator(object):
    def __init__(self):
        pass

    def fbeta(self, precision, recall, beta=1):
        """
        F1: for bata = 0.5, also called f1 score
        F2: for bata = 1
        """
        return (1+beta**2)*precision*recall/((beta**2)*precision+recall)

    def praf(self, tp, fp, tn, fn):
        precision = tp*1.0/(tp+fp)
        recall = tp*1.0/(tp+fn)
        accuracy = (tp+tn)*1.0/(tp+tn+fp+fn)
        fmeasure = self.fbeta(precision, recall, .5)
        print self.__praf_str(precision, recall, accuracy, fmeasure)

    def __praf_str(self, p, r, a, f):
        aa = []
        aa.append("Precision: {:.3f}".format(p))
        aa.append("Recall: {:.3f}".format(r))
        aa.append("Accuracy: {:.3f}".format(a))
        aa.append("Fmeasure: {:.3f}".format(f))
        ast = ""
        for a_ in aa:
            ast += "{}\n".format(a_)
        return ast
