# DEPRECATED
# SHOULD ONLY BE USED AS A REFERENCE TO MAKE leval


from array import array
from const import *
from piece import *

pieceValues = [0, 900, 500, 350, 300, 100]
# these tables will be used for positional bonuses: #

whiteknight = array(
    "b",
    [
        -20,
        -35,
        -10,
        -10,
        -10,
        -10,
        -35,
        -20,
        -10,
        0,
        0,
        3,
        3,
        0,
        0,
        -10,
        -10,
        0,
        15,
        15,
        15,
        15,
        0,
        -10,
        -10,
        0,
        20,
        20,
        20,
        20,
        0,
        -10,
        -10,
        10,
        25,
        20,
        25,
        25,
        10,
        -10,
        -10,
        15,
        25,
        35,
        35,
        35,
        15,
        -10,
        -10,
        15,
        25,
        25,
        25,
        25,
        15,
        -10,
        -20,
        -10,
        -10,
        -10,
        -10,
        -10,
        -10,
        -20,
    ],
)

blackknight = array(
    "b",
    [
        -20,
        -10,
        -10,
        -10,
        -10,
        -10,
        -10,
        -20,
        -10,
        15,
        25,
        25,
        25,
        25,
        15,
        -10,
        -10,
        15,
        25,
        35,
        35,
        35,
        15,
        -10,
        -10,
        10,
        25,
        20,
        25,
        25,
        10,
        -10,
        -10,
        0,
        20,
        20,
        20,
        20,
        0,
        -10,
        -10,
        0,
        15,
        15,
        15,
        15,
        0,
        -10,
        -10,
        0,
        0,
        3,
        3,
        0,
        0,
        -10,
        -20,
        -35,
        -10,
        -10,
        -10,
        -10,
        -35,
        -20,
    ],
)

whitepawn = array(
    "b",
    [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        25,
        25,
        35,
        5,
        5,
        50,
        45,
        30,
        0,
        0,
        0,
        7,
        7,
        5,
        5,
        0,
        0,
        0,
        0,
        14,
        14,
        0,
        0,
        0,
        0,
        0,
        10,
        20,
        20,
        10,
        5,
        5,
        12,
        18,
        18,
        27,
        27,
        18,
        18,
        18,
        25,
        30,
        30,
        35,
        35,
        35,
        30,
        25,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ],
)

blackpawn = array(
    "b",
    [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        30,
        30,
        30,
        35,
        35,
        35,
        30,
        25,
        12,
        18,
        18,
        27,
        27,
        18,
        18,
        18,
        0,
        0,
        10,
        20,
        20,
        10,
        5,
        5,
        0,
        0,
        0,
        14,
        14,
        0,
        0,
        0,
        0,
        0,
        0,
        7,
        7,
        5,
        5,
        0,
        25,
        25,
        35,
        5,
        5,
        50,
        45,
        30,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ],
)

whiteking = array(
    "h",
    [
        -100,
        15,
        15,
        -20,
        10,
        4,
        15,
        -100,
        -250,
        -200,
        -150,
        -100,
        -100,
        -150,
        -200,
        -250,
        -350,
        -300,
        -300,
        -250,
        -250,
        -300,
        -300,
        -350,
        -400,
        -400,
        -400,
        -350,
        -350,
        -400,
        -400,
        -400,
        -450,
        -450,
        -450,
        -450,
        -450,
        -450,
        -450,
        -450,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
    ],
)

blackking = array(
    "h",
    [
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -500,
        -450,
        -450,
        -450,
        -450,
        -450,
        -450,
        -450,
        -450,
        -400,
        -400,
        -400,
        -350,
        -350,
        -400,
        -400,
        -400,
        -350,
        -300,
        -300,
        -250,
        -250,
        -300,
        -300,
        -350,
        -250,
        -200,
        -150,
        -100,
        -100,
        -150,
        -200,
        -250,
        -100,
        7,
        15,
        -20,
        10,
        4,
        15,
        -100,
    ],
)

whitequeen = array(
    "b",
    [
        0,
        0,
        0,
        5,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        7,
        10,
        5,
        0,
        0,
        -15,
        -15,
        -15,
        -10,
        -10,
        -15,
        -15,
        -15,
        -40,
        -40,
        -40,
        -40,
        -40,
        -40,
        -40,
        -40,
        -60,
        -40,
        -40,
        -60,
        -60,
        -40,
        -40,
        -60,
        -30,
        -30,
        -30,
        -30,
        -30,
        -30,
        -30,
        -30,
        0,
        0,
        3,
        3,
        3,
        3,
        3,
        0,
        5,
        5,
        5,
        10,
        10,
        7,
        5,
        5,
    ],
)

blackqueen = array(
    "b",
    [
        5,
        5,
        5,
        10,
        10,
        7,
        5,
        5,
        0,
        0,
        3,
        3,
        3,
        3,
        3,
        0,
        -30,
        -30,
        -30,
        -30,
        -30,
        -30,
        -30,
        -30,
        -60,
        -40,
        -40,
        -60,
        -60,
        -40,
        -40,
        -60,
        -40,
        -40,
        -40,
        -40,
        -40,
        -40,
        -40,
        -40,
        -15,
        -15,
        -15,
        -10,
        -10,
        -15,
        -15,
        -15,
        0,
        0,
        0,
        7,
        10,
        5,
        0,
        0,
        0,
        0,
        0,
        5,
        0,
        0,
        0,
        0,
    ],
)

whiterook = array(
    "b",
    [
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        0,
        0,
        0,
        7,
        10,
        0,
        0,
        0,
        -15,
        -15,
        -15,
        -10,
        -10,
        -15,
        -15,
        -15,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -30,
        -30,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        0,
        10,
        15,
        20,
        20,
        15,
        10,
        0,
        10,
        15,
        20,
        25,
        25,
        20,
        15,
        10,
    ],
)

blackrook = array(
    "b",
    [
        10,
        15,
        20,
        25,
        25,
        20,
        15,
        10,
        0,
        10,
        15,
        20,
        20,
        15,
        10,
        0,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -30,
        -30,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -20,
        -15,
        -15,
        -15,
        -10,
        -10,
        -15,
        -15,
        -15,
        0,
        0,
        0,
        7,
        10,
        0,
        0,
        0,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
    ],
)

whitebishop = array(
    "b",
    [
        -5,
        -5,
        -10,
        -5,
        -5,
        -10,
        -5,
        -5,
        -5,
        10,
        5,
        10,
        10,
        5,
        10,
        -5,
        -5,
        5,
        6,
        15,
        15,
        6,
        5,
        -5,
        -5,
        3,
        15,
        10,
        10,
        15,
        3,
        -5,
        -5,
        3,
        15,
        10,
        10,
        15,
        3,
        -5,
        -5,
        5,
        6,
        15,
        15,
        6,
        5,
        -5,
        -5,
        10,
        5,
        10,
        10,
        5,
        10,
        -5,
        -5,
        -5,
        -10,
        -5,
        -5,
        -10,
        -5,
        -5,
    ],
)

blackbishop = array(
    "b",
    [
        -5,
        -5,
        -10,
        -5,
        -5,
        -10,
        -5,
        -5,
        -5,
        10,
        5,
        10,
        10,
        5,
        10,
        -5,
        -5,
        5,
        6,
        15,
        15,
        6,
        5,
        -5,
        -5,
        3,
        15,
        10,
        10,
        15,
        3,
        -5,
        -5,
        3,
        15,
        10,
        10,
        15,
        3,
        -5,
        -5,
        5,
        6,
        15,
        15,
        6,
        5,
        -5,
        -5,
        10,
        5,
        10,
        10,
        5,
        10,
        -5,
        -5,
        -5,
        -10,
        -5,
        -5,
        -10,
        -5,
        -5,
    ],
)

pos = {
    KNIGHT: {
        BLACK: array(
            "b",
            [
                -20,
                -10,
                -10,
                -10,
                -10,
                -10,
                -10,
                -20,
                -10,
                15,
                25,
                25,
                25,
                25,
                15,
                -10,
                -10,
                15,
                25,
                35,
                35,
                35,
                15,
                -10,
                -10,
                10,
                25,
                20,
                25,
                25,
                10,
                -10,
                -10,
                0,
                20,
                20,
                20,
                20,
                0,
                -10,
                -10,
                0,
                15,
                15,
                15,
                15,
                0,
                -10,
                -10,
                0,
                0,
                3,
                3,
                0,
                0,
                -10,
                -20,
                -35,
                -10,
                -10,
                -10,
                -10,
                -35,
                -20,
            ],
        ),
        WHITE: array(
            "b",
            [
                -20,
                -35,
                -10,
                -10,
                -10,
                -10,
                -35,
                -20,
                -10,
                0,
                0,
                3,
                3,
                0,
                0,
                -10,
                -10,
                0,
                15,
                15,
                15,
                15,
                0,
                -10,
                -10,
                0,
                20,
                20,
                20,
                20,
                0,
                -10,
                -10,
                10,
                25,
                20,
                25,
                25,
                10,
                -10,
                -10,
                15,
                25,
                35,
                35,
                35,
                15,
                -10,
                -10,
                15,
                25,
                25,
                25,
                25,
                15,
                -10,
                -20,
                -10,
                -10,
                -10,
                -10,
                -10,
                -10,
                -20,
            ],
        ),
    },
    PAWN: {
        WHITE: array(
            "b",
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                25,
                25,
                35,
                5,
                5,
                50,
                45,
                30,
                0,
                0,
                0,
                7,
                7,
                5,
                5,
                0,
                0,
                0,
                0,
                14,
                14,
                0,
                0,
                0,
                0,
                0,
                10,
                20,
                20,
                10,
                5,
                5,
                12,
                18,
                18,
                27,
                27,
                18,
                18,
                18,
                25,
                30,
                30,
                35,
                35,
                35,
                30,
                25,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ],
        ),
        BLACK: array(
            "b",
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                30,
                30,
                30,
                35,
                35,
                35,
                30,
                25,
                12,
                18,
                18,
                27,
                27,
                18,
                18,
                18,
                0,
                0,
                10,
                20,
                20,
                10,
                5,
                5,
                0,
                0,
                0,
                14,
                14,
                0,
                0,
                0,
                0,
                0,
                0,
                7,
                7,
                5,
                5,
                0,
                25,
                25,
                35,
                5,
                5,
                50,
                45,
                30,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ],
        ),
    },
    KING: {
        WHITE: array(
            "h",
            [
                -100,
                15,
                15,
                -20,
                10,
                4,
                15,
                -100,
                -250,
                -200,
                -150,
                -100,
                -100,
                -150,
                -200,
                -250,
                -350,
                -300,
                -300,
                -250,
                -250,
                -300,
                -300,
                -350,
                -400,
                -400,
                -400,
                -350,
                -350,
                -400,
                -400,
                -400,
                -450,
                -450,
                -450,
                -450,
                -450,
                -450,
                -450,
                -450,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
            ],
        ),
        BLACK: array(
            "h",
            [
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -500,
                -450,
                -450,
                -450,
                -450,
                -450,
                -450,
                -450,
                -450,
                -400,
                -400,
                -400,
                -350,
                -350,
                -400,
                -400,
                -400,
                -350,
                -300,
                -300,
                -250,
                -250,
                -300,
                -300,
                -350,
                -250,
                -200,
                -150,
                -100,
                -100,
                -150,
                -200,
                -250,
                -100,
                7,
                15,
                -20,
                10,
                4,
                15,
                -100,
            ],
        ),
    },
    QUEEN: {
        BLACK: array(
            "b",
            [
                5,
                5,
                5,
                10,
                10,
                7,
                5,
                5,
                0,
                0,
                3,
                3,
                3,
                3,
                3,
                0,
                -30,
                -30,
                -30,
                -30,
                -30,
                -30,
                -30,
                -30,
                -60,
                -40,
                -40,
                -60,
                -60,
                -40,
                -40,
                -60,
                -40,
                -40,
                -40,
                -40,
                -40,
                -40,
                -40,
                -40,
                -15,
                -15,
                -15,
                -10,
                -10,
                -15,
                -15,
                -15,
                0,
                0,
                0,
                7,
                10,
                5,
                0,
                0,
                0,
                0,
                0,
                5,
                0,
                0,
                0,
                0,
            ],
        ),
        WHITE: array(
            "b",
            [
                0,
                0,
                0,
                5,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                7,
                10,
                5,
                0,
                0,
                -15,
                -15,
                -15,
                -10,
                -10,
                -15,
                -15,
                -15,
                -40,
                -40,
                -40,
                -40,
                -40,
                -40,
                -40,
                -40,
                -60,
                -40,
                -40,
                -60,
                -60,
                -40,
                -40,
                -60,
                -30,
                -30,
                -30,
                -30,
                -30,
                -30,
                -30,
                -30,
                0,
                0,
                3,
                3,
                3,
                3,
                3,
                0,
                5,
                5,
                5,
                10,
                10,
                7,
                5,
                5,
            ],
        ),
    },
    ROOK: {
        WHITE: array(
            "b",
            [
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                0,
                0,
                0,
                7,
                10,
                0,
                0,
                0,
                -15,
                -15,
                -15,
                -10,
                -10,
                -15,
                -15,
                -15,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -30,
                -30,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                0,
                10,
                15,
                20,
                20,
                15,
                10,
                0,
                10,
                15,
                20,
                25,
                25,
                20,
                15,
                10,
            ],
        ),
        BLACK: array(
            "b",
            [
                10,
                15,
                20,
                25,
                25,
                20,
                15,
                10,
                0,
                10,
                15,
                20,
                20,
                15,
                10,
                0,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -30,
                -30,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -20,
                -15,
                -15,
                -15,
                -10,
                -10,
                -15,
                -15,
                -15,
                0,
                0,
                0,
                7,
                10,
                0,
                0,
                0,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
                2,
            ],
        ),
    },
    BISHOP: {
        WHITE: array(
            "b",
            [
                -5,
                -5,
                -10,
                -5,
                -5,
                -10,
                -5,
                -5,
                -5,
                10,
                5,
                10,
                10,
                5,
                10,
                -5,
                -5,
                5,
                6,
                15,
                15,
                6,
                5,
                -5,
                -5,
                3,
                15,
                10,
                10,
                15,
                3,
                -5,
                -5,
                3,
                15,
                10,
                10,
                15,
                3,
                -5,
                -5,
                5,
                6,
                15,
                15,
                6,
                5,
                -5,
                -5,
                10,
                5,
                10,
                10,
                5,
                10,
                -5,
                -5,
                -5,
                -10,
                -5,
                -5,
                -10,
                -5,
                -5,
            ],
        ),
        BLACK: array(
            "b",
            [
                -5,
                -5,
                -10,
                -5,
                -5,
                -10,
                -5,
                -5,
                -5,
                10,
                5,
                10,
                10,
                5,
                10,
                -5,
                -5,
                5,
                6,
                15,
                15,
                6,
                5,
                -5,
                -5,
                3,
                15,
                10,
                10,
                15,
                3,
                -5,
                -5,
                3,
                15,
                10,
                10,
                15,
                3,
                -5,
                -5,
                5,
                6,
                15,
                15,
                6,
                5,
                -5,
                -5,
                10,
                5,
                10,
                10,
                5,
                10,
                -5,
                -5,
                -5,
                -10,
                -5,
                -5,
                -10,
                -5,
                -5,
            ],
        ),
    },
}

pos[HAWK] = {WHITE: pos[BISHOP][WHITE], BLACK: pos[BISHOP][BLACK]}
pos[ELEPHANT] = {WHITE: pos[ROOK][WHITE], BLACK: pos[ROOK][BLACK]}

endking = array(
    "b",
    [
        -5,
        -3,
        -1,
        0,
        0,
        -1,
        -3,
        -5,
        -3,
        10,
        10,
        10,
        10,
        10,
        10,
        -3,
        -1,
        10,
        25,
        25,
        25,
        25,
        10,
        -1,
        0,
        10,
        25,
        30,
        30,
        25,
        10,
        0,
        0,
        10,
        25,
        30,
        30,
        25,
        10,
        0,
        -1,
        10,
        25,
        25,
        25,
        25,
        10,
        -1,
        -3,
        10,
        10,
        10,
        10,
        10,
        10,
        -3,
        -5,
        -3,
        -1,
        0,
        0,
        -1,
        -3,
        -5,
    ],
)

# Init KingTropism table
# Sjeng uses max instead of min..

tropismTable = []
for px in range(8):
    for py in range(8):
        for kx in range(8):
            for ky in range(8):
                knight = abs(ky - py) + abs(kx - px)
                rook = min(abs(ky - py), abs(kx - px)) * 2 + 5
                queen = min(abs(ky - py), abs(kx - px)) + 5
                tropismTable.append(knight + rook * 20 + queen * 20 * 20)
tropismArray = array("I", tropismTable)


def lookUpTropism(px, py, kx, ky, piece):
    value = tropismArray[ky + kx * 8 + py * 8 * 8 + px * 8 * 8 * 8]
    knight = value % 20
    rook = (value - knight) / 20 % 20
    queen = (value - knight - rook * 20) / 20 / 20
    if piece == knight:
        return knight - 5
    if piece == rook:
        return rook - 5
    return queen - 5


def evaluateComplete(game, color=WHITE):
    """A detailed evaluation function, taking into account
    several positional factors"""

    if game.running:
        analyzePawnStructure(game)
        status = (
            evalMaterial(game)
            + evalPawnStructure(game)
            + evalBadBishops(game)
            + evalDevelopment(game)
            + evalCastling(game)
            + evalRookBonus(game)
            + evalKingTropism(game)
        )
    # elif game.status == DRAW:
    #     status = 0
    # elif game.status == WHITEWON:
    #     status = -9999
    # else:
    #     status = 9999

    if color == BLACK_PLAYER:
        status = -status  # Đảo ngược giá trị status khi AI chơi quân đen

    return status


def evalMaterial(game):
    """Đánh giá giá trị vật chất của bàn cờ dựa trên các quân cờ hiện tại"""

    materialValue = [0, 0]  # Danh sách giá trị vật chất của mỗi bên (trắng, đen)
    numPawns = [0, 0]  # Số lượng quân Tốt của mỗi bên
    white = 0
    black = 1

    # Duyệt qua từng ô (square) trong game.board
    for y in range(ROWS):  # Duyệt qua 8 hàng
        for x in range(COLS):  # Duyệt qua 8 cột
            square = game.board.squares[y][x]  # Lấy Square tại (y, x)
            piece = square.piece  # Lấy quân cờ trong Square (nếu có)

            if not piece:  # Nếu không có quân cờ trong Square này, bỏ qua
                continue

            # Cập nhật giá trị vật chất của quân cờ trong Square
            if piece.color == WHITE_PIECE:
                materialValue[white] += pieceValues[piece.sign]
            else:
                materialValue[black] += pieceValues[piece.sign]

            # Đếm số lượng quân Tốt của mỗi bên
            if isinstance(piece, Pawn):
                if piece.color == WHITE_PIECE:
                    numPawns[white] += 1
                else:
                    numPawns[black] += 1

    # Nếu cả hai bên có giá trị vật chất bằng nhau, không cần tính toán gì thêm
    if materialValue[black] == materialValue[white]:
        return 0

    # Tổng giá trị vật chất của cả hai bên
    matTotal = materialValue[black] + materialValue[white]

    # Kiểm tra ai đang dẫn đầu về vật chất
    if materialValue[black] > materialValue[white]:
        # Nếu quân đen đang dẫn đầu
        matDiff = materialValue[black] - materialValue[white]
        val = min(2400, matDiff) + (matDiff * (12000 - matTotal) * numPawns[black]) / (
            6400 * (numPawns[black] + 1)
        )
        return -val  # Trả về giá trị âm khi quân đen dẫn đầu

    else:
        # Nếu quân trắng đang dẫn đầu
        matDiff = materialValue[white] - materialValue[black]
        val = min(2400, matDiff) + (matDiff * (12000 - matTotal) * numPawns[white]) / (
            6400 * (numPawns[white] + 1)
        )
        return val  # Trả về giá trị dương khi quân trắng dẫn đầu



def evalKingTropism(game):
    """Khi các yếu tố khác bằng nhau, việc có quân Mã, Xe và Hậu gần quân Vua đối phương là điều tốt"""

    score = 0

    try:
        wking = game.board.findWhiteKing()
        bking = game.board.findBlackKing()
        wky, wkx = wking.row, wking.col
        bky, bkx = bking.row, bking.col
    except AttributeError:
        return 0

    # Duyệt qua từng ô trong game.board
    for py in range(ROWS):  # Duyệt qua 8 hàng
        for px in range(COLS):  # Duyệt qua 8 cột
            square = game.board.squares[py][px]  # Lấy Square tại (py, px)
            piece = square.piece  # Lấy quân cờ trong Square (nếu có)

            if not piece:
                continue  # Nếu không có quân cờ, bỏ qua

            # Kiểm tra quân cờ trắng
            if piece.color == WHITE_PIECE:
                if isinstance(piece, Knight):
                    score += lookUpTropism(px, py, bkx, bky, KNIGHT)
                elif isinstance(piece, Rook):
                    score += lookUpTropism(px, py, bkx, bky, ROOK)
                elif isinstance(piece, Queen):
                    score += lookUpTropism(px, py, bkx, bky, QUEEN)

            # Kiểm tra quân cờ đen
            elif piece.color == BLACK_PIECE:
                if isinstance(piece, Knight):
                    score -= lookUpTropism(px, py, wkx, wky, KNIGHT)
                elif isinstance(piece, Rook):
                    score -= lookUpTropism(px, py, wkx, wky, ROOK)
                elif isinstance(piece, Queen):
                    score -= lookUpTropism(px, py, wkx, wky, QUEEN)

    return score



def evalRookBonus(game):
    """Các quân Xe hiệu quả hơn khi đứng trên hàng thứ 7 và trên các cột mở"""

    score = 0

    for y_loc in range(ROWS):  # Duyệt qua 8 hàng
        for x_loc in range(COLS):  # Duyệt qua 8 cột
            square = game.board.squares[y_loc][x_loc]  # Lấy Square tại (y_loc, x_loc)
            piece = square.piece  # Lấy quân cờ trong Square (nếu có)

            if not piece or not isinstance(piece, Rook):
                continue  # Nếu không phải quân Xe, bỏ qua

            # Nếu tổng số quân cờ ít hơn hoặc bằng 6, chúng ta giữ quân Xe ở hàng cuối
            if pieceCount <= 6:
                if y_loc in (0, 7):  # Nếu quân Xe ở hàng đầu hoặc cuối
                    score += 12 if piece.color == WHITE_PIECE else -12

            # Kiểm tra xem quân Xe có ở trên một cột mở hay không
            noblack = blackPawnFileBins[x_loc] == 0 and 1 or 0  # Kiểm tra xem có quân Tốt đen trong cột không
            nowhite = whitePawnFileBins[x_loc] == 0 and 1 or 0  # Kiểm tra xem có quân Tốt trắng trong cột không
            if piece.color == WHITE_PIECE:
                if noblack:
                    score += (noblack + nowhite) * 6
                else:
                    score += nowhite * 8
            else:
                if nowhite:
                    score -= (noblack + nowhite) * 6
                else:
                    score -= nowhite * 8

    return score



def evalDevelopment(game):
    """Chủ yếu có ích trong giai đoạn khai cuộc, hàm này khuyến khích máy di chuyển
    các quân Tượng và Mã vào thế chơi, kiểm soát trung tâm bằng các quân Tốt của vua và hậu"""

    score = 0

    # Kiểm tra tình huống kết thúc ván cờ (endgame)
    if pieceCount <= 8:
        wking = game.board.findWhiteKing()
        bking = game.board.findBlackKing()
        score += endking[wking.row * 8 + wking.col]
        score -= endking[bking.row * 8 + bking.col]
        return score

    # Duyệt qua từng ô (square) trong game.board
    for y_loc in range(8):  # 8 hàng
        for x_loc in range(8):  # 8 cột
            square = game.board.squares[y_loc][x_loc]  # Lấy Square tại (y_loc, x_loc)
            piece = square.piece  # Lấy quân cờ trong Square (nếu có)

            if not piece:
                continue  # Nếu không có quân cờ, bỏ qua

            # Cộng điểm cho quân cờ của quân trắng
            if piece.color == WHITE_PIECE:
                if isinstance(piece, Pawn):
                    score += whitepawn[x_loc + y_loc * 8]
                elif isinstance(piece, Knight):
                    score += whiteknight[x_loc + y_loc * 8]
                elif isinstance(piece, Bishop):
                    score += whitebishop[x_loc + y_loc * 8]
                elif isinstance(piece, Rook):
                    score += whiterook[x_loc + y_loc * 8]
                elif isinstance(piece, Queen):
                    score += whitequeen[x_loc + y_loc * 8]
                elif isinstance(piece, King):
                    score += whiteking[x_loc + y_loc * 8]
            else:
                # Cộng điểm cho quân cờ của quân đen
                if isinstance(piece, Pawn):
                    score -= blackpawn[x_loc + y_loc * 8]
                elif isinstance(piece, Knight):
                    score -= blackknight[x_loc + y_loc * 8]
                elif isinstance(piece, Bishop):
                    score -= blackbishop[x_loc + y_loc * 8]
                elif isinstance(piece, Rook):
                    score -= blackrook[x_loc + y_loc * 8]
                elif isinstance(piece, Queen):
                    score -= blackqueen[x_loc + y_loc * 8]
                elif isinstance(piece, King):
                    score -= blackking[x_loc + y_loc * 8]

    return score


def evalCastling(game):
    """Khuyến khích việc nhập thành"""

    if pieceCount <= 6:
        return 0  # Nếu có ít quân cờ, không cần tính toán nhập thành nữa

    score = 0

    for color, mod in ((WHITE_PIECE, -1), (BLACK_PIECE, 1)):
        mainrow = game.board.squares[int(3.5 - 3.5 * mod)]  # Hàng của quân Vua (hàng 0 hoặc 7)
        
        for x_loc, square in enumerate(mainrow):
            piece = square.piece  # Lấy quân cờ trong ô này
            if piece and isinstance(piece, King) and piece.color == color:
                bin = whitePawnFileBins if color == WHITE_PIECE else blackPawnFileBins
                if not bin[x_loc]:  # Nếu không có quân Tốt trong cột của quân Vua
                    score -= 10 * mod
                break

        if game.hasCastled[color]:
            score += 15 * mod
            continue

        # Kiểm tra quyền nhập thành
        if not game.board.can_castle(color, kingside=True) and not game.board.can_castle(color, kingside=False):
            score -= 60 * mod
        elif not game.board.can_castle(color, kingside=True):
            score -= 30 * mod
        elif not game.board.can_castle(color, kingside=False):
            score -= 45 * mod

    return score




def evalBadBishops(game):
    """Các quân Tượng có thể bị giới hạn trong việc di chuyển
    nếu có quá nhiều quân Tốt ở các ô có màu của chúng."""

    score = 0

    # Duyệt qua từng ô (square) trong game.board
    for y_loc in range(ROWS):  # Duyệt qua 8 hàng
        for x_loc in range(COLS):  # Duyệt qua 8 cột
            square = game.board.squares[y_loc][x_loc]  # Lấy Square tại (y_loc, x_loc)
            piece = square.piece  # Lấy quân cờ trong Square (nếu có)

            # Kiểm tra nếu quân cờ là quân Tượng (Bishop)
            if not piece or not(isinstance, Bishop):
                continue

            # Mod để xác định bên nào (trắng = 1, đen = -1)
            mod = 1 if piece.color == WHITE_PIECE else -1

            # Kiểm tra màu ô của quân Tượng
            lightsq = (x_loc + y_loc) % 2 == 1

            if lightsq:
                # Nếu quân Tượng ở ô sáng, giảm điểm dựa trên số lượng quân Tốt ở ô sáng
                score -= pawnColorBins[0] * 7 * mod
            else:
                # Nếu quân Tượng ở ô tối, giảm điểm dựa trên số lượng quân Tốt ở ô tối
                score -= pawnColorBins[1] * 7 * mod

    return score


def evalPawnStructure(game):
    """Given the pawn formations, penalize or bonify the position according to
    the features it contains"""

    score = 0

    for x_loc in range(8):
        # First, look for doubled pawns
        # In chess, two or more pawns on the same file usually hinder each other,
        # so we assign a penalty

        if whitePawnFileBins[x_loc] > 1:
            score -= 10
        if blackPawnFileBins[x_loc] > 1:
            score += 10

        # Now, look for an isolated pawn, i.e., one which has no neighbor pawns
        # capable of protecting it from attack at some point in the future

        if x_loc == 0 and whitePawnFileBins[x_loc] > 0 and whitePawnFileBins[1] == 0:
            score -= 15
        elif x_loc == 7 and whitePawnFileBins[x_loc] > 0 and whitePawnFileBins[6] == 0:
            score -= 15
        elif (
            whitePawnFileBins[x_loc] > 0
            and whitePawnFileBins[x_loc - 1] == 0
            and whitePawnFileBins[x_loc + 1] == 0
        ):
            score -= 15

        if x_loc == 0 and blackPawnFileBins[x_loc] > 0 and blackPawnFileBins[1] == 0:
            score += 15
        elif x_loc == 7 and blackPawnFileBins[x_loc] > 0 and blackPawnFileBins[6] == 0:
            score += 15
        elif (
            blackPawnFileBins[x_loc] > 0
            and blackPawnFileBins[x_loc - 1] == 0
            and blackPawnFileBins[x_loc + 1] == 0
        ):
            score += 15

        # Penalize pawn rams, because they restrict movement
        score -= 8 * pawnRams

    return score


whitePawnFileBins = [0] * 8
pawnColorBins = [0] * 2
pawnRams = 0
blackPawnFileBins = [0] * 8


def analyzePawnStructure(game):
    """Xem xét các vị trí quân Tốt để phát hiện các đặc điểm như quân Tốt đôi,
    quân Tốt cô lập hoặc quân Tốt thẳng."""

    global whitePawnFileBins, blackPawnFileBins, pawnColorBins, pawnRams
    whitePawnFileBins = [0] * 8
    blackPawnFileBins = [0] * 8
    pawnColorBins[0] = 0
    pawnColorBins[1] = 0
    pawnRams = 0

    global pieceCount
    pieceCount = 0

    # Duyệt qua từng ô (square) trong game.board
    for y in range(ROWS):  # 8 hàng
        for x in range(COLS):  # 8 cột
            square = game.board.squares[y][x]  # Lấy square tại (y, x)
            piece = square.piece  # Lấy quân cờ trong square này (nếu có)

            if piece and isinstance(piece, Pawn):  # Kiểm tra nếu là quân Tốt (Pawn)
                # Nếu là quân Tốt của quân trắng
                if piece.color == WHITE:
                    whitePawnFileBins[x] += 1
                else:  # Nếu là quân Tốt của quân đen
                    blackPawnFileBins[x] += 1

                # Xem quân Tốt này có ở ô trắng hay đen
                if (y + x) % 2 == 0:
                    pawnColorBins[0] += 1  # Quân Tốt ở ô màu trắng
                else:
                    pawnColorBins[1] += 1  # Quân Tốt ở ô màu đen

                # Kiểm tra tình huống "pawn ram" (quân Tốt đẩy nhau)
                if piece.color == WHITE_PIECE and y + 1 < 8:  # Quân trắng có thể di chuyển xuống
                    ahead = game.board.squares[y + 1][x].piece
                elif piece.color == BLACK_PIECE and y - 1 >= 0:  # Quân đen có thể di chuyển lên
                    ahead = game.board.squares[y - 1][x].piece
                else:
                    ahead = None  # Nếu là quân Tốt ở hàng đầu hoặc cuối không có quân để xem xét

                # Nếu ô phía trước có cùng màu quân Tốt
                if ahead and isinstance(ahead, Pawn) and ahead.color == piece.color:
                    if piece.color == WHITE_PIECE:
                        pawnRams += 1  # Quân Tốt trắng bị đẩy (ram)
                    else:
                        pawnRams -= 1  # Quân Tốt đen bị đẩy (ram)

            elif piece:  # Nếu có quân cờ khác ngoài quân Tốt
                pieceCount += 1  # Đếm tổng số quân cờ khác quân Tốt

