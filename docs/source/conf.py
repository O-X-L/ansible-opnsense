from datetime import datetime

# pylint: disable=W0622

project = 'Ansible Collection - OPNSense'
copyright = f'{datetime.now().year}, AnsibleGuy'
author = 'AnsibleGuy'
extensions = ['piccolo_theme', 'myst_parser']
templates_path = ['_templates']
exclude_patterns = ['_tmpl/*.rst', '_cp/*.rst']
html_theme = 'piccolo_theme'
html_static_path = ['_static']
html_logo = 'https://files.oxl.at/logos/opnsense.png'
html_favicon = '_static/img/favicon.ico'
html_js_files = ['https://files.oxl.at/js/feedback.js']
html_css_files = ['css/main.css', 'https://files.oxl.at/css/feedback.css']
master_doc = 'index'
display_version = True
sticky_navigation = True
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
html_theme_options = {
    'banner_text': '<a href="https://github.com/ansibleguy/collection_opnsense">Repository on GitHub</a> | '
                   '<a href="https://github.com/ansibleguy/collection_opnsense/issues/new/choose">Report Errors</a> | '
                   '<a href="https://www.o-x-l.com">Get Support</a>'
}
html_short_title = 'Ansible OPNSense'
