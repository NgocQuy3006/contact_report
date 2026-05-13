from odoo import models, fields


class ContactReportLine(models.Model):
    _name = 'contact.report.line'
    _description = 'Contact Report Line'

    report_id = fields.Many2one(
        'contact.report'
    )

    sequence = fields.Integer()

    partner_id = fields.Many2one(
        'res.partner'
    )

    name = fields.Char()

    email = fields.Char()

    phone = fields.Char()

    company = fields.Char()

    status = fields.Char()