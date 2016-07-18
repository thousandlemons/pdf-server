import re
import string

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


def replace_known(m_string):
    for pair in KNOWN_REPLACEMENTS:
        m_string = m_string.replace(pair[0], pair[1])
    return m_string


def replace_non_ascii(m_string):
    return re.sub(r'[^\x00-\x7F]', '', m_string)


def remove_multiple_newline(m_string):
    return re.sub(r'\n\s*\n', '\n', m_string)


def remove_multiple_whitespace(m_string):
    return re.sub(r'\s+', ' ', m_string).strip()


def remove_digits(m_string):
    return re.sub(r'\d*', '', m_string)


def remove_single_letter_words(m_string):
    return re.sub(r'\W*\b\w\b', ' ', ' ' + m_string + ' ').strip()


def remove_two_letter_words(m_string):
    return re.sub(r'\W*\b\w{2}\b', ' ', ' ' + m_string + ' ').strip()


def remove_stop_words(m_string):
    m_string = (' ' + m_string + ' ').lower()
    for word in CUSTOMIZED_STOP_WORDS:
        m_string = re.sub(r'\W' + word + '\W', ' ', m_string)
    return m_string.strip()


def remove_uri(m_string):
    return re.sub(
        r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]))',
        '', m_string
    )


def remove_email(m_string):
    return re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '', m_string)


def remove_punctuation_marks(m_string):
    r = re.compile(r'[\s{}]+'.format(re.escape(string.punctuation)))
    return r.sub(' ', m_string).strip()


def lemmatize(m_string):
    lemmatizer = WordNetLemmatizer()
    return ' '.join(lemmatizer.lemmatize(word) for word in m_string.split())


class Cleaner:
    methods = [
        replace_known,
        replace_non_ascii,
        remove_uri,
        remove_email,
        remove_stop_words,
        remove_punctuation_marks,
        remove_digits,
        remove_single_letter_words,
        remove_two_letter_words,
        remove_multiple_whitespace,
        remove_multiple_newline,
        lemmatize
    ]

    def set_methods(self, methods):
        self.methods = methods

    def add_method(self, method):
        self.methods.append(method)

    def add_methods(self, methods):
        self.methods.extend(methods)

    def clean(self, m_string):
        result = m_string
        for method in self.methods:
            result = method(result)
        return result
