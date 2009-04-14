# Django settings for cbc_website project.
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'django_esv_tests.db'
 
INSTALLED_APPS = [
    'esv',
    'core', 
]
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
)
