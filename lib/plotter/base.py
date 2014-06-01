class Plotter(object):
    """
    Plotter base
    """
    def __init__(self, root, name, data):
        self.data = data
        self.root = root
        self.name = name
