import re


def match_quote(str_to_match):
    if re.search(r':"\w\'\w"', str_to_match, re.I):
        print('match successfully!')
    else:
        print('match failed!')


def array_constructor():
    raw = [1, 2, 3]
    print([x * 2 for x in raw])


def set_minuse():
    set1 = set([1, 2, 3])
    set2 = set([2, 3, 4])
    print(set1 - set2)
    print(set1 | set2)
    print(set1 & set2)


if __name__ == '__main__':
    print(':"哈哈\'s科技时尚男装"')
    match_quote(':"哈哈\'s科技时尚男装"')

    array_constructor()
    set_minuse()
