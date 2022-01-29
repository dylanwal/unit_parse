import pytest

from unit_parse import parser, Quantity, config


examples = [
    # complex
    ['18 mm Hg at 68 °F ; 20 mm Hg at 77° F (NTP, 1992)', [[Quantity('18 mmHg'), Quantity('68 degF')],
                                                           [Quantity('20 mmHg'), Quantity('77 degF')]]],
    ['Sound travels at 0.34 km/s', Quantity('0.34 km/s')],
    ['Pass me a 300 ml beer.', Quantity("300 ml")],
]


@pytest.mark.parametrize("input, output", examples)
def test_result_multi(input, output):
    delete_ = [
        "beer",
        "(NTP, 1992)"
    ]
    assert output == parser(input)