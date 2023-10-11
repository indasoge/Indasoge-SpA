{
    "name": "Smart analytics - Dashboard Frame",
    'version': '15.0',
    'category': 'Reporting',
    "summary": "Dashboards for Smart Analytics",
    'description': """
        This module allows the seamless integration of external dashboards in Odoo
    """,
    "author": "Idealis Consulting",
    'website': "https://idealisconsulting.com",
    "depends": ["base", 'web'],
    "license": "LGPL-3",
    "data": [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
        # Wizards
        'wizards/create_menu.xml',
        # Views
        'views/menuitems.xml',
        'views/smart_analytics_dashboard.xml',
    ],

    "installable": True,
    'assets': {
        'web.assets_backend': [
            'dashboard_frame/static/src/js/smart_analytics_form_renderer.js',
            'dashboard_frame/static/src/js/smart_analytics_form_view.js',
            'dashboard_frame/static/src/js/smart_analytics_url2iframe.js',
        ],
        'web.assets_frontend': [
            'dashboard_frame/static/src/js/smart_analytics_form_renderer.js',
            'dashboard_frame/static/src/js/smart_analytics_form_view.js',
            'dashboard_frame/static/src/js/smart_analytics_url2iframe.js',
        ],
        'web.assets_qweb': [
            'dashboard_frame/static/src/xml/smart_analytics.xml',
        ],
    }

}
