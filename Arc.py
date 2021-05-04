class Arc:
    def __str__(self):
    	pass
        #return "name: " + self.name# + "\n transition: " + #str(self.transition) + "\n place" + #str(self.place)
    
    def __init__(self, name, transition, place):
    	self.name = name
    	self.weight = 0
    	self.transition = transition
    	self.place = place
    	self.arc_type = 0

    def set_type(self, arc_type):
    	self.arc_type = arc_type

    def get_type(self):
    	return self.arc_type
        