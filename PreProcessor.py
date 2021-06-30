import re
stopwords = open('/content/gdrive/MyDrive/Subasa V3.0 /Notebooks/Data/StopWords_425.txt',encoding='utf16')
stopwords = [x.split('\t')[0] for x in stopwords.readlines()]

suffixes_list = open('/content/gdrive/MyDrive/Subasa V3.0 /Notebooks/Data/Suffixes-413.txt','r')
suffixes_list = [x.split('\n')[0] for x in suffixes_list.readlines()]

def remove_stop_words(tokenized_list_with_stop_words, stopwords):        
    tokenized_list_without_stop_words = []        
    for token in tokenized_list_with_stop_words:
        if not token in stopwords:
            tokenized_list_without_stop_words.append(token)
    return tokenized_list_without_stop_words

def stem_words(tokenized_list, suffixes_list):        
    for index_in_tokenized_list in range(0, len(tokenized_list)):
        possible_stems = []            
        for suffix in suffixes_list:
            token=tokenized_list[index_in_tokenized_list]
            if (len(token) > len(suffix)):                
                if (token[(-len(suffix)):] == suffix):
                    print(suffix)
                    possible_stems.append(token[:-len(suffix)])
            
        if (possible_stems != []):
            print(possible_stems)
            tokenized_list[index_in_tokenized_list] = min(possible_stems, key=len)
    
    return tokenized_list

def clean_data(data):

    # split the sentence from fullstop
    data=re.split(r'(?<=[a-zA-Z\u0D80-\u0DFF][\.\;\?\:])\s', data)
    
    for sentence in data:

        # pattern to filter URLs
        pattern_urls  = re.compile('http\S+')
        sentence = pattern_urls.sub('URL', sentence)

        # pattern to filter emails
        pattern_email  = re.compile('\S+@\S+')        
        sentence = pattern_email.sub('EMAIL', sentence)

        # pattern to filter non-alphanumeric characters using unicode
        pattern_non_alphanumeric = re.compile(u'[^\u0061-\u007A | ^\u0041-\u005A | ^\u0D80-\u0DFF | ^\u0030-\u0039]', re.UNICODE)
        sentence = pattern_non_alphanumeric.sub(' ', sentence) 
        
        # pattern to detect HTML tags
        pattern_html  = re.compile('/<([a-z]*)\b[^>]*>(.*?)</\1>/i')
        sentence = pattern_html.sub(' ', sentence)

        # pattern to detect numbers
        pattern_numbers = re.compile('\d+')
        sentence = pattern_numbers.sub('NUM', sentence)
        
        yield sentence
