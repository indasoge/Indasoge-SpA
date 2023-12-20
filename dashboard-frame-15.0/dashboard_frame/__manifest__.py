{
    "name": "Smart analytics - Dashboard Frame",
    'version': '16.0',
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
            'dashboard_frame/static/src/**/*']
    }
}