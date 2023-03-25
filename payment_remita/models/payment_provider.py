# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

import requests
from werkzeug.urls import url_join

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.payment_remita.const import SUPPORTED_CURRENCIES


_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('remita', "remita")], ondelete={'remita': 'set default'}
    )
    remita_public_key = fields.Char(
        string="remita Public Key",
        help="The key solely used to identify the account with remita.",
        required_if_provider='remita',
    )
    remita_secret_key = fields.Char(
        string="remita Secret Key",
        required_if_provider='remita',
        groups='base.group_system',
    )
    remita_webhook_secret = fields.Char(
        string="remita Webhook Secret",
        required_if_provider='remita',
        groups='base.group_system',
    )

    #=== COMPUTE METHODS ===#

    def _compute_feature_support_fields(self):
        """ Override of `payment` to enable additional features. """
        super()._compute_feature_support_fields()
        self.filtered(lambda p: p.code == 'remita').update({
            'support_tokenization': True,
        })

    # === BUSINESS METHODS ===#

    @api.model
    def _get_compatible_providers(self, *args, currency_id=None, is_validation=False, **kwargs):
        """ Override of payment to filter out remita providers for unsupported currencies or
        for validation operations. """
        providers = super()._get_compatible_providers(
            *args, currency_id=currency_id, is_validation=is_validation, **kwargs
        )

        currency = self.env['res.currency'].browse(currency_id).exists()
        if (currency and currency.name not in SUPPORTED_CURRENCIES) or is_validation:
            providers = providers.filtered(lambda p: p.code != 'remita')

        return providers

    def _remita_make_request(self, endpoint, payload=None, method='POST'):
        """ Make a request to remita API at the specified endpoint.

        Note: self.ensure_one()

        :param str endpoint: The endpoint to be reached by the request.
        :param dict payload: The payload of the request.
        :param str method: The HTTP method of the request.
        :return The JSON-formatted content of the response.
        :rtype: dict
        :raise ValidationError: If an HTTP error occurs.
        """
        self.ensure_one()

        url = url_join('https://api.remita.com/v3/', endpoint)
        headers = {'Authorization': f'Bearer {self.remita_secret_key}'}
        try:
            if method == 'GET':
                response = requests.get(url, params=payload, headers=headers, timeout=10)
            else:
                response = requests.post(url, json=payload, headers=headers, timeout=10)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url, pprint.pformat(payload),
                )
                raise ValidationError("remita: " + _(
                    "The communication with the API failed. remita gave us the following "
                    "information: '%s'", response.json().get('message', '')
                ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "remita: " + _("Could not establish the connection to the API.")
            )
        return response.json()
