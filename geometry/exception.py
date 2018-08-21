from textwrap import fill, dedent


def filldedent(s, w=70):

    return '\n' + fill(dedent(str(s)).strip('\n'), width=w)