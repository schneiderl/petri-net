import json
from Place import Place
from Transition import Transition
from Arc import Arc
from PetriNetLoader import PetriNetLoader
import sys
from ArcTypesEnum import ArcTypes


class PetriNet:
	def __init__(self, net_descriptor):
		petri_loader = PetriNetLoader()
		self.transitions, self.places, self.transition_index  = petri_loader.load_network(net_descriptor)

	def set_marks(self, place, number_of_marks):
		self.places[place].set_mark_count()

	def get_enabled_transition(self):
		enabled_transitions = []
		for transition in self.transitions:
			transition_enabled = True
			for arc in transition.arcs_in:
				if arc.get_type() == ArcTypes.regular.value:
					if arc.place.mark_count < arc.weight:
						transition_enabled = False
				elif arc.get_type() == ArcTypes.inhibitor.value:
					if arc.place.mark_count >= arc.weight:
						transition_enabled = False
			if transition_enabled:
				enabled_transitions.append(transition.name)

		return enabled_transitions


	def trigger_transition(self, transition_name):
		if transition_name in self.get_enabled_transition():
			transition = self.transitions[self.transition_index[transition_name]]			
			for arc in transition.arcs_in:
				if arc.get_type() == ArcTypes.regular.value:
					arc.place.set_mark_count(arc.place.get_mark_count() - arc.weight)	
				elif arc.get_type() == ArcTypes.reset.value:
					arc.place.set_mark_count(0)
			for arc in transition.arcs_out:
				arc.place.set_mark_count(arc.place.get_mark_count() + arc.weight)
		else:
			print("transition not enabled.")

	def get_places_names(self):
		place_names = []
		for place in self.places:
			place_names.append(place.name)
		return place_names



	def print_network(self):
		places_str = "PLACES: "
		marks_str = "MARKS:   "
		for x in self.places: 
			places_str = places_str + x.name + "  |  "
			marks_str = marks_str + str(x.mark_count) + "   |  " 
		print("***************************************************")
		print(places_str)
		print(marks_str)
		print("***************************************************")
		print("\n")

		transitions_str = "TRANSITIONS: "
		enabled_transitions_str = "ENABLED?      "
		enabled_transitions_list = self.get_enabled_transition()
		for transition in self.transitions:
			transitions_str = transitions_str + transition.name + "  |  "
			if transition.name in enabled_transitions_list:
				enabled_transitions_str = enabled_transitions_str + "Y  |   "
			else:
				enabled_transitions_str = enabled_transitions_str + "N  |   "

		print("***************************************************")
		print(transitions_str)
		print(enabled_transitions_str)
		print("***************************************************")



net_descriptor = sys.argv[1]
petrinet = PetriNet(net_descriptor)
petrinet.print_network()

cycle_count = 0

while True:
	print("Cycle number: " + str(cycle_count) + "\n")
	cycle_count += 1
	i = input("Press enter to go to the next cycle ")
	enabled_transitions = petrinet.get_enabled_transition()
	if len(enabled_transitions) != 0:
		for transition in enabled_transitions:
			petrinet.trigger_transition(transition)
	else: 
		break
	petrinet.print_network()


print("There is no enabled transitions.")