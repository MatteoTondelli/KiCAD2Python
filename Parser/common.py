# https://dev-docs.kicad.org/en/file-formats/sexpr-intro/


import sexp


class KiCADElement:

    def __init__(self):
        pass

    def from_s_expression(self, s_expression: list):
        raise NotImplementedError

    def to_s_expression(self) -> str:
        raise NotImplementedError


class LibraryIdentifier(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        pass

    def from_s_expression(self, s_expression):
        raise NotImplementedError

    def to_s_expression(self):
        raise NotImplementedError


class PositionIdentifier(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.x = 0.0
        self.y = 0.0
        self.angle = None

    def from_s_expression(self, s_expression):
        property_values = sexp.get_symbol_data_by_token(s_expression, "at")
        if property_values is not None:
            self.x = property_values[0]
            self.y = property_values[1]
            if len(property_values) > 2:
                self.angle = property_values[2]

    def to_s_expression(self):
        if self.angle is None:
            return "(at {} {})".format(self.x, self.y)
        else:
            return "(at {} {} {})".format(self.x, self.y, self.angle)


class CoordinatePoint(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.x = 0.0
        self.y = 0.0

    def from_s_expression(self, s_expression):
        self.x = sexp.get_symbol_data_by_token(s_expression, "xy")[0]
        self.y = sexp.get_symbol_data_by_token(s_expression, "xy")[1]

    def to_s_expression(self):
        return "(xy {} {})".format(self.x, self.y)


class CoordinatePointList(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.coordinate_points = []

    def from_s_expression(self, s_expression):
        for item in sexp.get_symbol_data_by_token(s_expression, "pts"):
            new_coordinate_point = CoordinatePoint()
            new_coordinate_point.from_s_expression(item)
            self.coordinate_points.append(new_coordinate_point)

    def to_s_expression(self):
        base_string = "(pts"
        for coordinate_point in self.coordinate_points:
            base_string += " {}".format(coordinate_point.to_s_expression())
        base_string += ")"
        return base_string


class StrokeDefinition(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.width = ""
        self.type = ""
        self.color = ""

    def from_s_expression(self, s_expression):
        self.width = sexp.get_symbol_data_by_token(s_expression, "width")[0]
        self.type = sexp.get_symbol_data_by_token(s_expression, "type")[0].value()
        self.color = sexp.get_symbol_data_by_token(s_expression, "color")

    def to_s_expression(self):
        return "(stroke (width {}) (type {}) (color {}))".format(self.width, self.type,
                                                                 " ".join([str(x) for x in self.color]))


class TextEffects(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.size = None
        self.thickness = None
        self.is_bold = False
        self.is_italic = False
        self.justify = None
        self.is_hide = False

    def from_s_expression(self, s_expression):
        self.size = sexp.get_symbol_data_by_token(s_expression, "size")
        self.thickness = sexp.get_symbol_data_by_token(s_expression, "thickness")
        self.is_bold = sexp.get_symbol_data_by_token(s_expression, "bold") is not None
        self.is_italic = sexp.get_symbol_data_by_token(s_expression, "italic") is not None
        justify_attribute = sexp.get_symbol_data_by_token(s_expression, "justify")
        if justify_attribute is not None:
            self.justify = " ".join([sexp.get_symbol_value(item) for item in justify_attribute])
        self.is_hide = sexp.get_symbol_data_by_token(s_expression, "hide") is not None

    def to_s_expression(self):
        base_string = "(effects FONT JUSTIFY HIDE)"
        if self.size is not None:
            base_string = base_string.replace(" FONT", " (font (size {} {}))".format(self.size[0], self.size[1]))
        else:
            base_string = base_string.replace(" FONT", "")
        if self.justify is not None:
            base_string = base_string.replace(" JUSTIFY", " (justify {})".format(self.justify))
        else:
            base_string = base_string.replace(" JUSTIFY", "")
        if self.is_hide:
            base_string = base_string.replace(" HIDE", " hide")
        else:
            base_string = base_string.replace(" HIDE", "")
        if base_string == "(effects)":
            return ""
        else:
            return base_string


class PageSettings(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.paper_size = None
        self.is_portrait = False

    def from_s_expression(self, s_expression):
        processed_field_list = []
        for field in sexp.get_symbol_data_by_token(s_expression, "paper"):
            if type(field) == str:
                processed_field_list.append("\"{}\"".format(field))
            elif type(field) == float:
                processed_field_list.append(str(field))
        self.paper_size = " ".join(processed_field_list)
        self.is_portrait = sexp.get_symbol_data_by_token(s_expression, "portrait") is not None

    def to_s_expression(self):
        base_string = "(paper {} PORTRAIT)".format(self.paper_size)
        if self.is_portrait:
            base_string = base_string.replace(" PORTRAIT", " portrait")
        else:
            base_string = base_string.replace(" PORTRAIT", "")
        return base_string


class TitleBlock(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.title = ""
        self.date = ""
        self.revision = ""
        self.company = ""
        self.comments = []

    def from_s_expression(self, s_expression):
        self.title = sexp.get_symbol_data_by_token(s_expression, "title")
        self.date = sexp.get_symbol_data_by_token(s_expression, "date")
        self.revision = sexp.get_symbol_data_by_token(s_expression, "rev")
        self.company = sexp.get_symbol_data_by_token(s_expression, "company")

        for key in self.__dict__.keys():
            if self.__dict__[key] is not None:
                try:
                    self.__dict__[key] = self.__dict__[key][0]
                except IndexError:
                    pass
            else:
                self.__dict__[key] = ""

        for item in sexp.get_symbol_data_by_token(s_expression, "title_block"):
            value = sexp.get_symbol_value(item)
            if value == "comment":
                self.comments.append(sexp.get_symbol_data_by_token(item, "comment"))

    def to_s_expression(self):
        base_string = "(title_block\n TITLE DATE REVISION COMPANY_NAME COMMENTS)"
        if self.title != "":
            base_string = base_string.replace(" TITLE", "  (title \"{}\")\n".format(self.title))
        else:
            base_string = base_string.replace(" TITLE", "")
        if self.date != "":
            base_string = base_string.replace(" DATE", "  (date \"{}\")\n".format(self.date))
        else:
            base_string = base_string.replace(" DATE", "")
        if self.revision != "":
            base_string = base_string.replace(" REVISION", "  (rev \"{}\")\n".format(self.revision))
        else:
            base_string = base_string.replace(" REVISION", "")
        if self.company != "":
            base_string = base_string.replace(" COMPANY_NAME", "  (company \"{}\")\n".format(self.company))
        else:
            base_string = base_string.replace(" COMPANY_NAME", "")

        comments_string = ""
        for comment in self.comments:
            comments_string += "  (comment {} \"{}\")\n".format(comment[0], comment[1])
        base_string = base_string.replace(" COMMENTS", comments_string)

        return base_string


class Properties(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.key = ""
        self.value = ""

    def from_s_expression(self, s_expression):
        self.key = sexp.get_symbol_data_by_token(s_expression, "property")[0]
        self.value = sexp.get_symbol_data_by_token(s_expression, "property")[1].replace("\"", "\\\"")

    def to_s_expression(self):
        base_string = "(property \"{}\" \"{}\")".format(self.key, self.value)
        return base_string


class UniqueIdentifier(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.uuid = ""

    def from_s_expression(self, s_expression):
        self.uuid = sexp.get_symbol_data_by_token(s_expression, "uuid")[0].value()

    def to_s_expression(self):
        return "(uuid {})".format(self.uuid)


class_dict = {"uuid": UniqueIdentifier,
              "paper": PageSettings,
              "title_block": TitleBlock
              }
