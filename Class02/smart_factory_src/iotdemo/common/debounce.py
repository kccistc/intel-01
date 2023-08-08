"""
Debouncing decorator
"""
from threading import Timer

__all__ = ('debounce', )


def debounce(wait):
    """ Debounce decorator API"""
    def decorator(func):
        """ for decorator """
        def debounced(*args, **kwargs):
            """ for debounced """
            def call_it():
                """ real func """
                func(*args, **kwargs)

            try:
                debounced.t.cancel()
            except AttributeError:
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()

        return debounced

    return decorator
