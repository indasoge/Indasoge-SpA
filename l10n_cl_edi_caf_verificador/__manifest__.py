{
    'name': 'Verificador de Folios CAF (Chile)',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Añade validación y verificación de folios libres para CAFs en Chile.',
    'author': 'Leonee',
    'depends': ['l10n_cl_edi', 'mail'], 
    'data': [
        'views/caf_view.xml',
        'data/cron_caf.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
