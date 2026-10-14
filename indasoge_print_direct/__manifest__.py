{
    "name": "Indasoge Print Direct",
    "version": "19.0.2.5",
    "category": "Printer",
    "summary": """Print any report or shipping label or barcode label directly to any local (usb, wifi, bluetooth, network) printer without downloading PDF""",
    "author": "Indasoge",
    "website": "https://www.indasoge.com",
    "license": "OPL-1",
    "price": 50.00,
    "currency": "USD",
    "depends": [
        # Odoo
        'base',
        'web',
    ],
    "data": [
        # Views
        'views/ir_actions_report.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "indasoge_print_direct/static/lib/print.min.js",
            "indasoge_print_direct/static/lib/print.min.css",
            "indasoge_print_direct/static/src/js/browser_print_dialog.js",
        ],
        "web.assets_qweb": [],
    },
    "images": ['static/description/banner.gif'],
    "installable": True,
    "application": True,
}
