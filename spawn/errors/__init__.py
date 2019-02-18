"""Defines errors used in spawn
"""

class SpawnError(Exception):
    """Base class for all errors in spawn"""

class ParserError(SpawnError):
    """Base class for all parsing errors in spawn"""

class MacroNotFoundError(ParserError):
    """Error raised when a macro is not found
    """
    def __init__(self, macro_name):
        super().__init__('Macro "{}" not found'.format(macro_name))

class GeneratorNotFoundError(ParserError):
    """Error raised when a generator is not found
    """
    def __init__(self, generator_name):
        super().__init__('Generator "{}" not found'.format(generator_name))

class EvaluatorNotFoundError(ParserError):
    """Error raised when an evaluator is not found
    """
    def __init__(self, evaluator_name):
        super().__init__('Evaluator "{}" not found'.format(evaluator_name))

class EvaluatorTypeError(ParserError):
    """Error raised when an evaluator is provided with incorrect arguments
    """
    def __init__(self, evaluator_name, expected, actual):
        super().__init__(
            '{}() takes the following arguments: {} ({} provided)'.format(
                evaluator_name, ', '.join(expected), ', '.join(str(a) for a in actual)
            )
        )

class InvalidOperatorError(ParserError):
    """Error raised when an operator is invalid
    """
    def __init__(self, operator_name, position):
        super().__init__('Invalid operator in {} near position {}'.format(operator_name, position))

class SpecFormatError(ParserError):
    """Error raised when the format of the spec object is incorrect
    """
    def __init__(self, error):
        super().__init__('Invalid spec format: {}'.format(error))
