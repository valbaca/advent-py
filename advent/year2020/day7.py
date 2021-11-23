import re

from advent.elf import lines

"""
Given this was the first graph problem and one with such a "human" input, I was worried this would take a very long time
Ended up not taking long at all.
I knew the bag counts was going to matter for part 2, but still kept it out of the graph for part 1.
It can be hard deciding between the boundary of parsing and solving, but after doing enough, I'm starting to get it.

Python tuples make it especially easy to just return a list of tuples and then have the execution part of the code deal
with generating the data structures.
"""


def parse(line):
    # line = "light red bags contain 1 bright white bag, 2 muted yellow bags."
    splits = re.split(r"[\s,.]", line)
    top = str.join(" ", splits[:2])
    inside = []
    for i in range(4, len(splits), 5):
        count, luster, hue, *rest = splits[i:i + 5]
        color = f"{luster} {hue}"
        if not (count == "no" and color == "other bags"):
            inside.append((color, count))
    return top, inside


def to_graph(inp):
    graph = {}
    for top, inside in inp:
        graph[top] = list(map(lambda x: x[0], inside))
    return graph


def contains(graph, color, target):
    within = graph[color]
    if target in within:
        return True
    else:
        for c in within:
            if contains(graph, c, target):
                return True
    return False


def color_int_count(color_count):
    if not color_count:
        return color_count
    c, count = color_count
    return c, int(count)


def to_counting_graph(inp):
    return {top: list(map(color_int_count, color_count)) for top, color_count in inp}


def count_bags(graph, top_color):
    total = 0
    for color, count in graph[top_color]:
        total += count
        total += (count * count_bags(graph, color))
    return total


def main():
    inp = lines(__file__, parse)

    # print(inp)
    graph = to_graph(inp)
    # print(graph)
    # part 1
    print(len([k for k in graph.keys() if contains(graph, k, "shiny gold")]))

    # part 2
    counting_graph = to_counting_graph(inp)
    # print(counting_graph)
    print(count_bags(counting_graph, "shiny gold"))


if __name__ == '__main__':
    main()
