from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date
from markupsafe import Markup

class L10nClDteCaf(models.Model):
    """
    Extensión del modelo de Código de Autorización de Folios (CAF) para Chile.
    Incorpora validaciones de caducidad y disponibilidad de folios, junto con
    notificaciones automáticas para la gestión proactiva de facturación.
    """
    _name = 'l10n_cl.dte.caf'
    _inherit = ['l10n_cl.dte.caf', 'mail.thread', 'mail.activity.mixin']

    def action_verificar_libres(self):
        """
        Acción manual para verificar el estado de los folios del CAF actual.
        Calcula los folios restantes y evalúa reglas de negocio (caducidad de 6 meses
        y umbral crítico del 20%). Retorna una notificación en la interfaz de usuario.
        """
        self.ensure_one()

        numero_final = self.final_nb
        fecha_emision = self.issued_date
        tipo_documento = self.l10n_latam_document_type_id.code

        # Recupera el último movimiento contable publicado para este tipo de documento y compañía
        ultimo_movimiento = self.env['account.move'].search([
            ('l10n_latam_document_type_id', '=', self.l10n_latam_document_type_id.id),
            ('state', '=', 'posted'),
            ('company_id', '=', self.company_id.id)
        ], order='date desc', limit=1)

        num_folio = 0
        if ultimo_movimiento and ultimo_movimiento.l10n_latam_document_number:
            try:
                # Extracción de la secuencia numérica del documento, descartando prefijos (ej. "33 - 000085")
                folio_str = ''.join(filter(str.isdigit, ultimo_movimiento.l10n_latam_document_number))
                if folio_str:
                    num_folio = int(folio_str)
            except Exception:
                # En caso de error de parseo, se mantiene num_folio en 0 para evitar interrupción del flujo
                pass

        # Cálculo de folios disponibles
        folios_restantes = numero_final - num_folio

        fecha_actual = fields.Date.context_today(self)
        hace_6_meses = fecha_actual - relativedelta(months=6)

        mensaje = f"Ha emitido hasta el folio: {num_folio}\n"
        mensaje += f"Le quedan {folios_restantes} por emitir\n\n"

        # Evaluación de reglas de negocio para alertas
        # 1. Caducidad: Los CAFs (excepto Exportación 110 y 112) caducan a los 6 meses de emisión
        if fecha_emision and fecha_emision < hace_6_meses and tipo_documento not in ['110', '112']:
            self.status = 'spent'
            mensaje += "Este CAF ha sido dado por consumido por fecha.\nSe sugiere solicitar uno nuevo al SII."
            tipo_notificacion = 'warning'
        else:
            # 2. Umbral de disponibilidad: Alerta si queda un 20% o menos de la capacidad del CAF
            if numero_final > 0 and (folios_restantes / numero_final) <= 0.20:
                mensaje += "Se sugiere solicitar un nuevo CAF. Nivel crítico de folios."
                tipo_notificacion = 'warning'
            else:
                tipo_notificacion = 'success'

        # Retorna una acción de cliente para mostrar la notificación tipo "toast" en Odoo
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Estado de Folios CAF',
                'message': mensaje,
                'type': tipo_notificacion,
                'sticky': True,
            }
        }

    @api.model
    def _cron_verificar_folios_caf(self):
        """
        Proceso automatizado (Cron) para auditar periódicamente los CAFs en estado 'in_use'.
        Genera alertas en el Chatter y envía notificaciones por correo electrónico si un CAF
        está próximo a caducar o por agotarse.
        """
        # Filtramos únicamente los CAFs que están operativos
        cafs_activos = self.search([('status', '=', 'in_use')])

        fecha_actual = fields.Date.context_today(self)
        hace_6_meses = fecha_actual - relativedelta(months=6)

        for caf in cafs_activos:
            numero_final = caf.final_nb
            fecha_emision = caf.issued_date
            tipo_documento = caf.l10n_latam_document_type_id.code

            ultimo_movimiento = self.env['account.move'].search([
                ('l10n_latam_document_type_id', '=', caf.l10n_latam_document_type_id.id),
                ('state', '=', 'posted'),
                ('company_id', '=', caf.company_id.id)
            ], order='date desc', limit=1)

            num_folio = 0
            if ultimo_movimiento and ultimo_movimiento.l10n_latam_document_number:
                try:
                    folio_str = ''.join(filter(str.isdigit, ultimo_movimiento.l10n_latam_document_number))
                    if folio_str:
                        num_folio = int(folio_str)
                except Exception:
                    pass

            folios_restantes = numero_final - num_folio
            necesita_alerta = False

            mensaje_alerta = f"Se requiere atención para el CAF tipo {tipo_documento}.<br/>"
            mensaje_alerta += f"Ha emitido hasta el folio: {num_folio}. Le quedan {folios_restantes} por emitir.<br/><br/>"

            # Validación de caducidad
            if fecha_emision and fecha_emision < hace_6_meses and tipo_documento not in ['110', '112']:
                caf.status = 'spent'
                mensaje_alerta += "<b>Motivo:</b> Este CAF ha sido dado por consumido por fecha (mayor a 6 meses).<br/>Se requiere solicitar renovación."
                necesita_alerta = True
            else:
                # Validación de umbral crítico de folios (<= 20%)
                if numero_final > 0 and (folios_restantes / numero_final) <= 0.20:
                    mensaje_alerta += "<b>Motivo:</b> Capacidad de folios al 20% o inferior.<br/>Se sugiere solicitar un nuevo lote."
                    necesita_alerta = True

            # Generación de registros y notificaciones si aplican las reglas
            if necesita_alerta:
                mensaje_seguro = Markup(mensaje_alerta)

                # 1. Registro de auditoría interna en el Chatter del documento
                caf.message_post(
                    body=mensaje_seguro,
                    subject='Alerta Automática de Folios',
                    message_type='notification',
                    subtype_xmlid='mail.mt_comment',
                )

                # 2. Construcción de enlace directo al registro para la notificación por correo
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                url_documento = f"{base_url}/web#id={caf.id}&model={caf._name}&view_type=form"
                
                boton_html = f'<br/><br/><a href="{url_documento}" style="background-color: #875A7B; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Ver Registro en Odoo</a>'
                cuerpo_correo = mensaje_seguro + Markup(boton_html)

                # 3. Envío de correo electrónico a los responsables
                mail_values = {
                    'subject': f'Alerta Odoo: CAF {tipo_documento} requiere atención',
                    'body_html': cuerpo_correo,
                    'email_to': 'leoneelondono39@gmail.com',
                    'email_from': self.env.user.company_id.email or 'admin@odoo.local',
                }
                self.env['mail.mail'].sudo().create(mail_values).send()