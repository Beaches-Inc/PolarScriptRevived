KEYWORDS = ["let","and","or","if","return","def","class","import","elif","else","for","while","in","not","false","true","var","in","null","continue","break","pass"]

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        if self.value: return f'[{self.type}:{self.value}]'
        return f'[{self.type}]'

    def __repr__(self):
        return self.__str__()

class Namespace:
    def __init__(self,vars: dict,funcs:dict) -> None:
        self.vars = vars
        self.funcs = funcs

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def tokenize(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
            elif self.current_char == '+':
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token('ADD_ASSIGN'))
                    self.advance()
                else:
                    tokens.append(Token('PLUS'))
            elif self.current_char == '-':
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token('SUB_ASSIGN'))
                    self.advance()
                else:
                    tokens.append(Token('MINUS'))
            elif self.current_char == '*':
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token('MUL_ASSIGN'))
                    self.advance()
                else:
                    tokens.append(Token('MUL'))
            elif self.current_char == '/':
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token('DIV_ASSIGN'))
                    self.advance()
                else:
                    tokens.append(Token('DIV'))
            elif self.current_char == '%':
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token('MOD_ASSIGN'))
                    self.advance()
                else:
                    tokens.append(Token('MOD'))
            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token('EQUAL'))
                    self.advance()
                else:
                    tokens.append(Token('ASSIGN'))
            elif self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token('NOT_EQUAL'))
                    self.advance()
                else:
                    tokens.append(Token('NOT'))
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token('GREATER_EQUAL'))
                    self.advance()
                else:
                    tokens.append(Token('GREATER'))
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token('LESS_EQUAL'))
                    self.advance()
                else:
                    tokens.append(Token('LESS'))
            elif self.current_char == '&':
                self.advance()
                if self.current_char == '&':
                    tokens.append(Token('AND'))
                    self.advance()
                else:
                    tokens.append(Token('BITWISE_AND'))
            elif self.current_char == '|':
                self.advance()
                if self.current_char == '|':
                    tokens.append(Token('OR'))
                    self.advance()
                else:
                    tokens.append(Token('BITWISE_OR'))
            elif self.current_char == '^':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token('XOR_ASSIGN'))
                    self.advance()
                else:
                    tokens.append(Token('XOR'))
            elif self.current_char == '~':
                self.advance()
                tokens.append(Token('BITWISE_NOT'))
            elif self.current_char == '(':
                self.advance()
                tokens.append(Token('LPAREN'))
            elif self.current_char == ')':
                self.advance()
                tokens.append(Token('RPAREN'))
            elif self.current_char == '[':
                self.advance()
                tokens.append(Token('LBRACKET'))
            elif self.current_char == ']':
                self.advance()
                tokens.append(Token('RBRACKET'))
            elif self.current_char == '{':
                self.advance()
                tokens.append(Token('LBRACE'))
            elif self.current_char == '}':
                self.advance()
                tokens.append(Token('RBRACE'))
            elif self.current_char == ';':
                tokens.append(Token('SEMI'))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token('LBRACE'))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token('RBRACE'))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token('COMMA'))
                self.advance()
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == "'":
                tokens.append(self.make_string())
            elif self.current_char == '#':
                tokens.append(self.make_comment())
            elif self.current_char.isalpha():
                tokens.append(self.make_identifier())
            else:
                self.error()

        return tokens
    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char is not None and self.current_char.isdigit() or self.current_char == '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token('INTEGER', int(num_str))
        else:
            return Token('FLOAT', float(num_str))
    def make_string(self):
        quote = self.current_char
        string = ''
        self.advance()
        while self.current_char is not None and self.current_char != quote:
            string += self.current_char
            self.advance()
        self.advance()
        return Token('STRING',string)
    def make_comment(self):
        comment = ''
        self.advance()
        while self.current_char is not None and self.current_char != '':
            comment += self.current_char
            self.advance()
        self.advance()
        return Token('COMMENT',comment)
    def make_identifier(self):
        id_str = ''
        while self.current_char is not None and self.current_char.isalnum():
            id_str += self.current_char
            self.advance()
        if id_str in KEYWORDS:
            return Token(id_str)
        return Token('ID', id_str)

class Interpreter:
    def __init__(self) -> None:
        self.namespace = Namespace({},{})
    def runLine(self, code: str) -> None:
        tokens = Lexer(code).tokenize()
        print(tokens)
