{
	'name': "Facturas Cedible",
	'summary': "Facturas y recibos electronicos Cedible",
	'description': "Facturas y recibos electronicos Cedible",
	'author': "Indasoge",
    'website': "http://www.indasoge.com",
    'license': 'LGPL-3',
	'version': '18.0.0.1',
	'depends': ['base', 'account','l10n_cl','l10n_cl_edi'],
	'data': [
		'security/ir.model.access.csv',
		'views/template_cedible.xml',	
                                'views/template_cedible_inherit.xml',	
	],
	'installable': True,
	"sequence": 10,
}
