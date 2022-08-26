import tcod

letter_dict = {}
memor_count=2

class Letters:
	def __init__(self):
		self.dict = {}
		self.start = 0
		
	def add_letter(self, letter):
		if letter in self.dict:
			self.dict[letter] += 1
		else:
			self.dict[letter] = 1
			
	def get_random_letter(self):
		total = sum([self.dict[i] for i in self.dict])
		roll = tcod.random_get_int(0, 0, total-1)
		
		for i in self.dict:
			if roll < self.dict[i]:
				return i
			roll -= self.dict[i]
			
	def get_total(self):
		return sum([self.dict[i] for i in self.dict])
			
def load_letters(file_name="names.txt", memory=2):
	global memor_count
	memor_count = memory

	with open(file_name, "r") as f:
		lines = f.readlines()
		
		for line in lines:
			nline = "{}\n".format(line).lower()
			last_char = ""
			for char in nline:
				if last_char and len(last_char) == memor_count:
					if last_char not in letter_dict:
						letter_dict[last_char] = Letters()
					letter_dict[last_char].add_letter(char)
					last_char = last_char[-1:] + char
				else:
					if len(last_char) < memor_count:
						last_char += char
						if len(last_char) == memor_count:
							if last_char not in letter_dict:
								letter_dict[last_char] = Letters()
							letter_dict[last_char].start += 1
					else:
						last_char = char
				
def get_starting_letter():
	total = sum([letter_dict[i].start for i in letter_dict])
	roll = tcod.random_get_int(0, 0, total-1)
	
	for i in letter_dict:
		cstart = letter_dict[i].start
		if cstart > roll:
			return i
		roll -= cstart
		
def gen_name(min_length=4,max_length=9):
	string = get_starting_letter()
	return gen_name_with_start(string, min_length, max_length)
	
	
def gen_name_with_start(start, min_length=4, max_length=9):
	b_a = 0
	string = start
	while len(string) <= max_length:
		cchar = string[-memor_count:]
		nchar = letter_dict[cchar].get_random_letter()
		if nchar == "\n":
			b_a += 1
			if len(string) >= min_length or b_a > 3:
				break
		else:
			b_a = 0
			string += nchar
	if len(string) > max_length or b_a > 3:
		return gen_name_with_start(start, min_length, max_length)
	return string
	
def gen_multiple(count, min_length=4,max_length=9):
	list = []
	for i in range(0, count):
		list.append(gen_name(min_length, max_length))
	return list
