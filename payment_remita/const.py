# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Last seen online: 24 November 2022.
SUPPORTED_CURRENCIES = [
    'GBP',
    'CAD',
    'CLP',
    'COP',
    'EGP',
    'EUR',
    'GHS',
    'GNF',
    'KES',
    'MWK',
    'MAD',
    'NGN',
    'RWF',
    'SLL',
    'STD',
    'ZAR',
    'TZS',
    'UGX',
    'USD',
    'XAF',
    'XOF',
    'ZMW',
]


# Mapping of transaction states to remita payment statuses.
PAYMENT_STATUS_MAPPING = {
    'pending': ['pending auth'],
    'done': ['successful'],
    'cancel': ['cancelled'],
    'error': ['failed'],
}
