import unittest

from make_web import make_title

class TestMakeWeb(unittest.TestCase):
  def test_make_title(self):
    cases = [
        ('hello world', 'Hello World'),
        ('hello ABC world', 'Hello ABC World'),
        ('hello world ABC', 'Hello World ABC'),
        ('hello world (ABC)', 'Hello World (ABC)'),
        ('ABC hello world', 'ABC Hello World'),
        ('(ABC) hello world', '(ABC) Hello World'),
        ('ABC', 'ABC'),
    ]
    for text, expected in cases:
      with self.subTest(text=text, expected=expected):
        self.assertEqual(make_title(text), expected)


if __name__ == '__main__':
  unittest.main()
