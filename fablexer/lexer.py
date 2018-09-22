from pygments.lexer import RegexLexer, bygroups
from pygments.token import *

__all__ = [ 'FabLexer' ]

class FabLexer(RegexLexer):
    name = 'Fabrique'
    aliases = [ 'fab', 'fabrique' ]
    filenames = [ '*.fab', 'fabfile' ]

    tokens = {
        'root': [
            (r'#.*\n', Comment.Single),

            (r"'", String, 'singlestring'),
            (r'"', String, 'doublestring'),

            (r'(.*?)(\s*)(=)(\s*)(function)',
                bygroups(Name.Function, Whitespace, Operator,
                         Whitespace, Name.Builtin)),

            (r'action', Name.Builtin),
            (r'buildroot', Name.Builtin),
            (r'files', Name.Builtin),
            (r'function', Name.Builtin),
            (r'srcroot', Name.Builtin),

            (r'bool', Keyword.Type),
            (r'file', Keyword.Type),
            (r'int', Keyword.Type),
            (r'list', Keyword.Type),
            (r'record', Keyword.Type),
            (r'string', Keyword.Type),

            (r'in', Keyword.Pseudo),
            (r'out', Keyword.Pseudo),

            (r'if', Keyword),
            (r'else', Keyword),
            (r'foreach', Keyword),
            (r'as', Keyword),

            (r'([_a-zA-Z]\w*)(\s*)(=)',
                bygroups(Name.Constant, Whitespace, Operator)),

            (r'([_a-zA-Z]\w*)(\s*)(:)(\s*)(\w*)(\s*)(=)',
                bygroups(Name.Constant,
                    Whitespace,
                    Punctuation,
                    Whitespace,
                    Keyword.Type,
                    Whitespace,
                    Operator)),

            (r'([_a-zA-Z]\w*)',
                bygroups(Name.Variable)),

            (r'([_a-zA-Z]\w*)(\s*)(:)(\s*)(\w*)',
                bygroups(Name.Constant,
                    Whitespace,
                    Punctuation,
                    Whitespace,
                    Keyword.Type)),

            (r'\+', Operator),
            (r'\.\+', Operator),
            (r'<-', Operator),
            (r'=>', Operator),
            (r'[=:]', Operator),
            (r'and', Operator.Word),
            (r'or', Operator.Word),
            (r'xor', Operator.Word),

            (r'[\.,(){}\[\];]', Punctuation),

            (r'[\s+]', Whitespace),
        ],

        'singlestring': [
            (r"'", String, '#pop'),
            (r"[^']", String),
        ],

        'doublestring': [
            (r'"', String, '#pop'),
            (r'[^"]', String),
        ],
    }
