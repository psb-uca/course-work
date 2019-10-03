# Tokenizer class python script
# CSCI 3370
# Preston Bennett

import re
from typing import List


class JackTokenizer:

    jack_body = ""
    xml_body = "<tokens>\n"

    # private data structures
    symbols = ('{', '}', '(',  ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '|', '=', '~')
    html_symbols = ('<', '>', '&', '"')
    keywords = ("class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void"
                , "true", "false", "null", "this", "let", "do", "if", "else", "while", "return")

    def __init__(self, jack_file, xml_name):
        self.jack_file = open(jack_file)
        self.jack_list: List[str] = ()
        self.xml_name = xml_name
        self.remove_comments()
        self.jack_file.close()

    def remove_comments(self):
        # Removing comments using regular expressions
        jack_body_original: str = self.jack_file.read()
        b1 = re.sub(r'(\/\*\*)([\s\S]+?)(\*\/)', '', jack_body_original)  # remove // comments
        b2 = re.sub(r'(\/\/).*', '', b1)  # remove comments until closing
        b3 = re.sub(r'(\/\*).*(\*\/)', '', b2)  # remove API documentation style comments
        b4 = re.sub(r'[\t]+', '', b3)
        current_list = b4.split('\n')
        while '' in current_list:
            current_list.pop(current_list.index(''))  # Remove whitespace in list
        self.jack_list = current_list
        self.jack_body = '\n'.join(self.jack_list)

    def tokenize(self):
        pattern = re.compile(r"\w+|[^ ]")  # pattern for splitting all lines into tokens
        for line in self.jack_list:
            tokens: List[str] = pattern.findall(line)
            prev = "not_stringConstant"
            text: str
            for token in tokens:

                # control flow for when processing stringConstants
                if prev == 'is_stringConstant':
                    text = "<stringConstant> " + token
                    prev = "next"
                    continue
                elif prev == "next":
                    if token != '"':
                        text += " " + token
                        continue
                    else:
                        text += " </stringConstant\n"
                        self.xml_body += text
                        prev = 'not_stringConstant'
                        continue
                else:
                    self.xml_body += "\t"

                # control flow for everything else
                if token in self.symbols:
                    text = "<symbol> " + token + " </symbol>\n"
                    self.xml_body += text
                    continue

                elif token in self.html_symbols:
                    if token == '<':
                        text = "<symbol> &lt; </symbol>\n"
                        self.xml_body += text
                        continue
                    elif token == '>':
                        text = "<symbol> &gt; </symbol>\n"
                        self.xml_body += text
                        continue
                    elif token == '"':
                        prev = 'is_stringConstant'  # activates first control flow structure for stringConstants
                        continue
                    elif token == '&':
                        text = "<symbol> &amp; </symbol>\n"
                        self.xml_body += text
                        continue
                elif token.isnumeric():
                    text = "<integerConstant> " + token + " </integerConstant>\n"
                    self.xml_body += text
                    continue
                elif token in self.keywords:
                    text = "<keyword> " + token + " </keyword>\n"
                    self.xml_body += text
                    continue
                else:
                    text = "<identifier> " + token + " </identifier>\n"
                    self.xml_body += text
                    continue

        self.xml_body += "</tokens>"
        print(self.xml_body) # For debugging purposes
        xml_file = open(self.xml_name, "w")
        xml_file.write(self.xml_body)
        xml_file.close()


def main():
    jt1 = JackTokenizer("Main.jack", "MainT.xml")
    jt2 = JackTokenizer("Square.jack", "SquareT.xml")
    jt3 = JackTokenizer("SquareGame.jack", "SquareGameT.xml")
    jt1.tokenize()
    jt2.tokenize()
    jt3.tokenize()


if __name__ == "__main__":
    main()
