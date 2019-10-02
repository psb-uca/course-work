# Tokenizer class python script
# CSCI 3370

import re


class JackTokenizer:

    jack_body = ""
    token = ''
    xml_file = ""
    xml_body = "<tokens>\n\t"

    symbols = ('{', '}', '(',  ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~')
    keywords = ("class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void"
                , "true", "false", "null", "this", "let", "do", "if", "else", "while", "return")

    def __init__(self, jack_file):
        self.jack_file = open(jack_file)
        self.jack_list = ()
        self.remove_comments()
        self.jack_file.close()

    def remove_comments(self):
        # Removing comments using regular expressions
        jack_body_original: str = self.jack_file.read()
        b1 = re.sub(r'(\/\*\*)([\s\S]+?)(\*\/)', '', jack_body_original)
        b2 = re.sub(r'(\/\/).*', '', b1)
        current_list = b2.split('\n')
        while '' in current_list:
            current_list.pop(current_list.index(''))
        self.jack_list = current_list
        self.jack_body = '\n'.join(self.jack_list)


    # def tokenize(self):

# TEST MAIN
def main():
    j1 = JackTokenizer("test.jack")
    print('\n'.join(j1.jack_list))


if __name__ == "__main__":
    main()
