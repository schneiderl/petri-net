class Transition:
    def __str__(self):
    	return "arcs in: " + str(self.arcs_in) + "\n arcs out: " + str(self.arcs_out)

    def __init__(self, name):
    	self.name = name
    	self.arcs_in = []
    	self.arcs_out = []
    	self.places = []