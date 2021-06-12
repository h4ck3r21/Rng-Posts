from essential_generators import DocumentGenerator

gen = DocumentGenerator()


class Player:
    def __init__(self, name, ID):
        self.name = name
        self.id = ID
        self.cor_msg = ''
        self.message = ''
        self.para = self.make_paragraph()
        self.char = 0
        self.is_correct = True
        self.remaining_char = self.para
        self.score = 0
        self.ready = False
        self.victory = False

    def get_message(self, msg):
        self.message = msg

    def get_para(self, para):
        self.para = para

    def check(self):
        print('checking input')
        self.is_correct = self.para.startswith(self.message)
        if self.is_correct:
            self.cor_msg = self.message
            if self.message != '':
                self.remaining_char = self.para.split(self.message, 1)[1]
            else:
                self.remaining_char = self.para
            print(self.char)
            self.char = len(self.message)
        self.score = len(self.cor_msg)
        if self.score >= 5000:
            self.victory = True
        print(self.message == self.para)
        if self.remaining_char == '':
            self.increase_paragraph(self.para)

    @staticmethod
    def make_paragraph():
        print('makin paragraf')
        para = gen.paragraph()
        return sanitise_paragraph(para)

    def increase_paragraph(self, paragraph):
        print('adding more paragraph')
        self.para = ' '.join([paragraph, self.make_paragraph()])


def sanitise_paragraph(para: str) -> str:
    """Remove unwanted characters.

    Filter down to just ASCII characters
    """
    return ' '.join(para.encode().decode("ASCII", "ignore").split("\n"))
