import json
from pathlib import Path

class savestates:
    def __init__(self):
        self.pos = 0
        self.last_opened_f = ""

class cursor:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.selected = [] # 0th element should be start 1st should be end
    def renew_text(self, text):
        self.text = text
        if self.pos > len(text) - 1:
            self.pos = len(text) - 1
    def update_pos(self, n):
        if self.pos + n >= 0: self.pos += n
        else: self.pos = 0
    def peek(self, n): return self.text[self.pos + n]
    def insert(self, text):
        self.text = self.text[:self.pos] + text + self.text[self.pos:]
        self.update_pos(len(text))
    def delete_part(self, start, end):
        self.text = self.text[:start] + self.text[:end]
        self.update_pos(start)
    def delete(self):
        self.delete_part(self.pos-1, self.pos)
    def select_part(self, start, end):
        self.selected = [start,end]
    def select(self, start):
        self.select_part(start, self.pos)


def file_exist(fname):
    return True if Path(fname).is_file() else False

def load_savestates():
    if not file_exist("savestate.json"):
        with open("savestate.json", "w", encoding="utf-8") as file:
            file.write("{}")
            return savestates()
    with open("savestate.json", "r", encoding="utf-8") as file:
        save = json.loads(file.read())
        ss = savestates()
        ss.pos = save.get("pos", 0)
        ss.last_opened_f = save.get("last_opened_f", "")
        return ss
def save_savestates(savestate: savestates):
    with open("savestate.json", "w", encoding="utf-8") as file:
        save = json.dumps(savestate.__dict__)
        file.write(save)

if __name__ == "__main__":
    Savestates = load_savestates()

    file_sel = input(": ")
    if file_sel == "LAST": file_sel = Savestates.last_opened_f

    with open(file_sel, "r+", encoding="utf-8") as file:
        running = True
        Cursor = cursor(file.read(), Savestates.pos)

        """
        while running:
            # main loop?
            pass
        """

        Cursor.update_pos(20)
        Cursor.insert("#")

        Savestates.pos = Cursor.pos
        Savestates.last_opened_f = file_sel
        save_savestates(Savestates)

        file.write(Cursor.text)