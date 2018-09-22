#
# Copyright 2014, 2018  Jonathan Anderson <jonathan.anderson@mun.ca>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
#

from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import *

__all__ = ['FabLexer']


def keywords(*strings):
    return words(strings, prefix=r'\b', suffix=r'\b')


class FabLexer(RegexLexer):
    name = 'Fabrique'
    aliases = ['fab', 'fabrique']
    filenames = ['*.fab', 'fabfile']

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
