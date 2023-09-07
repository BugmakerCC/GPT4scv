import re
import os

def create_directory(name):
    if not os.path.exists(name):
        os.mkdir(name)

def char_obfuscation(word):
    transtab = str.maketrans('loisg', '10l59')
    word = word.translate(transtab)
    if word[0].isdigit():
        word = "_" + word
    return word

def obscure_var_name(text, strategy):
    variable_pattern = r'\b(address|uint|int|string|bool|bytes|mapping\s*\([^\)]*\))\s+(public|private|internal|external|indexed)?\s*([a-zA-Z_][a-zA-Z0-9_]*)\b'
    replacement_dict = {}
    for match in re.findall(variable_pattern, text):
        if strategy == 'char_obfuscation':
            replacement_dict[match[2]] = char_obfuscation(match[2])
    for original, replacement in replacement_dict.items():
        text = re.sub(r'\b' + original + r'\b', replacement, text)
    return text

def process(name, path, strategy, vulnerability):
    with open(path, 'r') as file:
        content = file.read()
    content = obscure_var_name(content, strategy)
    with open(f'mutation/{strategy}/{vulnerability}/{name}', 'w') as file:
        file.write(content)

mutation_strategies = ['synonym', 'char_obfuscation', 'split', 'combine', 'noise', 'mask', 'swap']

if not os.path.exists('mutation'):
    os.mkdir('mutation')

for vulnerability in os.listdir('processed'):
    contract_li = os.listdir(f'processed/{vulnerability}')
    path_li = [os.path.join(f'processed/{vulnerability}', contract) for contract in contract_li]
    for strategy in mutation_strategies:
        if not os.path.exists(f'mutation/{strategy}/{vulnerability}'):
            os.makedirs(f'mutation/{strategy}/{vulnerability}')
        for i in range(len(contract_li)):
            process(contract_li[i], path_li[i], strategy, vulnerability)