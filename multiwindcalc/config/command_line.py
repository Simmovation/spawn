"""Defines the a :class:`ConfigurationBase` implementation that parses values from the command line
"""
from .base import ConfigurationBase

DEFAULT_CATEGORY = 'multiwindcalc'

class CommandLineConfiguration(ConfigurationBase):
    """Implementation of :class:`ConfugurationBase` that is able to parse
    configuration values from command line arguments
    """

    def __init__(self, **kwargs):
        """Initialises :class:`CommandLineConfiguration`

        :param kwargs: The kwargs passed on the command line
        :type kwargs: kwargs
        """
        self._args = {DEFAULT_CATEGORY: {}}
        for k, v in kwargs.items():
            if k == 'd':
                for defintion in v:
                    key, value = defintion.split('=')
                    category, key = key.split('.', 1) if '.' in key else (DEFAULT_CATEGORY, key)
                    self._args.setdefault(category, {})
                    self._args[category][key] = value
            else:
                self._args[DEFAULT_CATEGORY][k] = v
    
    def _get_value(self, category, key):
        return self._args.get(category, {}).get(key)