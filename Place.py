class Place:    

    def __str__(self):
    	print(self.name)
    	return "arcs out: " + str([str(x) for x in self.arcs_out]) + "\n marks: " + str(self.mark_count)

    def set_mark_count(self, mark):
    	self.mark_count = mark

    def get_mark_count(self):
        return self.mark_count

    def __init__(self, name):
    	self.name = name
    	self.arcs_out = []
    	self.arcs_in = []
    	self.mark_count = 0