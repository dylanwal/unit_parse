import pytest

from unit_parse import Q, U
from unit_parse.classification import ClassificationObj, QuantClass, quantity_classifier


example_quantity_classifier = [
    [1, [ClassificationObj(1, U(""), 1, QuantClass.NUMBER)]],
    [[1], [ClassificationObj(1, U(""), 1, QuantClass.NUMBER)]],
    [Q("5 g/mol"), [ClassificationObj(Q("5 g/mol"), U("g/mol"), 1, QuantClass.SINGLE)]],
    [[Q("5 g/mol")], [ClassificationObj(Q("5 g/mol"), U("g/mol"), 1, QuantClass.SINGLE)]],

    [[Q("40 degF"), Q("4 degC")], [ClassificationObj(Q("40 degF"), U("degF"), 2, QuantClass.SINGLE)]],

    [[[Q("40 degF"), Q("40 psi")]],
     [ClassificationObj([[Q("40 degF"), Q("40 psi")]], U("degF"), 1, QuantClass.CONDITION)]],

    [[Q("40 degF"), Q("40 psi"), Q("4 degC"), Q("50 degF")],
     [ClassificationObj(Q("40 degF"), U("degF"), 3, QuantClass.SINGLE),
      ClassificationObj(Q("40 psi"), U("psi"), 1, QuantClass.SINGLE)
      ]
     ],

    [[[Q("40 degF"), Q("40 psi")], [Q("50 degF"), Q("50 psi")]],
     [ClassificationObj([[Q("40 degF"), Q("40 psi")], [Q("50 degF"), Q("50 psi")]],
                        U("degF"), 1, QuantClass.SERIES_CONDITIONS, len_=2)]],

    [[[Q("40 degF"), Q("40 psi")], Q("40 degF"), Q("40 psi"), [Q("4 degC"), Q("50 degF"), Q("52 degF")]],
     [ClassificationObj(Q("40 degF"), U("degF"), 4, QuantClass.SINGLE),
      ClassificationObj(Q("40 psi"), U("psi"), 1, QuantClass.SINGLE),
      ClassificationObj([[Q("40 degF"), Q("40 psi")]], U("degF"), 1, QuantClass.CONDITION)
      ]
     ],

    [[[[Q("40 degF"), Q("40 psi")], Q("40 degF")], Q("40 degF"), Q("40 psi"),
      [Q("4 degC"), Q("50 degF"), Q("52 degF")]],
     [ClassificationObj(Q("40 degF"), U("degF"), 5, QuantClass.SINGLE),
      ClassificationObj([[Q("40 degF"), Q("40 psi")]], U("degF"), 1, QuantClass.CONDITION),
      ClassificationObj(Q("40 psi"), U("psi"), 1, QuantClass.SINGLE)
      ]
     ],

    [[[[Q("40 degF"), 40], Q("40 degF")], Q("40 degF"), Q("40 psi"),
      [Q("4 degC"), Q("50 degF"), Q("52 degF")]],
     [ClassificationObj(Q("40 degF"), U("degF"), 5, QuantClass.SINGLE),
      ClassificationObj([[Q("40 degF"), 40]], U("degF"), 1, QuantClass.CONDITION),
      ClassificationObj(Q("40 psi"), U("psi"), 1, QuantClass.SINGLE)
      ]
     ],

    [[[Q("40 degF"), Q("40 psi")], [Q("50 kg"), Q("50 psi")]],
     [ClassificationObj([[Q("40 degF"), Q("40 psi")], [Q("50 kg"), Q("50 psi")]],
                        None, 1, QuantClass.SERIES_CONDITIONS, len_=2)]],

]


@pytest.mark.parametrize("input_, output_", example_quantity_classifier)
def test_reduce_quantities(input_, output_):
    assert output_ == quantity_classifier(input_)


example_error = [
    [[[[["fish"]]]], ValueError],
    ["fish", TypeError],
    [["fish"], TypeError],
    [[["fish"]], TypeError],
    [[[[Q("40 degF"), Q("40 psi")], Q("40 degF")], "40 degF", Q("40 psi"),
      [Q("4 degC"), Q("50 degF"), Q("52 degF")]], TypeError],
    [[[[Q("40 degF"), "40 psi"], Q("40 degF")], Q("40 degF"), Q("40 psi"),
      [Q("4 degC"), Q("50 degF"), Q("52 degF")]], TypeError],
    [[[["40 degF", Q("40 psi")], Q("40 degF")], Q("40 degF"), Q("40 psi"),
      [Q("4 degC"), Q("50 degF"), Q("52 degF")]], TypeError]
]


@pytest.mark.parametrize("input_, error_", example_error)
def test_reduce_quantities_error(input_, error_):
    with pytest.raises(error_):
        quantity_classifier(input_)
