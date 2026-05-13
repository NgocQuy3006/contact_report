from odoo import models, fields
from odoo.osv import expression


class ContactReport(models.Model):
    _name = 'contact.report'
    _description = 'Contact Report'
    _rec_name = 'company_id'

    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company
    )

    customer = fields.Boolean(string='Customer')

    supplier = fields.Boolean(string='Vendor')

    active = fields.Boolean(default=True)

    inactive = fields.Boolean()

    line_ids = fields.One2many(
        'contact.report.line',
        'report_id',
        string='Lines'
    )

    def action_apply(self):

        domain = []

        partner_domain = []

        if self.customer:
            partner_domain.append(('customer_rank', '>', 0))

        if self.supplier:
            partner_domain.append(('supplier_rank', '>', 0))

        if len(partner_domain) == 2:
            domain = expression.OR([
                [partner_domain[0]],
                [partner_domain[1]],
            ])

        elif len(partner_domain) == 1:
            domain.append(partner_domain[0])

        if self.active and not self.inactive:
            domain.append(('active', '=', True))

        elif self.inactive and not self.active:
            domain.append(('active', '=', False))

        contacts = self.env['res.partner'].search(domain)

        self.line_ids.unlink()

        vals = []

        no = 1

        for partner in contacts:

            vals.append((0, 0, {
                'sequence': no,
                'partner_id': partner.id,
                'name': partner.name or '',
                'email': partner.email or '',
                'phone': partner.phone or '',
                'company': partner.company_id.name or '',
                'status': 'Active' if partner.active else 'Inactive',
            }))

            no += 1

        self.line_ids = vals

        return True

    def action_export_excel(self):

        return self.env.ref(
            'contact_excel_report.contact_report_xlsx_action'
        ).report_action(self)