{
    "name": "Smart analytics - Dashboard Frame",
    'version': '18.0.0.0',
    'category': 'Reporting',
    "summary": "Dashboards for Smart Analytics",
    'description': """
        This module allows the seamless integration of external dashboards in Odoo
    """,
    "author": "Idealis Consulting",
    'website': "https://idealisconsulting.com",
    "depends": ["base", 'web', 'mail'],
    "license": "LGPL-3",
    "data": [
        # Security
        'security/ir_rule.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        # Views
        'views/menuitems.xml',
        'views/smart_analytics_dashboard.xml',
    ],

    "installable": True,
    'assets': {
        'web.assets_backend': [
            'dashboard_frame/static/src/js/smart_analytics_form_renderer.js',
            'dashboard_frame/static/src/xml/smartanalytics_dashboard_kanban.xml',
            'dashboard_frame/static/src/css/smartanalytics.css',
        ]
    }
}
