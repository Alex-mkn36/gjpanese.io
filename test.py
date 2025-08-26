import regex

text = "(Poster wo haru kara, heya ga kirei ni narimasu.) Because I put up a poster, the room becomes clean.ポスターを貼るから、部屋がきれいになります。"

# Extract only Japanese characters (Hiragana, Katakana, Kanji)
japanese_text = ''.join(regex.findall(r'[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}ー。、！？]', text))

print(japanese_text)
