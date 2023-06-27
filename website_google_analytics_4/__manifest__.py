# Copyright © 2021 Garazd Creation (https://garazd.biz)
# @author: Yurii Razumovskyi (support@garazd.biz)
# @author: Iryna Razumovska (support@garazd.biz)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

# flake8: noqa: E501

{
    'name': 'Google Analytics 4 Global Site Tag (gtag.js)',
    'version': '15.0.2.1.0',
    'category': 'Website',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz/shop',
    'license': 'LGPL-3',
    'summary': 'Google Analytics 4 Global Site Tag (gtag.js) | GA4 integration | Login and Sign Up events',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'live_test_url': 'https://garazd.biz/r/Ikz',
    'depends': [
        'website',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/website_templates.xml',
    ],
    'external_dependencies': {
    },
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
