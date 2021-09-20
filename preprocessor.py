import re
import sys

class PreProcessor:
  def __init__(self,url_repl='', email_repl='', phone_repl='', num_repl='', date_repl='', emoji_repl='', html_tag_repl=''):
    self.url_repl = url_repl
    self.email_repl = email_repl
    self.phone_repl = phone_repl
    self.date_repl = date_repl
    self.num_repl = num_repl
    self.emoji_repl = emoji_repl
    self.html_tag_repl = html_tag_repl

    self._preProccess =[]
    self._init_preProccess()
    
  def _preprocess_email(self,input_text,email_repl):
    regex_pattern = re.compile(
        r"(?:mailto:)?"
        r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(\.([a-z]{2,})){1,3}"
        r"(?:$|(?=\b))",
        flags=re.IGNORECASE,)
    text= regex_pattern.sub(email_repl,input_text)
    return text

  def _preprocess_phone_numbers(self,input_text,phone_repl):
    # for more information: https://github.com/jfilter/clean-text/issues/10
    regex_pattern = re.compile(r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))")
    #regex_pattern= re.compile(r"((?:^|(?<=[^\w)]))(((\+?[01])|(\+\d{2}))[ .-]?)?(\(?\d{3,4}\)?/?[ .-]?)?(\d{3}[ .-]?\d{4})(\s?(?:ext\.?|[#x-])\s?\d{2,6})?(?:$|(?=\W)))|\+?\d{4,5}[ .-/]\d{6,9}")
    text = regex_pattern.sub(phone_repl,input_text)
    return text
 
  def _preprocess_dates(self,input_text,date_repl): 
    regex_pattern = re.compile(r"(\d{4}(.|-|\/)(0[1-9]|1[0-2])(.|-|\/)(0[1-9]|[12][0-9]|3[01]))|(([1-9]|1[0-9]|2[0-9]|3[0-1]|0[0-9])(.|-|\/)([1-9]|1[0-2]|0[0-9])(.|-|\/)(\d{4}))")
    text = regex_pattern.sub(date_repl,input_text)
    return text

  def _preprocess_numbers(self,input_text,num_repl):
    regex_pattern = re.compile(r"(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))")
    text= regex_pattern.sub(num_repl,input_text)
    return text

  def _preprocess_emoji(self,input_text,emoji_repl):
    # https://gist.github.com/Alex-Just/e86110836f3f93fe7932290526529cd1
    regex_pattern = re.compile(
        "(["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "])"
      )
    text= regex_pattern.sub(emoji_repl,input_text)
    return text

  def _preprocess_html_tags(self,input_text,html_tag_repl):
    regex_pattern = re.compile(r"<[^>]*>")
    text= regex_pattern.sub(html_tag_repl,input_text)
    return text

  def _preprocess_url(self,input_text,url_repl):
    regex_pattern = re.compile(
        r"(?:^|(?<![\w/.]))"
        # protocol identifier
        # r"(?:(?:https?|ftp)://)"  <-- alt?
        r"(?:(?:https?://|ftp://|www\d{0,3}\.))"
        # user:pass authentication
        r"(?:\S+(?::\S*)?@)?"
        r"(?:"
        # IP address exclusion
        # private & local networks
        r"(?!(?:10|127)(?:\.\d{1,3}){3})"
        r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
        r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
        # IP address dotted notation octets
        # excludes loopback network 0.0.0.0
        # excludes reserved space >= 224.0.0.0
        # excludes network & broadcast addresses
        # (first & last IP address of each class)
        r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
        r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
        r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
        r"|"
        # host name
        r"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
        # domain name
        r"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
        # TLD identifier
        r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
        r")"
        # port number
        r"(?::\d{2,5})?"
        # resource path
        r"(?:/\S*)?"
        r"(?:$|(?![\w?!+&/]))",
        flags=re.IGNORECASE,)
    return regex_pattern.sub(url_repl, input_text)

  def _init_preProccess(self):
    if self.url_repl is not None:
      self._preProccess.append((self._preprocess_url, self.url_repl))
    if self.email_repl is not None:
      self._preProccess.append((self._preprocess_email, self.email_repl))
    if self.phone_repl is not None:
      self._preProccess.append((self._preprocess_phone_numbers, self.phone_repl))
    if self.date_repl is not None:
      self._preProccess.append((self._preprocess_dates, self.date_repl))
    if self.num_repl is not None:
      self._preProccess.append((self._preprocess_numbers, self.num_repl))
    if self.emoji_repl is not None:
      self._preProccess.append((self._preprocess_emoji, self.emoji_repl))
    if self.html_tag_repl is not None:
      self._preProccess.append((self._preprocess_html_tags, self.html_tag_repl))  
        
  def preProccess(self,input_text):
    #print(self._preProccess)
    for preProccess_fn, repl in self._preProccess:
      input_text = preProccess_fn(input_text,repl)
    return input_text


if __name__ == "__main__":
    P = PreProcessor(url_repl='[URL]', email_repl='[EMAIL]', phone_repl='[TEL]',date_repl='[DATE]',num_repl ='[NUM]', emoji_repl='[EMOJI]')
    example ="කොළඹ ගිය පියල් ඇතැම් විට ගමට එන්නේ සතියකට වරකි. ashmari@gmail.com, https://github.com/  2021.02.12 00254 😀 2021-02-23 12.01.1996  <?>"
    out = P.preProccess(example)
    print(out)
