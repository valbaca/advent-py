def main():
    tls_total = 0
    ssl_total = 0
    with open('day7.txt') as file:
        for line in file:
            ln = line.strip()
            if supports_tls(ln):
                tls_total += 1
            if supports_ssl(ln):
                ssl_total += 1
    print(tls_total, ssl_total)


def supports_tls(s):
    found_abba = False
    groups = split_groups(s)
    for group in groups:
        if group.startswith('[') and has_abba(group):
            return False
        elif not found_abba and has_abba(group):
            found_abba = True
    return found_abba


def supports_ssl(s):
    groups = split_groups(s)
    abas = split_abas(groups)
    for aba in abas[0]:
        bab_wanted = aba[1] + aba[0] + aba[1]
        if bab_wanted in abas[1]:
            return True
    return False


def split_abas(xs):
    abas = []
    babs = []
    for s in xs:
        if s.startswith('['):
            babs.extend(find_abas(s[1:-1]))
        else:
            abas.extend(find_abas(s))
    return [abas, babs]


def find_abas(s):
    abas = []
    for i, c in enumerate(s[:-2]):
        if c == s[i + 2] and c != s[i + 1]:
            abas.append(s[i:i + 3])
    return abas


def split_groups(s):
    pos = 0
    groups = []
    while pos < len(s):
        end = 0
        if s[pos] == '[':
            end = pos + (s[pos:].index(']')) + 1
        else:
            idx = s[pos:].find('[')
            end = (pos + idx) if idx != -1 else len(s)
        groups.append(s[pos:end])
        pos = end
    return groups


def has_abba(s: str):
    for i, c in enumerate(s[:-3]):
        if c == s[i + 3] and c != s[i + 1] and s[i + 1] == s[i + 2]:
            return True
    return False


if __name__ == '__main__':
    main()
