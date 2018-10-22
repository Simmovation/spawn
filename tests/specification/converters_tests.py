import pytest

from multiwindcalc.parsers import SpecificationParser, DictSpecificationProvider
from multiwindcalc.specification import DictSpecificationConverter
from multiwindcalc.parsers.specification_parser import DEFAULT_COMBINATORS, ZIP

SPEC_1 = {
    'base_file': './file/input.in',
    'creation_time': '2018-10-19T12:00:00',
    'notes': 'Some notes',
    'spec': {
        'policy:path': 'WS{wind_speed}/WD{wind_direction}',
        'wind_speed': 12.0,
        'wind_direction': 180.0
    }
}

EXPECTED_1 = {
    'base_file': './file/input.in',
    'metadata': {
        'creation_time': '2018-10-19T12:00:00',
        'notes': 'Some notes'
    },
    'spec': [{
        'name': 'wind_speed',
        'value': 12.0,
        'children': [
            {
                'path': 'WS12.0/WD180.0',
                'name': 'wind_direction',
                'value': 180.0
            }
        ]
    }]
}

SPEC_2 = {
    'base_file': './file/input.in',
    'creation_time': '2018-10-19T12:00:00',
    'notes': 'Some notes',
    'spec': {
        'policy:path': 'WS{wind_speed}/WD{wind_direction}',
        'wind_speed': 12.0,
        'wind_direction': [0.0, 180.0]
    }
}

EXPECTED_2 = {
    'base_file': './file/input.in',
    'metadata': {
        'creation_time': '2018-10-19T12:00:00',
        'notes': 'Some notes'
    },
    'spec': [{
        'name': 'wind_speed',
        'value': 12.0,
        'children': [
            {
                'path': 'WS12.0/WD0.0',
                'name': 'wind_direction',
                'value': 0.0
            },
            {
                'path': 'WS12.0/WD180.0',
                'name': 'wind_direction',
                'value': 180.0
            }
        ]
    }]
}

SPEC_3 = {
    'base_file': './file/input.in',
    'creation_time': '2018-10-19T12:00:00',
    'notes': 'Some notes',
    'spec': {
        'policy:path': 'WS{wind_speed}/WD{wind_direction}',
        'wind_speed': [3.0, 12.0],
        'wind_direction': [0.0, 180.0]
    }
}

EXPECTED_3 = {
    'base_file': './file/input.in',
    'metadata': {
        'creation_time': '2018-10-19T12:00:00',
        'notes': 'Some notes'
    },
    'spec': [{
        'name': 'wind_speed',
        'value': 3.0,
        'children': [
            {
                'path': 'WS3.0/WD0.0',
                'name': 'wind_direction',
                'value': 0.0
            },
            {
                'path': 'WS3.0/WD180.0',
                'name': 'wind_direction',
                'value': 180.0
            }
        ]
    },{
        'name': 'wind_speed',
        'value': 12.0,
        'children': [
            {
                'path': 'WS12.0/WD0.0',
                'name': 'wind_direction',
                'value': 0.0
            },
            {
                'path': 'WS12.0/WD180.0',
                'name': 'wind_direction',
                'value': 180.0
            }
        ]
    }]
}

SPEC_4 = {
    'base_file': './file/input.in',
    'creation_time': '2018-10-19T12:00:00',
    'notes': 'Some notes',
    'spec': {
        'policy:path': 'WS{wind_speed}/WD{wind_direction}',
        'combine:zip': {
            'wind_speed': [3.0, 12.0],
            'wind_direction': [0.0, 180.0]
        }
    }
}

EXPECTED_4 = {
    'base_file': './file/input.in',
    'metadata': {
        'creation_time': '2018-10-19T12:00:00',
        'notes': 'Some notes'
    },
    'spec': [{
        'name': 'wind_speed',
        'value': 3.0,
        'children': [
            {
                'path': 'WS3.0/WD0.0',
                'name': 'wind_direction',
                'value': 0.0
            }
        ]
    },{
        'name': 'wind_speed',
        'value': 12.0,
        'children': [
            {
                'path': 'WS12.0/WD180.0',
                'name': 'wind_direction',
                'value': 180.0
            }
        ]
    }]
}

def parse(spec):
    return SpecificationParser(DictSpecificationProvider(spec)).parse()

@pytest.fixture
def dict_converter():
    return DictSpecificationConverter()

@pytest.mark.parametrize('spec,expected', [
    (SPEC_1, EXPECTED_1),
    (SPEC_2, EXPECTED_2),
    (SPEC_3, EXPECTED_3),
    (SPEC_4, EXPECTED_4),
])
def test_dict_converter_converts_parsed_spec(dict_converter, spec, expected):
    spec_model = parse(spec)
    assert dict_converter.convert(spec_model) == expected
