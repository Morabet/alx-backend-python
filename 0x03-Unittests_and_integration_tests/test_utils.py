#!/usr/bin/env python3
""" A module for testing the utils module"""

from utils import access_nested_map, get_json, memoize
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock, MagicMock
from typing import Dict, Tuple, Union


class TestAccessNestedMap(unittest.TestCase):
    """ Tests the `access_nested_map` function"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(
        self, nested_map: Dict, path: Tuple[str],
        expected_result: Union[Dict, int]
    ) -> None:
        """ Tests `access_nested_map`'s output"""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected_result)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(
        self, nested_map: Dict, path: Tuple[str]
    ) -> None:
        """ Tests `access_nested_map`'s exception raising"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """ Tests the `get_json` function"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("requests.get")
    def test_get_json(
        self, test_url: str, test_payload: Dict, mock_get: MagicMock
    ) -> None:
        """ Tests `get_json`'s output"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response
        result = get_json(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """ Tests the `memoize` function"""

    def test_memoize(self):
        """ Tests `memoize`'s output"""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass,
            "a_method",
            return_value=lambda: 42
        ) as mock_a_method:
            obj = TestClass()
            self.assertEqual(obj.a_property(), 42)
            self.assertEqual(obj.a_property(), 42)
            mock_a_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
