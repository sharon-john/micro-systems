import random 

class URLShortener:
    # shortened codes must be 6 characters long: (a-z),(A-Z), (0-9)
    lowercase_min_range = ord('a')
    lowercase_max_range = ord('z')

    uppercase_min_range = ord('A')
    uppercase_max_range = ord('Z')

    numeric_min_range, numeric_max_range = 0, 9

    top_urls = []

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
        if n > len(self.short_code_mapping):
            n = len(self.short_code_mapping)

        if self.top_urls == []:
            num_urls = len(self.short_code_mapping)
            if n > num_urls:
                n = num_urls 
            
            self.top_urls = [ (self.short_code_mapping[elem][0], elem, self.short_code_mapping[elem][1]) for elem in sorted(self.short_code_mapping, key = lambda x: self.short_code_mapping[x][1], reverse=True) ]

        return self.top_urls[0:n]
    
    def resort_top_urls(self, updated_url):
        # can only resort if it's already sorted 
        if self.top_urls == []:
            self.get_top_urls(len(self.url_mapping))
        
        # implement linear search here to find where the updated access count goes and then reorder rest of top_urls  

        # left shift by 1 
        curr_index = -1
        new_index = -1 
        for i in range(len(self.top_urls)):
            if self.top_urls[i][0] == updated_url[0]:
                curr_index = i 
                break 

        for i in range(len(self.top_urls)):
            if self.top_urls[i][2] < updated_url[1] and self.top_urls[i][0] != updated_url[0]:
                new_index = i 
                break 
        
        # first delete old index, then right shift by 1 starting at new_index + 1 
        curr_url_entry = self.top_urls[curr_index]
        curr_url_entry = (curr_url_entry[0], curr_url_entry[1], updated_url[1])

        del self.top_urls[curr_index]
        self.top_urls.append(0)

        for i in range(len(self.top_urls)-1, new_index, -1):
            self.top_urls[i] = self.top_urls[i-1]
        
        self.top_urls[new_index] = curr_url_entry

    def get_url(self, short_code):
        url_and_access_count = self.short_code_mapping.get(short_code, -1)
        if url_and_access_count == -1:
            raise KeyError
        
        url, access_count = url_and_access_count[0], url_and_access_count[1] + 1 

        self.short_code_mapping[short_code] = (url, access_count)
        
        if self.top_urls != []:
            self.resort_top_urls(self.short_code_mapping[short_code])

        return url






