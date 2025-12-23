# String field max lengths
MAX_LENGTH_TITLE = 255
MAX_LENGTH_NAME = 100
MAX_LENGTH_SLUG = 100
MAX_LENGTH_USERNAME = 150
MAX_LENGTH_EMAIL = 254

# Database choices
ARTICLE_STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('archived', 'Archived'),
]

# Pagination
DEFAULT_PAGE_SIZE = 20

# Common defaults
DEFAULT_LANGUAGE = 'en'
DEFAULT_TIMEZONE = 'UTC'
