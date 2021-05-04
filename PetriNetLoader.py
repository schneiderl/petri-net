import json
from Place import Place
from Transition import Transition
from Arc import Arc


class PetriNetLoader():
	def __init__(self):
		self.places = []
		self.transitions = []
		self.transition_index = {}

	def __initialize_places__(self, number_of_places):
		for x in range(0, number_of_places):
			self.places.append(Place("P"+str(x+1)))

	def __initialize_transitions__(self, number_of_transitions):
		for x in range(0, number_of_transitions):
			self.transitions.append(Transition("T"+str(x+1)))
			self.transition_index["T"+str(x+1)] = x

	def __load_place_marks__(self, list_of_marks):
		for x, mark in enumerate(list_of_marks):
			self.places[x].set_mark_count(mark)

	def __load_transition_entries__(self, transition_entries):
		# from place -> transition
		for x, entries in enumerate(transition_entries):
			for entry in entries:
				new_arc = Arc(self.places[entry-1].name+self.transitions[x].name, self.transitions[x], self.places[entry-1])
				self.transitions[x].arcs_in.append(new_arc)
				self.places[entry-1].arcs_out.append(new_arc)
	
	def __load_transition_entries_weights__(self, entries_weights):
		for x, weights in enumerate(entries_weights):
			for y, archs in enumerate(self.transitions[x].arcs_in):
				self.transitions[x].arcs_in[y].weight = weights[y]

	def __load_transition_exits__(self, transition_exits):
		#from transitions -> places - loop at transitions 
		for transition_id, exits in enumerate(transition_exits):
			for place in exits:
				new_arc = Arc(self.transitions[transition_id].name + self.places[place-1].name, self.transitions[transition_id], self.places[place-1])
				self.transitions[transition_id].arcs_out.append(new_arc)
				self.places[place-1].arcs_in.append(new_arc)

	def __load_transition_exits_weights__(self, exit_weights):
		for x, weights in enumerate(exit_weights):
			for y, archs in enumerate(self.transitions[x].arcs_out):
				self.transitions[x].arcs_out[y].weight = weights[y]

	def __load_transition_exits_types__(self, exit_types):
		for x, exit_type in enumerate(exit_types):
			for y, archs in enumerate(self.transitions[x].arcs_out):
				self.transitions[x].arcs_out[y].set_type(exit_type[y]) 

	def __load_transition_entries_types__(self, entries_types):
		for x, entries_types in enumerate(entries_types):
			for y, archs in enumerate(self.transitions[x].arcs_in):
				self.transitions[x].arcs_in[y].set_type(entries_types[y])


	def load_network(self, filename):
		f = open(filename)
		network_data = json.load(f)
		self.__initialize_places__(network_data['number_of_places'])
		self.__initialize_transitions__(network_data['number_of_transitions'])
		self.__load_place_marks__(network_data['marks'])
		self.__load_transition_entries__(network_data['transition_entries'])
		self.__load_transition_entries_weights__(network_data['transition_entries_weights'])
		self.__load_transition_exits__(network_data['transition_exits'])
		self.__load_transition_exits_weights__(network_data['transition_exits_weights'])
		self.__load_transition_exits_types__(network_data['transition_exits_types'])
		self.__load_transition_entries_types__(network_data['transition_entries_types'])
		return self.transitions, self.places, self.transition_index
