""" A library of object-oriented patterns """

class _meta_class_extension(type):
  def __init__(cls, classname, bases, classdict):
    for target_class in bases[1:]:
      for name, attribute in classdict.items():
        if not callable(attribute): continue
        assert not hasattr(target_class, name), (
          "class %s has already a method %s"
          % (target_class.__name__, name))
        setattr(target_class, name, attribute)

class extends:
  """ Extends existing classes with new methods

  * synopsis *

  class some_descriptive_text(extends, some_existing_class,
                                       another_existing_class, ...):

    def new_method(self, ...): ...

    def another_new_method(self, ...): ...

  obj = some_existing_class(...)
  obj.new_method(...)
  obj = another_existing_class(...)
  obj.new_method(...)
  # class 'some_descriptive_name' is an empty shell with no use by itself.

  * motivation *

  The traditional way to add methods to an existing class involves typing
  three times the same information:

  def new_method(self, ...): ...
  existing_class.new_method = new_method

  or to defer the nameing to after the definition:

  def foo(self, ...): ...
  existing_class.new_method = foo

  A bit of metaclass trickery results in a cleaner syntax.
  """
  __metaclass__ = _meta_class_extension
