import abjad
import inspect
import pytest


classes = pytest.helpers.list_all_ide_classes()


@pytest.mark.parametrize("object_", classes)
def test_idetools___doc___01(object_):
    """
    All classes have a docstring. All class methods have a docstring.
    """

    ignored_names = (
        "__documentation_section__",
        "__dict__",
        "__init__",
        "__new__",
    )

    ignored_classes = ()

    assert object_.__doc__ is not None
    if object_.__name__ in ignored_classes:
        return
    for attribute in inspect.classify_class_attrs(object_):
        if attribute.name in ignored_names:
            continue
        elif attribute.defining_class is not object_:
            continue
        if attribute.name[0].isalpha() or attribute.name.startswith("__"):
            message = f"{object_.__name__}.{attribute.name}"
            assert getattr(object_, attribute.name).__doc__ is not None, message
