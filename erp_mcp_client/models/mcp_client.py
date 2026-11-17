import logging

import requests

from odoo import _, fields, models, api
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class McpClient(models.Model):
    _name = "erp.mcp.client"
    _description = "ERP MCP Client Registration"
    _order = "create_date desc"

    name = fields.Char(string="Registration Name", required=True)

    registrar_url = fields.Char(
        string="Registrar URL",
        required=True,
        help="Base URL of the ERP MCP registrar (the Odoo running erp_mcp_handler).",
        default='https://mcp.erpswiss.com/mcp/register',
    )

    odoo_url = fields.Char(string="Odoo URL", required=True, default= lambda self: self.env["ir.config_parameter"].sudo().get_param("web.base.url"))
    odoo_db = fields.Char(string="Odoo Database", required=True, default=lambda self: self.env.cr.dbname)
    odoo_login = fields.Char(string="Odoo Login / User")
    odoo_api_key = fields.Char(string="Odoo API Key")

    use_google_oauth = fields.Boolean(
        string="Use Google OAuth",
        default=True,
        help="Enable to let users sign in to the MCP with their Google account. "
             "Requires a Google OAuth Client ID and Secret. When disabled, the "
             "AI client connects with an access token instead.",
    )
    auth_method = fields.Selection(
        selection=[
            ("google_oauth", "Google OAuth"),
            ("access_token", "Access Token"),
        ],
        string="Authentication",
        compute="_compute_auth_method",
    )
    google_client_id = fields.Char(string="Google Client ID")
    google_client_secret = fields.Char(string="Google Client Secret")

    odoo_admin_emails = fields.Char(
        string="Admin Emails",
        help="Comma-separated Google emails granted the 'admin' role (they act "
             "as the Odoo user behind the API Key above). Put here the email(s) "
             "you log into the MCP with so you get access after registering.",
    )
    odoo_admin_access_tokens = fields.Char(
        string="Admin Access Tokens",
        help="Comma-separated static Bearer tokens granted the 'admin' role "
             "(Authorization: Bearer <token>) — lets a non-interactive client "
             "call the MCP without a Google login.",
    )
    role_ids = fields.One2many(
        comodel_name="erp.mcp.client.role",
        inverse_name="client_id",
        string="Access Roles",
        help="Extra Odoo users to expose as MCP roles. Each maps a set of "
             "Google emails to that Odoo user's API key.",
    )

    tenant_uuid = fields.Char(string="Tenant UUID", readonly=True, copy=False)
    mcp_url = fields.Char(string="MCP URL", readonly=True, copy=False)
    mcp_ai_url = fields.Char(string="AI Connector URL", readonly=True, copy=False, compute="_compute_mcp_calback_url")
    mcp_https_url = fields.Char(string="Google Origin URL", readonly=True, copy=False,
                                compute="_compute_mcp_calback_url")
    mcp_callback_url = fields.Char(string="Google Callback URL", readonly=True, copy=False,
                                   compute="_compute_mcp_calback_url")
    remote_state = fields.Char(string="Remote Status", readonly=True, copy=False)

    registration_state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("registered", "Registered"),
            ("error", "Error"),
        ],
        string="Status",
        default="draft",
        required=True,
        copy=False,
    )
    last_error = fields.Text(string="Last Error", readonly=True, copy=False)
    registered_on = fields.Datetime(string="Registered On", readonly=True, copy=False)

    def action_fill_odoo_url(self):
        """Fill the Odoo URL with this instance's base URL, forcing https."""
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url") or ""
        base_url = base_url.strip().rstrip("/")
        if base_url.startswith("http://"):
            base_url = "https://" + base_url[len("http://"):]
        elif not base_url.startswith("https://"):
            base_url = "https://" + base_url
        self.odoo_url = base_url
        return True

    def action_fill_odoo_db(self):
        """Fill the Odoo Database with the current database name."""
        self.ensure_one()
        self.odoo_db = self.env.cr.dbname
        return True

    @api.depends("use_google_oauth")
    def _compute_auth_method(self):
        for rec in self:
            rec.auth_method = "google_oauth" if rec.use_google_oauth else "access_token"

    @api.depends('mcp_url')
    def _compute_mcp_calback_url(self):
        for rec in self:
            if not rec.mcp_url:
                rec.mcp_ai_url = rec.mcp_https_url = rec.mcp_callback_url = False
                continue
            url = rec.mcp_url.strip().rstrip("/")
            if not url.startswith(("http://", "https://")):
                url = f"https://{url}"
            rec.mcp_ai_url = url
            rec.mcp_https_url = url.removesuffix("/mcp")
            rec.mcp_callback_url = rec.mcp_https_url + '/auth/callback'

    @api.constrains("use_google_oauth", "google_client_id", "google_client_secret")
    def _check_google_oauth(self):
        for rec in self:
            if rec.use_google_oauth and not (
                (rec.google_client_id or "").strip()
                and (rec.google_client_secret or "").strip()
            ):
                raise ValidationError(_(
                    "Google Client ID and Google Client Secret are required "
                    "when \"Use Google OAuth\" is enabled."
                ))

    def _check_registrar_url(self):
        for record in self:
            if record.registrar_url and not record.registrar_url.startswith(
                    ("http://", "https://")
            ):
                raise ValidationError(
                    _("Registrar URL must start with http:// or https://")
                )

    def _register_payload(self):
        self.ensure_one()
        data = {
            "name": self.name,

            "odoo_url": self.odoo_url,
            "odoo_db": self.odoo_db,
            "odoo_login": self.odoo_login,
            "odoo_api_key": self.odoo_api_key,
            "auth_method": self.auth_method,
            "use_google_oauth": self.use_google_oauth,
            "google_client_id": self.google_client_id if self.use_google_oauth else "",
            "google_client_secret": self.google_client_secret if self.use_google_oauth else "",
            "odoo_admin_emails": self.odoo_admin_emails or "",
            "odoo_admin_access_tokens": self.odoo_admin_access_tokens or "",
            "roles": [
                {
                    "role_name": role.role_name,
                    "odoo_api_key": role.odoo_api_key,
                    "emails": role.emails or "",
                    "access_tokens": role.access_tokens or "",
                }
                for role in self.role_ids
            ],
        }
        if self.tenant_uuid:
            data["tenant_uuid"] = self.tenant_uuid
        return data

    def _mark_error(self, message):
        self.write({"registration_state": "error", "last_error": message})
        raise UserError(message)

    def action_register(self):
        self.ensure_one()
        self._check_registrar_url()
        self._check_google_oauth()
        if not self.use_google_oauth and not (
            (self.odoo_admin_access_tokens or "").strip()
            or any((role.access_tokens or "").strip() for role in self.role_ids)
        ):
            raise UserError(_(
                "Google OAuth is disabled: set at least one Access Token "
                "(on a role) so the AI client can connect."
            ))
        endpoint = self.registrar_url.rstrip("/")
        envelope = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": self._register_payload(),
        }

        try:
            response = requests.post(endpoint, json=envelope, timeout=30)
            response.raise_for_status()
            body = response.json()
        except (requests.RequestException, ValueError) as exc:
            self._mark_error(_("Registration request failed: %s") % exc)

        if body.get("error"):
            error = body["error"]
            message = (error.get("data") or {}).get("message") or error.get("message")
            self._mark_error(_("Registrar returned an error: %s") % message)

        result = body.get("result") or {}
        if result.get("error") == "missing_fields":
            self._mark_error(
                _("Registrar rejected the request, missing fields: %s")
                % ", ".join(result.get("fields", []))
            )

        if not result.get("tenant_uuid"):
            self._mark_error(_("Registrar returned an unexpected response."))

        self.write({
            "tenant_uuid": result.get("tenant_uuid"),
            "mcp_url": result.get("mcp_url"),
            "remote_state": result.get("state"),
            "registration_state": "registered",
            "last_error": False,
            "registered_on": fields.Datetime.now(),
        })
        _logger.info("Registered MCP client %s (%s)", self.name, self.tenant_uuid)
        return True
