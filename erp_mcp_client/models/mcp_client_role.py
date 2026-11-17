from odoo import fields, models


class McpClientRole(models.Model):
    _name = "erp.mcp.client.role"
    _description = "ERP MCP Client Role"
    _order = "role_name"

    client_id = fields.Many2one(
        comodel_name="erp.mcp.client",
        string="Registration",
        required=True,
        ondelete="cascade",
        index=True,
    )
    role_name = fields.Char(
        string="Role",
        required=True,
        help="Role name sent to the registrar. On the MCP server it becomes "
             "ODOO_<ROLE>_API_KEY / ODOO_<ROLE>_EMAILS (e.g. admin, sales, readonly).",
    )
    odoo_api_key = fields.Char(
        string="Odoo API Key",
        required=True,
        help="API key of the Odoo user this role should act as.",
    )
    emails = fields.Char(
        string="Allowed Emails",
        help="Comma-separated Google emails that log into the MCP as this role.",
    )
    access_tokens = fields.Char(
        string="Access Tokens",
        help="Comma-separated static Bearer tokens that authenticate as this "
             "role (Authorization: Bearer <token>), no Google login needed.",
    )
