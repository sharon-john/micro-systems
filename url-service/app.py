import url_shortener

shortener = url_shortener.URLShortener()
short_code = shortener.shorten("https://www.example.com/very/long/path")  # Returns something like "abc123"
print(short_code)
original_url = shortener.get_url(short_code) 
print(original_url)

short_code = shortener.shorten("https://www.example.com/very/long/path")
print(short_code)

short_code2 = shortener.shorten("https://www.something.com/very/long/path2")
print(short_code2)
print(shortener.get_url(short_code2))

short_code3 = shortener.shorten("https://www.something.com/very/long/path3")
print(short_code3)
print(shortener.get_url(short_code3))

print(shortener.get_url(short_code3))
print(shortener.get_url(short_code3))


print(shortener.get_top_urls(4))

shortener.get_url(short_code2)
print(shortener.get_top_urls(4))

shortener.get_url(short_code2)
print(shortener.get_top_urls(4))

shortener.get_url(short_code2)
shortener.get_url(short_code2)
shortener.get_url(short_code2)
print(shortener.get_top_urls(4))