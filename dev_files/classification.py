import logging

from testing_func import testing_func, test_logger
from unit_parse.classification import *
from unit_parse import logger, Q, U

test_logger.setLevel(logging.DEBUG)
logger.setLevel(logging.CRITICAL)

test_quantity_classifier = [
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

testing_func(quantity_classifier, test_quantity_classifier)
