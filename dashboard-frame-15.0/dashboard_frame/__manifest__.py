{
    "name": "Smart analytics - Dashboard Frame",
    "version": "18.0.1.0",
    "category": "Reporting",
    "summary": "Dashboards for Smart Analytics",
    "description": """
        This module allows the seamless integration of external dashboards in Odoo
    """,
    "author": "Idealis Consulting",
    "website": "https://idealisconsulting.com",
    "depends": ["base", "web", "mail"],
    "license": "LGPL-3",
    "data": [
        # Security
        "security/ir_rule.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        # Views
        "views/menuitems.xml",
        "views/smart_analytics_dashboard.xml",
        # Wizard
        "wizards/dashboard_email_wizard.xml",
        "wizards/dashboard_create_menu_wizard.xml",
        # Data
        "data/dashboard_mail_template.xml",
    ],
    "installable": True,
    "assets": {
        "web.assets_backend":
            ["dashboard_frame/static/src/***/**/*",]
    },
}
