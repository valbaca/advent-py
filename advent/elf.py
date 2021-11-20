def howdy():
    print("Howdy!")


def lines(file, parseFn=None):
    text_file = file.replace(".py", ".txt")
    return _lines(text_file, parseFn)

def test_lines(file, parseFn=None):
    text_file = file.replace(".py", "-test.txt")
    return _lines(text_file, parseFn)

def _lines(filename, parseFn=None):
    with open(filename, "r") as f:
        xs = list(f.readlines())
        if parseFn:
            xs = list(map(parseFn, xs))
        return xs
