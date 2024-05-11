import src.utils.add as addition


class TestAddition:
    def test_nonzero_addition(self):
        assert addition.add(1, 2) == 3

    def test_x_zero_addition(self):
        assert addition.add(0, 2) == 2

    def test_y_zero_addition(self):
        assert addition.add(1, 0) == 1

    def test_both_zero_addition(self):
        assert addition.add(0, 0) == 0
