from datetime import datetime

# pylint: disable=W0622

project = 'Ansible Collection - OPNsense'
author = 'OXL IT Services'
copyright = f'{datetime.now().year}, {author}'
extensions = ['sphinx_immaterial', 'myst_parser']
templates_path = ['_templates']
exclude_patterns = ['_tmpl/*.rst', '_cp/*.rst']
html_theme = 'sphinx_immaterial'
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
    # 'banner_text': '<a href="https://github.com/O-X-L/ansible_opnsense">Repository on GitHub</a> | '
    #                '<a href="https://github.com/O-X-L/ansible_opnsense/issues/new/choose">Report Errors</a> | '
    #                '<a href="https://www.o-x-l.com">Get Support</a>'
    "site_url": "https://ansible-opnsense.oxl.app",
    "repo_url": "https://github.com/O-X-L/ansible-opnsense",
    "repo_name": "OPNsense Ansible Community-Collection (by OXL)",
    "globaltoc_collapse": True,
    "features": [
        "navigation.expand",
        # "navigation.tabs",
        # "navigation.tabs.sticky",
        # "toc.integrate",
        "navigation.sections",
        # "navigation.instant",
        # "header.autohide",
        "navigation.top",
        "navigation.footer",
        # "navigation.tracking",
        # "search.highlight",
        "search.share",
        "search.suggest",
        "toc.follow",
        "toc.sticky",
        "content.tabs.link",
        "content.code.copy",
        "content.action.edit",
        "content.action.view",
        "content.tooltips",
        "announce.dismiss",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "light-blue",
            "accent": "light-green",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to dark-mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "deep-orange",
            "accent": "lime",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to light-mode",
            },
        },
    ],
    "version_dropdown": True,
    "version_info": [
        {
            "version": "https://www.O-X-L.com",
            "title": "About OXL",
            "aliases": [],
        },
    ],
    "social": [
        {
            "icon": "fontawesome/solid/globe",
            "link": "https://www.O-X-L.com",
            "name": "About OXL",
        },
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/O-X-L",
            "name": "OXL on GitHub",
        },
    ],
}
html_title = 'OPNsense Ansible'
html_short_title = 'OPNsense Ansible Collection (Community)'
