import sexp
from schematic_file_format import *


class Schematic:

    def __init__(self):
        self.file_name = ""
        self.raw_string = ""

        self.version = ""
        self.generator = ""
        self.kicad_element = []

    def load(self, file_name: str):
        self.file_name = file_name
        with open(self.file_name, "r", encoding="UTF-8") as file:
            self.raw_string = file.read()
            s_expression_list = sexp.load(self.raw_string)

        for item in s_expression_list:
            value = sexp.get_symbol_value(item)
            if value == "version":
                self.version = sexp.get_symbol_data_by_token(item, "version")[0]
            try:
                new_class_instance = eval("{}()".format(class_dict[value].__name__))
                new_class_instance.from_s_expression(item)
                self.kicad_element.append(new_class_instance)
            except KeyError:
                pass

    def save(self, file_name: str = None):
        """
        Save schematic to file.

        :param file_name: File where save, if None the original file will be overwritten.
        """
        if file_name is None:
            file_name = self.file_name
        with open(file_name, "w", encoding="UTF-8") as file:
            file.write("(kicad_sch (version {}) (generator KiCAD2Python)\n\n".format(self.version))
            for item in self.kicad_element:
                file.write("  {}\n\n".format(item.to_s_expression()))
            file.write(")")


########################################################################################################################


if __name__ == "__main__":
    schematic = Schematic()
    schematic.load("..\\Tests\\KiCAD_6_Test.kicad_sch")
    # Do stuff...
    schematic.save("..\\Tests\\KiCAD_6_Test_PARSED.kicad_sch")
