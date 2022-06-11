import sexp
from common import KiCADElement
from common import PositionIdentifier, TextEffects, StrokeDefinition, CoordinatePointList


class FillDefinition(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.type = ""

    def from_s_expression(self, s_expression):
        self.type = sexp.get_symbol_data_by_token(s_expression, "type")[0].value()

    def to_s_expression(self):
        return "(fill (type {}))".format(self.type)


class Symbol(KiCADElement):
    """
    The symbol token defines a symbol or sub-unit of a parent symbol.
    There can be zero or more symbol tokens in a symbol library file.
    """
    def __init__(self):
        KiCADElement.__init__(self)
        self.library_identifier = ""
        self.unit_identifier = ""
        self.extends = None
        self.pin_numbers = None
        self.pin_names = None
        self.in_bom = None
        self.on_board = None
        self.properties = []
        self.graphic_items = []
        self.pins = []
        self.units = []

        self.sub_symbols = []

    def from_s_expression(self, s_expression):
        self.library_identifier = sexp.get_symbol_data_by_token(s_expression, "symbol")[0]

        for item in sexp.get_symbol_data_by_token(s_expression, "symbol"):
            if len(item) == 1:
                self.extends = sexp.get_symbol_value(item)

        try:
            self.in_bom = sexp.get_symbol_data_by_token(s_expression, "in_bom")[0]
            self.on_board = sexp.get_symbol_data_by_token(s_expression, "on_board")[0]
        except TypeError:
            # Sub-symbols does not have the above fields.
            pass

        self.pin_numbers = sexp.get_symbol_data_by_token(s_expression, "pin_numbers")
        self.pin_names = sexp.get_symbol_data_by_token(s_expression, "pin_names")

        prop_expression_list = [item for item in s_expression
                                if sexp.get_symbol_data_by_token(item, "property") is not None]
        for prop_expression in prop_expression_list:
            new_property = SymbolProperty()
            new_property.from_s_expression(prop_expression)
            self.properties.append(new_property)

        for item in s_expression:
            if isinstance(item, list):
                value = sexp.get_symbol_value(item)
                try:
                    new_class_instance = eval("{}()".format(symbol_graphic_items_dict[value].__name__))
                    new_class_instance.from_s_expression(item)
                    self.graphic_items.append(new_class_instance)
                except KeyError:
                    pass

        sub_symbol_expression_list = [item for item in s_expression
                                      if sexp.get_symbol_data_by_token(item, "symbol") is not None]
        for sub_symbol_expression in sub_symbol_expression_list:
            new_sub_symbol = Symbol()
            new_sub_symbol.from_s_expression(sub_symbol_expression)
            self.sub_symbols.append(new_sub_symbol)

        pin_expression_list = [item for item in s_expression
                               if sexp.get_symbol_data_by_token(item, "pin", recursive=False) is not None]
        for pin_expression in pin_expression_list:
            new_pin = SymbolPin()
            new_pin.from_s_expression(pin_expression)
            self.pins.append(new_pin)

    def to_s_expression(self):
        base_string = "(symbol \"{}\"".format(self.library_identifier)

        if self.extends is not None:
            base_string += " ({})".format(self.extends)

        if self.pin_numbers is not None:
            base_string += " (pin_numbers hide)"
        if self.pin_names is not None:
            base_string += " (pin_names"
            offset = sexp.get_symbol_data_by_token(self.pin_names, "offset")
            if len(offset) > 0:
                base_string += " (offset {})".format(offset[0])
            if sexp.get_symbol_data_by_token(self.pin_names, "hide") is not None:
                base_string += " hide"
            base_string += ")"

        if self.in_bom is not None:
            base_string += " (in_bom {})".format("yes" if self.in_bom else "no")
        if self.on_board is not None:
            base_string += " (on_board {})".format("yes" if self.on_board else "no")

        for prop in self.properties:
            base_string += "\n  {}".format(prop.to_s_expression())
        for graphic_item in self.graphic_items:
            base_string += "\n  {}".format(graphic_item.to_s_expression())
        for pin in self.pins:
            base_string += "\n  {}".format(pin.to_s_expression())
        for symbol in self.sub_symbols:
            base_string += "\n  {}".format(symbol.to_s_expression())

        base_string += "\n)"
        return base_string


class SymbolProperty(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.key = ""
        self.value = ""
        self.id = 0
        self.position_identifier = PositionIdentifier()
        self.text_effects = TextEffects()

    def from_s_expression(self, s_expression):
        self.key = sexp.get_symbol_data_by_token(s_expression, "property")[0]
        self.value = sexp.get_symbol_data_by_token(s_expression, "property")[1].replace("\"", "\\\"")
        self.id = sexp.get_symbol_data_by_token(s_expression, "id")[0]
        self.position_identifier.from_s_expression(s_expression)
        self.text_effects.from_s_expression(s_expression)

    def to_s_expression(self):
        text_effects_string = self.text_effects.to_s_expression()
        if text_effects_string != "":
            base_string = "(property \"{}\" \"{}\" (id {}) {}\n    {}\n  )"\
                .format(self.key, self.value, self.id, self.position_identifier.to_s_expression(), text_effects_string)
        else:
            base_string = "(property \"{}\" \"{}\" (id {}) {})" \
                .format(self.key, self.value, self.id, self.position_identifier.to_s_expression())
        return base_string


class SymbolArc(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.start = []
        self.mid = []
        self.end = []
        self.stroke_definition = StrokeDefinition()
        self.fill_definition = FillDefinition()

    def from_s_expression(self, s_expression):
        self.start = sexp.get_symbol_data_by_token(s_expression, "start")
        self.mid = sexp.get_symbol_data_by_token(s_expression, "mid")
        self.end = sexp.get_symbol_data_by_token(s_expression, "end")
        self.stroke_definition.from_s_expression(sexp.get_symbol_data_by_token(s_expression, "stroke"))
        self.fill_definition.from_s_expression(sexp.get_symbol_data_by_token(s_expression, "fill"))

    def to_s_expression(self):
        return "(arc (start {}) (mid {}) (end {})\n" \
               "  {}\n" \
               "  {}\n" \
               ")".format(" ".join(map(str, self.start)), " ".join(map(str, self.mid)), " ".join(map(str, self.end)),
                          self.stroke_definition.to_s_expression(), self.fill_definition.to_s_expression())


class SymbolCircle(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.center = []
        self.radius = []
        self.stroke_definition = StrokeDefinition()
        self.fill_definition = FillDefinition()

    def from_s_expression(self, s_expression):
        self.center = sexp.get_symbol_data_by_token(s_expression, "center")
        self.radius = sexp.get_symbol_data_by_token(s_expression, "radius")
        self.stroke_definition.from_s_expression(sexp.get_symbol_data_by_token(s_expression, "stroke"))
        self.fill_definition.from_s_expression(sexp.get_symbol_data_by_token(s_expression, "fill"))

    def to_s_expression(self):
        return "(circle (center {}) (radius {})\n" \
               "  {}\n" \
               "  {}\n" \
               ")".format(" ".join(map(str, self.center)), " ".join(map(str, self.radius)),
                          self.stroke_definition.to_s_expression(), self.fill_definition.to_s_expression())


class SymbolCurve(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.coordinate_point_list = CoordinatePointList()
        self.stroke_definition = StrokeDefinition()
        self.fill_definition = FillDefinition()

    def from_s_expression(self, s_expression):
        self.coordinate_point_list.from_s_expression(s_expression)
        self.stroke_definition.from_s_expression(sexp.get_symbol_data_by_token(s_expression, "stroke"))
        self.fill_definition.from_s_expression(sexp.get_symbol_data_by_token(s_expression, "fill"))

    def to_s_expression(self):
        return "(gr_curve\n" \
               "  {}\n" \
               "  {}\n" \
               "  {}\n" \
               ")".format(self.coordinate_point_list.to_s_expression(),
                          self.stroke_definition.to_s_expression(), self.fill_definition.to_s_expression())


class SymbolLine(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.coordinate_point_list = CoordinatePointList()
        self.stroke_definition = StrokeDefinition()
        self.fill_definition = FillDefinition()

    def from_s_expression(self, s_expression):
        self.coordinate_point_list.from_s_expression(s_expression)
        self.stroke_definition.from_s_expression(sexp.get_symbol_data_by_token(s_expression, "stroke"))
        self.fill_definition.from_s_expression(sexp.get_symbol_data_by_token(s_expression, "fill"))

    def to_s_expression(self):
        return "(polyline\n" \
               "  {}\n" \
               "  {}\n" \
               "  {}\n" \
               ")".format(self.coordinate_point_list.to_s_expression(),
                          self.stroke_definition.to_s_expression(), self.fill_definition.to_s_expression())


class SymbolRectangle(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.start = []
        self.end = []
        self.stroke_definition = StrokeDefinition()
        self.fill_definition = FillDefinition()

    def from_s_expression(self, s_expression):
        self.start = sexp.get_symbol_data_by_token(s_expression, "start")
        self.end = sexp.get_symbol_data_by_token(s_expression, "end")
        self.stroke_definition.from_s_expression(sexp.get_symbol_data_by_token(s_expression, "stroke"))
        self.fill_definition.from_s_expression(sexp.get_symbol_data_by_token(s_expression, "fill"))

    def to_s_expression(self):
        return "(rectangle (start {}) (end {})\n" \
               "  {}\n" \
               "  {}\n" \
               ")".format(" ".join(map(str, self.start)), " ".join(map(str, self.end)),
                          self.stroke_definition.to_s_expression(), self.fill_definition.to_s_expression())


class SymbolText(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.text = ""
        self.position_identifier = PositionIdentifier()
        self.text_effects = TextEffects()

    def from_s_expression(self, s_expression):
        self.text = sexp.get_symbol_data_by_token(s_expression, "text")[0]
        self.position_identifier.from_s_expression(s_expression)
        self.text_effects.from_s_expression(s_expression)

    def to_s_expression(self):
        return "(text \"{}\" {}\n" \
               "  {}\n" \
               ")".format(self.text, self.position_identifier.to_s_expression(), self.text_effects.to_s_expression())


class SymbolPin(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.pin_electrical_type = ""
        self.pin_graphic_style = ""
        self.position_identifier = PositionIdentifier()
        self.length = ""
        self.name = ["", TextEffects()]
        self.number = ["", TextEffects()]

        self.hide = None

    def from_s_expression(self, s_expression):
        self.pin_electrical_type = sexp.get_symbol_data(s_expression)
        self.pin_graphic_style = sexp.get_symbol_data(s_expression, 1)
        self.position_identifier.from_s_expression(s_expression)
        self.length = sexp.get_symbol_data_by_token(s_expression, "length")[0]
        name, text_effects = sexp.get_symbol_data_by_token(s_expression, "name")
        self.name[0] = name
        self.name[1].from_s_expression(text_effects)
        number, text_effects = sexp.get_symbol_data_by_token(s_expression, "number")
        self.number[0] = number
        self.number[1].from_s_expression(text_effects)

        self.hide = sexp.get_symbol_data_by_token(s_expression, "hide")

    def to_s_expression(self):
        base_string = "(pin {} {} {} (length {})".format(self.pin_electrical_type, self.pin_graphic_style,
                                                         self.position_identifier.to_s_expression(), self.length)
        if self.hide is not None:
            base_string += " hide"
        base_string += "\n  (name \"{}\" {})".format(self.name[0], self.name[1].to_s_expression())
        base_string += "\n  (number \"{}\" {})".format(self.number[0], self.number[1].to_s_expression())
        base_string += "\n)"
        return base_string


symbol_graphic_items_dict = {"arc": SymbolArc,
                             "circle": SymbolCircle,
                             "gr_curve": SymbolCurve,
                             "polyline": SymbolLine,
                             "rectangle": SymbolRectangle,
                             "text": SymbolText}
