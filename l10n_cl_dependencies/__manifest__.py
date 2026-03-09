# -*- coding: utf-8 -*-
{
    'name': "l10n_cl_dependencies",

    'summary': """
        Add External depency on pdf417gen for migrations""",

    'description': """
        Add External depency on pdf417gen for migrations
    """,

    'author': "Indasoge SpA",
    'website': "http://www.indasoge.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
  
    'version': '0.5',


    # any module necessary for this one to work correctly
    'depends': ['base'],

    # external depency on pdf417gen
    'external_dependencies': {'python': ['pdf417gen']},

    'license': 'OPL-1',
}
