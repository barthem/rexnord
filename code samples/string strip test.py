
unicode_line = b"\x00{\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
print(unicode_line)
unicode_line = str(unicode_line)


translation_table = dict.fromkeys(map(ord, '\\x0'), None)
unicode_line = unicode_line.translate(translation_table)

print(bytes(unicode_line))