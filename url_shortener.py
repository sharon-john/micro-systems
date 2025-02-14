import random 

class URLShortener:
    # shortened codes must be 6 characters long: (a-z),(A-Z), (0-9)
    lowercase_min_range = ord('a')
    lowercase_max_range = ord('z')

    uppercase_min_range = ord('A')
    uppercase_max_range = ord('Z')

    numeric_min_range, numeric_max_range = 0, 9

    def __init__(self):
        self.url_mapping = dict()
        self.short_code_mapping = dict()

    def _generate_short_code(self):
        short_code = ""
        gen_first_three_chars = 0
        while (gen_first_three_chars != 3): 
            candidates = []
            candidates.append(random.randint(self.lowercase_min_range, self.lowercase_max_range))
            candidates.append(random.randint(self.uppercase_min_range, self.uppercase_max_range))

            char_ord = candidates[random.randint(0,1)]

            short_code += chr(char_ord)
            gen_first_three_chars += 1 

        gen_last_three_chars = 0
        while (gen_last_three_chars != 3):
            num = random.randint(self.numeric_min_range, self.numeric_max_range)
            short_code += str(num)
            gen_last_three_chars += 1 
        
        return short_code

    def shorten(self, url):
        if url in self.url_mapping:
            return self.url_mapping[url]

        short_code = ""
        while (len(short_code) < 6 or short_code in self.short_code_mapping):
            short_code = self._generate_short_code()
        
        self.url_mapping[url] = short_code
        self.short_code_mapping[short_code] = (url, 0) 
        return short_code  
    
    def get_top_urls(self, n):
        num_urls = len(self.short_code_mapping)
        if n > num_urls:
            n = num_urls 
        
        res = [ (self.short_code_mapping[elem][0], elem, self.short_code_mapping[elem][1]) for elem in sorted(self.short_code_mapping, key = lambda x: self.short_code_mapping[x][1], reverse=True) ]

        return res[0:n]

    def get_url(self, short_code):
        url_and_access_count = self.short_code_mapping.get(short_code, -1)
        if url_and_access_count == -1:
            raise KeyError
        
        url, access_count = url_and_access_count[0], url_and_access_count[1] + 1 

        self.short_code_mapping[short_code] = (url, access_count)
        return url

shortener = URLShortener()
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

