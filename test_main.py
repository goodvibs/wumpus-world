import pytest

from main import wumpus_world


def test_case_1():
    cave = [
        [*"____"],
        [*"_W__"],
        [*"___G"],
        [*"P___"]
    ]
    assert wumpus_world(cave)


def test_case_2():
    cave = [
        [*"____"],
        [*"_P__"],
        [*"____"],
        [*"_W_G"]
    ]
    assert wumpus_world(cave)


def test_case_3():
    cave = [
        [*"____"],
        [*"____"],
        [*"W__P"],
        [*"__PG"]
    ]
    assert not wumpus_world(cave)


def test_case_4():
    cave = [
        [*"__GP"],
        [*"_P__"],
        [*"W___"],
        [*"____"]
    ]
    assert wumpus_world(cave)


def test_case_5():
    cave = [
        [*"__W_"],
        [*"____"],
        [*"___P"],
        [*"___G"]
    ]
    assert wumpus_world(cave)


def test_case_6():
    cave = [
        [*"__W_"],
        [*"____"],
        [*"__PP"],
        [*"___G"]
    ]
    assert wumpus_world(cave)


def test_case_7():
    cave = [
        [*"__W_"],
        [*"____"],
        [*"_PPP"],
        [*"___G"]
    ]
    assert wumpus_world(cave)


def test_case_8():
    cave = [
        [*"___P"],
        [*"__PG"],
        [*"___P"],
        [*"W___"]
    ]
    assert not wumpus_world(cave)


def test_case_9():
    cave = [
        [*"__P_"],
        [*"____"],
        [*"__P_"],
        [*"__WG"]
    ]
    assert wumpus_world(cave)


def test_case_10():
    cave = [
        [*"____"],
        [*"__PW"],
        [*"PG__"],
        [*"____"]
    ]
    assert wumpus_world(cave)


def test_case_11():
    cave = [
        [*"__P_"],
        [*"____"],
        [*"WP__"],
        [*"_G__"]
    ]
    assert wumpus_world(cave)


def test_case_12():
    cave = [
        [*"__PG"],
        [*"____"],
        [*"__WP"],
        [*"____"]
    ]
    assert wumpus_world(cave)


def test_case_13():
    cave = [
        [*"___W"],
        [*"__P_"],
        [*"__G_"],
        [*"P___"]
    ]
    assert wumpus_world(cave)


def test_case_14():
    cave = [
        [*"__WP"],
        [*"_P__"],
        [*"____"],
        [*"_G__"]
    ]
    assert wumpus_world(cave)


def test_case_15():
    cave = [
        [*"__WP"],
        [*"____"],
        [*"__P_"],
        [*"P_G_"]
    ]
    assert wumpus_world(cave)


def test_case_16():
    cave = [
        [*"__PG"],
        [*"___W"],
        [*"__PP"],
        [*"____"]
    ]
    assert wumpus_world(cave)
