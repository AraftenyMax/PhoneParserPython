from src.utils import dump_csv, dump_json


SMFIELDS_SECTION_KEY = 'SimpleFields'
REQUIRED_SECTIONS = {
    'UrlResolveRules': ['PageLinkTemplate', ],
    'CheckXpaths': ['DetailLinkSelector', ]
}
AVAILABLE_DUMPS = {'json': dump_json, 'csv': dump_csv}
SPEC_SYMBOLS = ['\n', '\t', '\r']
