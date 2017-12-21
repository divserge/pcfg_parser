from pparser import Parser

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

def tuple_to_str(inp_tuple):
    out_string = "("
    for elem in inp_tuple:
        if type(elem) == str:
            out_string += elem + " "
        else:
            out_string += tuple_to_str(elem)
    out_string += ")"
    return out_string


def writeout_parses(parser, input_file, output_file):
    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        k = 0
        for l in fin:
            sent = [w.split('^')[0] for w in l.split()[:-1]][:20]
            line = ' '.join(sent)
            kek = parser.parse(line)
            k += 1
            if k % 100 == 0:
                fout.flush()
            print(tuple_to_str(kek), file=fout)


def test_parser(approximation, rules_path, rank, input_file, output_folder):
    rules, root = parse_grammars(path=rules_path)
    p = Parser(rules, root, approximation=approximation, rank=rank)
    writeout_parses(
        input_file,
        '{}/test_{}_{}.txt'.format(output_folder, approximation, rank)
    )