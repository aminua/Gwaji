# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Remita Payment Gateway',
    'version': '1.0',
    'category': 'Accounting/Payment',
    'description': """
        Remita Payment Gateway integration for Odoo.
    """,
    'summary': 'Remita Payment Gateway integration',
    'author': 'Dr. Aminu Abubakar',
    'depends': ['payment', 'website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
