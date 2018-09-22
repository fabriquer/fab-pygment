from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import *

__all__ = [ 'FabLexer' ]

def keywords(*strings):
    return words(strings, prefix=r'\b', suffix=r'\b')

class FabLexer(RegexLexer):
    name = 'Fabrique'
    aliases = [ 'fab', 'fabrique' ]
    filenames = [ '*.fab', 'fabfile' ]

    tokens = {
        'root': [
            # Comments (single-line only) and whitespace:
            (r'#', Comment.Single, 'comment'),
            (r'[\s+]', Whitespace),

            # Literals: boolean, integer and string
            ("'", Literal.String.Single, 'singlestring'),
            ('"', Literal.String.Double, 'doublestring'),

            (r'\b[0-9]+\b', Literal.Number.Integer),
            (keywords('true', 'false'), Keyword.Constant),

            # Builtin functions, types and constants:
            (keywords('action', 'file', 'files', 'import'), Name.Builtin),
            (keywords('bool', 'file', 'int', 'list', 'record', 'string'),
                Keyword.Type),
            (keywords('in', 'out'), Keyword.Pseudo),
            (keywords('buildroot', 'srcroot'), Keyword.Constant),

            # Other keywords:
            (keywords('if', 'else', 'foreach', 'function'), Keyword),

            # Operators and punctuation:
            (r'[\+\.]', Operator),
            (r'[!=]=', Operator),
            (r'=', Keyword.Declaration),
            (keywords('and', 'or', 'xor'), Operator.Word),
            (r'[,(){}\[\]:;<\->]', Punctuation),

            # Other identifiers:
            (r'([_a-zA-Z]\w*)', bygroups(Name.Variable)),
        ],

        # We recognize lit directives within comments:
        'comment': [
            (r'\n', Comment.Single, '#pop'),
            (keywords('RUN', 'CHECK', 'CHECK-DAG', 'CHECK-NEXT', 'CHECK-NOT'),
                Comment.Special),
            (r"[^\n]", Comment.Single),
        ],

        # Within single-quoted strings, a single quote ends the string
        'singlestring': [
            ("'", Literal.String.Single, '#pop'),
            (r'\${', Literal.String.Delimiter, 'stringvar'),
            (r"[^']", Literal.String.Single),
        ],

        # Within double-quoted strings, a double quote ends the string
        'doublestring': [
            ('"', Literal.String.Double, '#pop'),
            (r'\${', Literal.String.Delimiter, 'stringvar'),
            (r'[^"]', Literal.String.Double),
        ],

        'stringvar': [
            ('}', Literal.String.Interpol, '#pop'),
            (r'[^}]', Literal.String.Interpol),
        ],
    }
