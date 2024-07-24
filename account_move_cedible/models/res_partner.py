# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import requests

import logging

_logger = logging.getLogger(__name__)
