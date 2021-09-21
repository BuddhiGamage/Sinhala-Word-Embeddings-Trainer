import re
import sys
import resources

class PreProcessor:
    def __init__(self,url_repl='', email_repl='', phone_repl='', num_repl='', date_repl='', emoji_repl='', html_tag_repl=''):
        self.url_repl = url_repl
        self.email_repl = email_repl
        self.phone_repl = phone_repl
        self.date_repl = date_repl
        self.num_repl = num_repl
        self.emoji_repl = emoji_repl
        self.html_tag_repl = html_tag_repl

        self._preprocess =[]
        self._init_preprocess()
    
    def _preprocess_email(self,input_text,email_repl):
        return resources.RE_EMAIL.sub(email_repl,input_text)
        
    def _preprocess_phone_numbers(self,input_text,phone_repl):
        return resources.RE_PHONE_NUMBER.sub(phone_repl,input_text)
        
    
    def _preprocess_dates(self,input_text,date_repl): 
        return resources.RE_DATES.sub(date_repl,input_text)

    def _preprocess_numbers(self,input_text,num_repl):
        return resources.RE_NUMBER.sub(num_repl,input_text)
    

    def _preprocess_emoji(self,input_text,emoji_repl):
        return resources.RE_EMOJI.sub(emoji_repl,input_text)


    def _preprocess_html_tags(self,input_text,html_tag_repl):
        return resources.RE_HTML.sub(html_tag_repl,input_text)
        

    def _preprocess_url(self,input_text,url_repl):
        return resources.RE_URL.sub(url_repl, input_text)

    def _init_preprocess(self):
        if self.url_repl is not None:
            self._preprocess.append((self._preprocess_url, self.url_repl))
        if self.email_repl is not None:
            self._preprocess.append((self._preprocess_email, self.email_repl))
        if self.phone_repl is not None:
            self._preprocess.append((self._preprocess_phone_numbers, self.phone_repl))
        if self.date_repl is not None:
            self._preprocess.append((self._preprocess_dates, self.date_repl))
        if self.num_repl is not None:
            self._preprocess.append((self._preprocess_numbers, self.num_repl))
        if self.emoji_repl is not None:
            self._preprocess.append((self._preprocess_emoji, self.emoji_repl))
        if self.html_tag_repl is not None:
            self._preprocess.append((self._preprocess_html_tags, self.html_tag_repl))  
        
    def preprocess(self,input_text):
        for preprocess_fn, repl in self._preprocess:
            input_text = preprocess_fn(input_text,repl)
        return input_text

