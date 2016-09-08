import re

from nltk.stem import WordNetLemmatizer

MYSQL_STOP_WORDS = [
    "a", 'able', 'about', 'above', 'according', 'accordingly', 'across', 'actually', 'after',
    'afterwards', 'again', 'against', "ain't", 'all', 'allow', 'allows', 'almost', 'alone', 'along',
    'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'another', 'any',
    'anybody', 'anyhow', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'appear',
    'appreciate', 'appropriate', 'are', "aren't", 'around', 'as', 'aside', 'ask', 'asking',
    'associated', 'at', 'available', 'away', 'awfully', 'be', 'became', 'because', 'become', 'becomes',
    'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'believe', 'below', 'beside',
    'besides', 'best', 'better', 'between', 'beyond', 'both', 'brief', 'but', 'by', "c'mon", "c's",
    'came', 'can', "can't", 'cannot', 'cant', 'cause', 'causes', 'certain', 'certainly', 'changes',
    'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently', 'consider', 'considering',
    'contain', 'containing', 'contains', 'corresponding', 'could', "couldn't", 'course', 'currently',
    'definitely', 'described', 'despite', 'did', "didn't", 'different', 'do', 'does', "doesn't",
    'doing', "don't", 'done', 'down', 'downwards', 'during', 'each', 'edu', 'eg', 'eight', 'either',
    'else', 'elsewhere', 'enough', 'entirely', 'especially', 'et', 'etc', 'even', 'ever', 'every',
    'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly', 'example', 'except', 'far',
    'few', 'fifth', 'first', 'five', 'followed', 'following', 'follows', 'for', 'former', 'formerly',
    'forth', 'four', 'from', 'further', 'furthermore', 'get', 'gets', 'getting', 'given', 'gives', 'go',
    'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'had', "hadn't", 'happens', 'hardly', 'has',
    "hasn't", 'have', "haven't", 'having', 'he', "he's", 'hello', 'help', 'hence', 'her', 'here',
    "here's", 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'hi', 'him', 'himself',
    'his', 'hither', 'hopefully', 'how', 'howbeit', 'however', "i'd", "i'll", "i'm", "i've", 'ie', 'if',
    'ignored', 'immediate', 'in', 'inasmuch', 'inc', 'indeed', 'indicate', 'indicated', 'indicates',
    'inner', 'insofar', 'instead', 'into', 'inward', 'is', "isn't", 'it', "it'd", "it'll", "it's",
    'its', 'itself', 'just', 'keep', 'keeps', 'kept', 'know', 'known', 'knows', 'last', 'lately',
    'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', "let's", 'like', 'liked', 'likely',
    'little', 'look', 'looking', 'looks', 'ltd', 'mainly', 'many', 'may', 'maybe', 'me', 'mean',
    'meanwhile', 'merely', 'might', 'more', 'moreover', 'most', 'mostly', 'much', 'must', 'my',
    'myself', 'name', 'namely', 'nd', 'near', 'nearly', 'necessary', 'need', 'needs', 'neither',
    'never', 'nevertheless', 'new', 'next', 'nine', 'no', 'nobody', 'non', 'none', 'noone', 'nor',
    'normally', 'not', 'nothing', 'novel', 'now', 'nowhere', 'obviously', 'of', 'off', 'often', 'oh',
    'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others',
    'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own',
    'particular', 'particularly', 'per', 'perhaps', 'placed', 'please', 'plus', 'possible',
    'presumably', 'probably', 'provides', 'que', 'quite', 'qv', 'rather', 'rd', 're', 'really',
    'reasonably', 'regarding', 'regardless', 'regards', 'relatively', 'respectively', 'right', 'said',
    'same', 'saw', 'say', 'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed',
    'seeming', 'seems', 'seen', 'self', 'selves', 'sensible', 'sent', 'serious', 'seriously', 'seven',
    'several', 'shall', 'she', 'should', "shouldn't", 'since', 'six', 'so', 'some', 'somebody',
    'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry',
    'specified', 'specify', 'specifying', 'still', 'sub', 'such', 'sup', 'sure', "t's", 'take',
    'taken', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', "that's", 'thats',
    'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', "there's", 'thereafter',
    'thereby', 'therefore', 'therein', 'theres', 'thereupon', 'these', 'they', "they'd", "they'll",
    "they're", "they've", 'think', 'third', 'this', 'thorough', 'thoroughly', 'those', 'though',
    'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'took', 'toward',
    'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'twice', 'two', 'un', 'under',
    'unfortunately', 'unless', 'unlikely', 'until', 'unto', 'up', 'upon', 'us', 'use', 'used', 'useful',
    'uses', 'using', 'usually', 'value', 'various', 'very', 'via', 'viz', 'vs', 'want', 'wants', 'was',
    "wasn't", 'way', 'we', "we'd", "we'll", "we're", "we've", 'welcome', 'well', 'went', 'were',
    "weren't", 'what', "what's", 'whatever', 'when', 'whence', 'whenever', 'where', "where's",
    'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while',
    'whither', 'who', "who's", 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'willing', 'wish',
    'with', 'within', 'without', "won't", 'wonder', 'would', "wouldn't", 'yes', 'yet', 'you', "you'd",
    "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves', 'zero']

CUSTOMIZED_STOP_WORDS = MYSQL_STOP_WORDS + [
    'chapter', 'figure', 'diagram', 'system'
]

KNOWN_REPLACEMENTS = [
    ('ﬁ', 'fi'),
    ('ﬀ', 'ff'),
    ('ﬂ', 'fl'),
    ('ﬃ', 'ffi'),
    ('ﬄ', 'ffl')
]


def replace_known(text):
    for pair in KNOWN_REPLACEMENTS:
        text = text.replace(pair[0], pair[1])
    return text


def fix_line_join(text):
    return re.sub(r'\b- \b', '', text)


def remove_extra_newline_space(text):
    if len(text) > 0 and text[0] == '\n':
        text = text[1:]
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'(?:\n|\r|\r\n?)+', '\n', text)
    text = '\n'.join(line.strip() for line in text.splitlines())
    return text


def remove_duplicate_lines(text):
    lines = text.splitlines()
    cleaned = []
    line_set = set()
    for line in lines:
        if line not in line_set:
            cleaned.append(line)
            line_set.add(line)
    return '\n'.join(cleaned)


def remove_lines_without_words_longer_than_3(text):
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        if re.search('[a-zA-Z]{4,}', line):
            cleaned.append(line)
    return '\n'.join(cleaned)


def remove_lines_with_no_space(text):
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        if ' ' in line:
            cleaned.append(line)
    return '\n'.join(cleaned)


def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]', '', text)


def remove_digits(text):
    return re.sub(r'\d+', ' ', text)


def remove_one_letter_words(text):
    return re.sub(r'\b[a-zA-Z]\b', ' ', text)


def remove_two_letter_words(text):
    return re.sub(r'\b[a-zA-Z]{2}\b', ' ', text)


def remove_stop_words(text):
    for word in MYSQL_STOP_WORDS:
        text = re.sub(r'\b{word}\b'.format(word=word), '', text, flags=re.IGNORECASE)
    return text


def remove_uri(text):
    return re.sub(
        r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]))',
        '', text
    )


def remove_email(text):
    return re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '', text)


def remove_punctuation_marks(text):
    return re.sub(r'[^\w\s]', ' ', text)


def lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    return ' '.join(lemmatizer.lemmatize(word) for word in text.split())


class Cleaner:
    methods = [
        replace_known,
        fix_line_join,
        remove_extra_newline_space,
        remove_lines_without_words_longer_than_3,
        remove_lines_with_no_space,
        remove_duplicate_lines,
    ]

    def set_methods(self, methods):
        self.methods = methods

    def add_method(self, method):
        self.methods.append(method)

    def add_methods(self, methods):
        self.methods.extend(methods)

    def clean(self, text):
        for method in self.methods:
            text = method(text)
        return text
