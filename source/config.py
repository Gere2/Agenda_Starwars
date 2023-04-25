class Agenda:
    def __init__(self):
        self.jedi = []
        self.sith = []

    def add_character(self, side, character):
        if side == "jedi":
            if len(self.jedi) < 50:
                self.jedi.append(character)
            else:
                print("No se pueden agregar más Jedi a la agenda.")
        elif side == "sith":
            if len(self.sith) < 50:
                self.sith.append(character)
            else:
                print("No se pueden agregar más Sith a la agenda.")

    def modify_character(self, side, index, character):
        if side == "jedi":
            if 0 <= index < len(self.jedi):
                self.jedi[index] = character
            else:
                print("Índice de Jedi no válido.")
        elif side == "sith":
            if 0 <= index < len(self.sith):
                self.sith[index] = character
            else:
                print("Índice de Sith no válido.")

    def get_character(self, side, index):
        if side == "jedi":
            if 0 <= index < len(self.jedi):
                return self.jedi[index]
            else:
                print("Índice de Jedi no válido.")
        elif side == "sith":
            if 0 <= index < len(self.sith):
                return self.sith[index]
            else:
                print("Índice de Sith no válido.")

    def remove_character(self, side, index):
        if side == "jedi":
            if 0 <= index < len(self.jedi):
                self.jedi.pop(index)
            else:
                print("Índice de Jedi no válido.")
        elif side == "sith":
            if 0 <= index < len(self.sith):
                self.sith.pop(index)
            else:
                print("Índice de Sith no válido.")

    def search_by_name(self, name):
        results = []
        for jedi in self.jedi:
            if jedi.name.lower() == name.lower():
                results.append(("jedi", jedi))
        for sith in self.sith:
            if sith.name.lower() == name.lower():
                results.append(("sith", sith))
        return results

    def search_by_rank(self, rank):
        results = []
        for jedi in self.jedi:
            if jedi.rank.lower() == rank.lower():
                results.append(("jedi", jedi))
        for sith in self.sith:
            if sith.rank.lower() == rank.lower():
                results.append(("sith", sith))
        return results

    def search_by_power_level(self, power_level):
        results = []
        for jedi in self.jedi:
            if jedi.power_level == power_level:
                results.append(("jedi", jedi))
        for sith in self.sith:
            if sith.power_level == power_level:
                results.append(("sith", sith))
        return results

    def show_all(self):
        return [("jedi", jedi) for jedi in self.jedi] + [("sith", sith) for sith in self.sith]

    def character_exists(self, name):
        for jedi in self.jedi:
            if jedi.name.lower() == name.lower():
                return True
        for sith in self.sith:
            if sith.name.lower() == name.lower():
                return True
        return False

    def add_character(self, side, character):
        if self.character_exists(character.name):
            print("Ya existe un personaje con ese nombre en la agenda.")
            return