from unittest import TestCase

from financier.functions.fastapi_lambda import handler


class TestFastAPIFunction(TestCase):
    def test_handler(self):
        self.assertEqual(200, handler(None, None).get("statusCode"))
