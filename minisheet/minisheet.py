from __future__ import with_statement

'''
Very minimal class for reading cells from 2d structures (e.g. those
returned by the csv reader.

reader classes extend GridModel and contain a Field and optional XAxis and
YAxis

class Customers(GridModel):
   name = XAxis()
   category = YAxis()
   age = Field()



You can use properties to infer values...


class Customers(GridModel):
   name = XAxis()
   category = YAxis()
   age = Field()
   
   def __get_centinarian(self):
       return self.age > 99

   centinarian = property(__get_centinarian)

'''

class FieldModelException(Exception):
   pass


class CellRange:
    def __init__(self):
        self.value = None
    
    def __str__(self):
        return str(self.value)


class Field(CellRange):
    
    def read_cell(self, (x, y), value):
        """
        
        """
        self.value = value
        return True
    

class XAxis(CellRange):
    """
    Store values on the XAxis.  After calling read_cell, the current XAxis
    value will be available in value
    """
    def __init__(self):
        self.value = None
        self.values = {}

    def read_cell(self, (x, y), value):
        if y is 0:
            self.values[x] = value
            return True
        self.value = self.values[x]


class YAxis(CellRange):
    """
    Store values on the YAxis.  After calling read_cell, the current YAxis
    value will be available in value
    """
    def __init__(self):
        self.value = None
        self.values = {}
        
    def read_cell(self, (x, y), value):
        if x is 0:
            self.values[y] = value
            return True
        self.value = self.values[y]


class _GridModel(type):
    """
    The Metaclass for GridModel
    """
    def __new__(meta, name, bases, attrs):
       cellattr = None
       metadata = []
       for attr, cls in attrs.items():
           if hasattr(cls, '__class__') and cls.__class__.__name__ == 'Field':
               if cellattr is not None:
                   raise FieldModelException('Cells added to FieldModel more than once')
               cellattr = attr
           else:
               if isinstance(cls, CellRange):
                   # For fields added, cls is set to None at this point
                   metadata.append(attr)
       attrs['__cell_attr__'] = cellattr
       attrs['__metadata_attrs__'] = metadata
       return type.__new__(meta, name, bases, attrs)


        
class GridModel:
    __metaclass__ = _GridModel
    
    def __init__(self):
        # Get instance of __cellattr__ into __cells__
        self.__cells__ = getattr(self.__class__, self.__cell_attr__)
        self.__metadata__ = []
        for field in self.__metadata_attrs__:
            self.__metadata__.append(getattr(self, field))
        
    def read_cells(self, data):
        """
        Generator function, reads 2d data, yields data from cells only
        
        At the moment has a simple model - if an Axis has handled the
        cell reading then __cells__.read_cell will not be called
        """
        for y, row_data in enumerate(data):
            # Special case if reading single columns of strings
            if isinstance(row_data, str):
                row = row_data, # return tuple
            else:
                row = row_data
            
            for x, value in enumerate(row):
                handled = False
                for handler in self.__metadata__:
                    handled |= bool(handler.read_cell((x, y), value))
                
                if not handled and self.__cells__.read_cell((x, y), value):
                    self.data_ready()
                    yield(self)
    
    def data_ready(self):
        """
        Called when data has been read from a cell
        """
        pass
    
    def __str__(self):
        return str(self.__cells__.value)
        
