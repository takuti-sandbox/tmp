def build(keywords):
    tree = dict()
    for keyword in keywords:
        node = tree
        for c in keyword:
            if c not in node:
                node[c] = dict()
            node = node[c]
        node[-1] = None
    return tree


def match(tree, text):
    for i, ci in enumerate(text):
        if ci not in tree:
            continue
        node = tree[ci]

        pos, word = i, ci
        tail = len(text[(i + 1):]) - 1
        for j, cj in enumerate(text[(i + 1):]):
            if -1 in node:
                yield pos, len(word), word
            if cj not in node:
                break
            word += cj
            node = node[cj]
            if j == tail:
                yield pos, len(word), word


if __name__ == '__main__':
    tree = build(['he', 'hers', 'his', 'she'])
    print(tree)
    print(list(match(tree, 'a his hoge hershe')))
