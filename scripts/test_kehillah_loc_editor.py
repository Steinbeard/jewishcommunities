import unittest

from kehillah_loc_editor import decode_value, encode_value, parse_entries


class LocalizationEditorTests(unittest.TestCase):
    def test_multiline_and_comments_survive_one_value_edit(self):
        source = (
            'l_english:\r\n'
            ' # explanation\r\n'
            ' first.key:0 "First \\"quote\\"\\nNext line" # note\r\n'
            ' second_key:0 "Other"\r\n'
        )
        entries = parse_entries(source)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0][2], 'First "quote"\nNext line')
        start, end = entries[0][3:5]
        updated = source[:start] + encode_value('Changed\nline') + source[end:]
        self.assertEqual(parse_entries(updated)[0][2], 'Changed\nline')
        self.assertIn(' # explanation\r\n', updated)
        self.assertIn('" # note\r\n second_key:0 "Other"', updated)

    def test_literal_newline_and_backslash(self):
        value = 'A real\nline with \\ and "quotes"'
        self.assertEqual(decode_value(encode_value(value)), value)
        self.assertEqual(parse_entries('l_english:\n key:0 "A\nB"\n')[0][2], 'A\nB')


if __name__ == '__main__':
    unittest.main()
