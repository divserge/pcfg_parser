


def parse_grammars(path):
	grammars = {}
	root_syms = {}

	with open(path, 'r') as file:
		for line in file:
			content = line.split()
			if content[0] in ['interminals', 'preterminals']:
				for sym in content[1:]:
					grammars[sym] = []
			elif content[0] == 'root':
				root_syms[content[1]] = float(content[-1].split(':')[-1])
			elif content[0] == 'term':
				fr = content[1]
				to = content[3]
				prob = float(content[-1].split(':')[-1])
				grammars[fr].append((to, prob))
			elif content[0] == 'binary':
				fr = content[1]
				to = content[3] + ' ' + content[4]
				prob = float(content[-1].split(':')[-1])
				grammars[fr].append((to, prob))

	return grammars, root_syms





