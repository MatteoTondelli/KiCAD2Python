# https://dev-docs.kicad.org/en/file-formats/sexpr-schematic/


import sexp
from common import KiCADElement
from common import PositionIdentifier, UniqueIdentifier, StrokeDefinition, CoordinatePointList, TextEffects
from schematic_and_symbol_library import Symbol, SymbolProperty, FillDefinition


class Header(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.version = ""
        self.generator = ""

    def from_s_expression(self, s_expression):
        self.version = sexp.get_symbol_data_by_token(s_expression, "version")[0].value()
        self.generator = sexp.get_symbol_data_by_token(s_expression, "generator")[0].value()

    def to_s_expression(self):
        return "(kicad_sch ({}) ({})\n\n)".format(self.version, self.generator)


class LibrarySymbols(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.symbol_list = []

    def from_s_expression(self, s_expression):
        for item in s_expression:
            if isinstance(item, list):
                new_symbol = Symbol()
                new_symbol.from_s_expression(item)
                self.symbol_list.append(new_symbol)

    def to_s_expression(self):
        base_string = "(lib_symbols"
        for item in self.symbol_list:
            base_string += "\n  {}".format(item.to_s_expression())
        base_string += "\n)"
        return base_string


class Junction(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.position_identifier = PositionIdentifier()
        self.diameter = ""
        self.color = ""
        self.unique_identifier = UniqueIdentifier()

    def from_s_expression(self, s_expression):
        self.position_identifier.from_s_expression(s_expression)
        self.diameter = sexp.get_symbol_data_by_token(s_expression, "diameter")[0]
        self.color = sexp.get_symbol_data_by_token(s_expression, "color")
        self.unique_identifier.from_s_expression(s_expression)

    def to_s_expression(self):
        return "(junction {} (diameter {}) (color {})\n  {}\n)".format(self.position_identifier.to_s_expression(),
                                                                       self.diameter,
                                                                       " ".join([str(x) for x in self.color]),
                                                                       self.unique_identifier.to_s_expression())


class NoConnect(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.position_identifier = PositionIdentifier()
        self.unique_identifier = UniqueIdentifier()

    def from_s_expression(self, s_expression):
        self.position_identifier.from_s_expression(s_expression)
        self.unique_identifier.from_s_expression(s_expression)

    def to_s_expression(self):
        return "(no_connect {} {})".format(self.position_identifier.to_s_expression(),
                                           self.unique_identifier.to_s_expression())


class BusEntry(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.position_identifier = PositionIdentifier()
        self.size = None
        self.stroke_definition = StrokeDefinition()
        self.unique_identifier = UniqueIdentifier()

    def from_s_expression(self, s_expression):
        self.position_identifier.from_s_expression(s_expression)
        self.size = sexp.get_symbol_data_by_token(s_expression, "size")
        self.stroke_definition.from_s_expression(s_expression)
        self.unique_identifier.from_s_expression(s_expression)

    def to_s_expression(self):
        base_string = "(bus_entry {} (size {})" \
                      "\n  {}" \
                      "\n  {}" \
                      "\n)".format(self.position_identifier.to_s_expression(), " ".join(map(str, self.size)),
                                   self.stroke_definition.to_s_expression(), self.unique_identifier.to_s_expression())
        return base_string


class Wire(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.coordinate_point_list = CoordinatePointList()
        self.stroke_definition = StrokeDefinition()
        self.unique_identifier = UniqueIdentifier()

    def from_s_expression(self, s_expression):
        self.coordinate_point_list.from_s_expression(s_expression)
        self.stroke_definition.from_s_expression(s_expression)
        self.unique_identifier.from_s_expression(s_expression)

    def to_s_expression(self):
        base_string = "(wire {}" \
                      "\n  {}" \
                      "\n  {}" \
                      "\n)".format(self.coordinate_point_list.to_s_expression(),
                                   self.stroke_definition.to_s_expression(), self.unique_identifier.to_s_expression())
        return base_string


class Bus(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.coordinate_point_list = CoordinatePointList()
        self.stroke_definition = StrokeDefinition()
        self.unique_identifier = UniqueIdentifier()

    def from_s_expression(self, s_expression):
        self.coordinate_point_list.from_s_expression(s_expression)
        self.stroke_definition.from_s_expression(s_expression)
        self.unique_identifier.from_s_expression(s_expression)

    def to_s_expression(self):
        base_string = "(bus {}" \
                      "\n  {}" \
                      "\n  {}" \
                      "\n)".format(self.coordinate_point_list.to_s_expression(),
                                   self.stroke_definition.to_s_expression(), self.unique_identifier.to_s_expression())
        return base_string


class Image(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.position_identifier = PositionIdentifier()
        self.scale = None
        self.uuid = UniqueIdentifier()
        self.data = None

    def from_s_expression(self, s_expression):
        self.position_identifier.from_s_expression(s_expression)
        # ...
        self.uuid.from_s_expression(s_expression)
        raise NotImplementedError

    def to_s_expression(self):
        raise NotImplementedError


class GraphicalLine(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.coordinate_point_list = CoordinatePointList()
        self.stroke_definition = StrokeDefinition()
        self.unique_identifier = UniqueIdentifier()

    def from_s_expression(self, s_expression):
        self.coordinate_point_list.from_s_expression(s_expression)
        self.stroke_definition.from_s_expression(s_expression)
        self.unique_identifier.from_s_expression(s_expression)

    def to_s_expression(self):
        return "(polyline {}\n  {}\n  {}\n)".format(self.coordinate_point_list.to_s_expression(),
                                                    self.stroke_definition.to_s_expression(),
                                                    self.unique_identifier.to_s_expression())


class GraphicalText(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.text = ""
        self.position_identifier = PositionIdentifier()
        self.text_effects = TextEffects()
        self.unique_identifier = UniqueIdentifier()

    def from_s_expression(self, s_expression):
        self.text = sexp.get_symbol_data_by_token(s_expression, "text")[0]
        self.position_identifier.from_s_expression(s_expression)
        self.text_effects.from_s_expression(s_expression)
        self.unique_identifier.from_s_expression(s_expression)

    def to_s_expression(self):
        return "(text \"{}\" {}\n  {}\n  {}\n)".format(repr(self.text).strip("'"),
                                                       self.position_identifier.to_s_expression(),
                                                       self.text_effects.to_s_expression(),
                                                       self.unique_identifier.to_s_expression())


class LocalLabel(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.text = ""
        self.position_identifier = PositionIdentifier()
        self.text_effects = TextEffects()
        self.unique_identifier = UniqueIdentifier()

    def from_s_expression(self, s_expression):
        self.text = sexp.get_symbol_data_by_token(s_expression, "label")[0]
        self.position_identifier.from_s_expression(s_expression)
        self.text_effects.from_s_expression(s_expression)
        self.unique_identifier.from_s_expression(s_expression)

    def to_s_expression(self):
        return "(label \"{}\" {}\n  {}\n  {}\n)".format(repr(self.text).strip("'"),
                                                        self.position_identifier.to_s_expression(),
                                                        self.text_effects.to_s_expression(),
                                                        self.unique_identifier.to_s_expression())


class GlobalLabel(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.text = ""
        self.shape = None
        self.fields_autoplaced = ""
        self.position_identifier = PositionIdentifier()
        self.text_effects = TextEffects()
        self.unique_identifier = UniqueIdentifier()
        self.properties = []

    def from_s_expression(self, s_expression):
        self.text = sexp.get_symbol_data(s_expression)
        self.position_identifier.from_s_expression(s_expression)
        self.text_effects.from_s_expression(sexp.get_symbol_data_by_token(s_expression, "effects"))
        self.unique_identifier.from_s_expression(s_expression)
        for item in s_expression[2:]:
            value = sexp.get_symbol_value(item)
            if value == "property":
                new_property = SymbolProperty()
                new_property.from_s_expression(item)
                self.properties.append(new_property)
            elif value == "shape":
                self.shape = sexp.get_symbol_data(item)
            elif value == "fields_autoplaced":
                self.fields_autoplaced = sexp.get_symbol_value(item)

    def to_s_expression(self):
        base_string = "(global_label \"{}\" (shape {}) {} (FIELDS_AUTOPLACED)\n  {}\n  {}\n  PROPERTIES\n)"\
            .format(repr(self.text).strip("'"), self.shape, self.position_identifier.to_s_expression(),
                    self.text_effects.to_s_expression(), self.unique_identifier.to_s_expression())
        if self.fields_autoplaced != "":
            base_string = base_string.replace("FIELDS_AUTOPLACED", self.fields_autoplaced)
        else:
            base_string = base_string.replace(" (FIELDS_AUTOPLACED)", "")

        properties_string = ""
        for item in self.properties:
            properties_string += item.to_s_expression()
            if item is not self.properties[-1]:
                properties_string += "\n  "
        base_string = base_string.replace("PROPERTIES", properties_string)

        return base_string


class HierarchicalLabel(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.text = ""
        self.shape = None
        self.position_identifier = PositionIdentifier()
        self.text_effects = TextEffects()
        self.unique_identifier = UniqueIdentifier()

    def from_s_expression(self, s_expression):
        # ...
        self.position_identifier.from_s_expression(s_expression)
        self.text_effects.from_s_expression(s_expression)
        self.unique_identifier.from_s_expression(s_expression)
        raise NotImplementedError

    def to_s_expression(self):
        raise NotImplementedError


class Pin(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.number = ""
        self.unique_identifier = UniqueIdentifier()

    def from_s_expression(self, s_expression):
        raise NotImplementedError

    def to_s_expression(self):
        return "(pin \"{}\" {})".format(self.number, self.unique_identifier.to_s_expression())


class SymbolSchematic(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.library_identifier = ""
        self.position_identifier = PositionIdentifier()
        self.mirror = None
        self.unit = 0
        self.in_bom = False
        self.on_board = False
        self.fields_autoplaced = None
        self.unique_identifier = UniqueIdentifier()
        self.properties = []
        self.pins = []

    def from_s_expression(self, s_expression):
        self.library_identifier = sexp.get_symbol_data_by_token(s_expression, "lib_id")[0]
        self.position_identifier.from_s_expression(s_expression)
        self.unit = sexp.get_symbol_data_by_token(s_expression, "unit")[0]
        self.in_bom = sexp.get_symbol_data_by_token(s_expression, "in_bom")[0]
        self.on_board = sexp.get_symbol_data_by_token(s_expression, "on_board")[0]
        self.unique_identifier.from_s_expression(s_expression)

        for item in s_expression:
            value = sexp.get_symbol_value(item)
            if value == "fields_autoplaced":
                self.fields_autoplaced = sexp.get_symbol_value(item)
            elif value == "mirror":
                self.mirror = sexp.get_symbol_data_by_token(item, "mirror")[0].value()
            elif value == "property":
                new_property = SymbolProperty()
                new_property.from_s_expression(item)
                self.properties.append(new_property)
            elif value == "pin":
                new_pin = Pin()
                new_pin.number = sexp.get_symbol_data(item)
                new_pin.unique_identifier.from_s_expression(item)
                self.pins.append(new_pin)

    def to_s_expression(self):
        base_string = "(symbol (lib_id \"{}\") {} MIRROR (unit {})\n" \
                      "  (in_bom {}) (on_board {}) {}\n" \
                      "  {}\n" \
                      "  PROPERTIES\n" \
                      "  PINS\n" \
                      ")"\
            .format(self.library_identifier, self.position_identifier.to_s_expression(), self.unit,
                    "yes" if self.in_bom else "no", "yes" if self.on_board else "no",
                    "(fields_autoplaced)" if self.fields_autoplaced is not None else "",
                    self.unique_identifier.to_s_expression())

        if self.mirror is not None:
            base_string = base_string.replace("MIRROR ", "(mirror {}) ".format(self.mirror))
        else:
            base_string = base_string.replace("MIRROR ", "")

        properties_string = ""
        for item in self.properties:
            properties_string += item.to_s_expression()
            if item is not self.properties[-1]:
                properties_string += "\n  "
        base_string = base_string.replace("PROPERTIES", properties_string)

        pins_string = ""
        for item in self.pins:
            pins_string += item.to_s_expression()
            if item is not self.pins[-1]:
                pins_string += "\n  "
        base_string = base_string.replace("PINS", pins_string)

        return base_string


class HierarchicalSheet(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.position_identifier = PositionIdentifier()
        self.size = None
        self.stroke_definition = StrokeDefinition()
        self.fill_definition = FillDefinition()
        self.unique_identifier = UniqueIdentifier()
        self.sheet_name_property = None
        self.file_name_property = None
        self.hierarchical_pins = None

    def from_s_expression(self, s_expression):
        raise NotImplementedError

    def to_s_expression(self):
        raise NotImplementedError


class HierarchicalSheetPin(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.name = ""
        self.type = ""
        self.position_identifier = PositionIdentifier()
        self.text_effects = TextEffects()
        self.unique_identifier = UniqueIdentifier()

    def from_s_expression(self, s_expression):
        raise NotImplementedError

    def to_s_expression(self):
        raise NotImplementedError


class HierarchicalSheetInstance(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.instance_path = None
        self.page = None

    def from_s_expression(self, s_expression):
        self.instance_path = sexp.get_symbol_data_by_token(s_expression, "path")[0]
        self.page = sexp.get_symbol_data_by_token(s_expression, "page")[0]

    def to_s_expression(self):
        base_string = "(path \"{}\"(page \"{}\"))".format(self.instance_path, self.page)
        return base_string


class HierarchicalSheetInstances(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.sheet_instances = []

    def from_s_expression(self, s_expression):
        for item in s_expression:
            if isinstance(item, list):
                new_path = HierarchicalSheetInstance()
                new_path.from_s_expression(item)
                self.sheet_instances.append(new_path)

    def to_s_expression(self):
        base_string = "(sheet_instances"
        for item in self.sheet_instances:
            base_string += "\n  {}".format(item.to_s_expression())
        base_string += "\n)"
        return base_string


class SymbolInstance(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.instance_path = None
        self.reference = None
        self.unit = None
        self.value = None
        self.footprint = None

    def from_s_expression(self, s_expression):
        self.instance_path = sexp.get_symbol_data_by_token(s_expression, "path")[0]
        self.reference = sexp.get_symbol_data_by_token(s_expression, "reference")[0]
        self.unit = sexp.get_symbol_data_by_token(s_expression, "unit")[0]
        self.value = sexp.get_symbol_data_by_token(s_expression, "value")[0]
        self.footprint = sexp.get_symbol_data_by_token(s_expression, "footprint")[0]

    def to_s_expression(self):
        base_string = "(path \"{}\"" \
                      "\n  (reference \"{}\") (unit {}) (value \"{}\") (footprint \"{}\")" \
                      "\n)".format(self.instance_path, self.reference, self.unit, self.value, self.footprint)
        return base_string


class SymbolInstances(KiCADElement):
    def __init__(self):
        KiCADElement.__init__(self)
        self.path_list = []

    def from_s_expression(self, s_expression):
        for item in s_expression:
            if isinstance(item, list):
                new_path = SymbolInstance()
                new_path.from_s_expression(item)
                self.path_list.append(new_path)

    def to_s_expression(self):
        base_string = "(symbol_instances"
        for item in self.path_list:
            base_string += "\n  {}".format(item.to_s_expression())
        base_string += "\n)"
        return base_string


class_dict = {#"kicad_sch": Header,
              "uuid": UniqueIdentifier,
              "lib_symbols": LibrarySymbols,
              "junction": Junction,
              "no_connect": NoConnect,
              "bus_entry": BusEntry,
              "wire": Wire,
              "bus": Bus,
              "image": Image,
              "polyline": GraphicalLine,
              "text": GraphicalText,
              "label": LocalLabel,
              "global_label": GlobalLabel,
              "symbol": SymbolSchematic,
              "sheet_instances": HierarchicalSheetInstances,
              "symbol_instances": SymbolInstances,
              }
