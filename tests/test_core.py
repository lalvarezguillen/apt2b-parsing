from apt2b.core import (
    has_interesting_category,
    is_in_stock,
    is_sleeper,
    create_cora_row,
    get_image_info,
    NAME_COL_IDX,
    STOCK_COL_IDX,
    SKU_COL_IDX,
    URL_COL_IDX,
    SALEPRICE_COL_IDX,
    PRICE_COL_IDX,
    DESCRIPTION_COL_IDX,
    RETAILER_CODE,
    RETAILER_NAME,
    IMAGEURL_COL_IDX,
)


class TestHasInterestingCategory:
    @staticmethod
    def create_dummy_row(name):
        row = ["dummy"] * 40
        row[NAME_COL_IDX] = name
        return row

    def test_has_interesting_category(self):
        cases = [
            (self.create_dummy_row("Some sofa"), (True, "sofa")),
            (self.create_dummy_row("A bench"), (False, "bench")),
            (
                self.create_dummy_row("it says sofa, but it also says sectional"),
                (False, "sectional"),
            ),
            (self.create_dummy_row("nonsense"), (False, "")),
        ]

        for inp, out in cases:
            assert out == has_interesting_category(inp)


class TestIsInStock:
    @staticmethod
    def create_dummy_row(instock):
        row = ["dummy"] * 40
        row[STOCK_COL_IDX] = instock
        return row

    def test_is_in_stock(self):
        cases = [
            (self.create_dummy_row("yes"), True),
            (self.create_dummy_row("YES"), True),
            (self.create_dummy_row("no"), False),
            (self.create_dummy_row("maybe"), False),
        ]

        for inp, out in cases:
            assert out == is_in_stock(inp)


class TestIsSleeper:
    @staticmethod
    def create_dummy_row(name):
        row = ["dummy"] * 40
        row[NAME_COL_IDX] = name
        return row

    def test_is_sleeper(self):
        cases = [
            (self.create_dummy_row("contains sleeper"), 1),
            (self.create_dummy_row("CONTAINS SLEEPER"), 1),
            (self.create_dummy_row("spartan chair"), 0),
        ]

        for inp, out in cases:
            assert is_sleeper(inp) == out


def test_create_cora_row():
    row = ["dummy"] * 40
    row[SKU_COL_IDX] = "sku"
    row[URL_COL_IDX] = "url"
    row[NAME_COL_IDX] = "name"
    row[SALEPRICE_COL_IDX] = "5.0"
    row[PRICE_COL_IDX] = ""
    row[DESCRIPTION_COL_IDX] = "description"

    expected = (
        RETAILER_CODE,
        RETAILER_NAME,
        "sku",
        "url",
        "category",
        "name",
        0,
        5.0,
        None,
        "",
        "",
        "",
        "image",
        "description",
    )
    res = create_cora_row(row, "category", "image")
    assert expected == res


class TestGetImageInfo:
    @staticmethod
    def create_dummy_row(imageurl):
        row = ["dummy"] * 40
        row[IMAGEURL_COL_IDX] = imageurl
        return row

    def test_get_image_info(self):
        cases = [
            (
                self.create_dummy_row("https://images.com/image.jpeg?200"),
                ("12+image.jpeg", "https://images.com/image.jpeg?200"),
            )
        ]

        for inp, out in cases:
            assert out == get_image_info(inp)
