from odoo import models
from datetime import datetime


class ContactReportXlsx(models.AbstractModel):
    _name = 'report.contact_excel_report.contact_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, reports):

        sheet = workbook.add_worksheet('contacts')

        # ================= FORMAT =================
        title = workbook.add_format({
            'bold': True,
            'font_size': 16
        })

        header = workbook.add_format({
            'bold': True,
            'align': 'center',
            'bg_color': '#D9E1F2',
            'border': 1
        })

        normal = workbook.add_format({
            'border': 1
        })

        small = workbook.add_format({
            'font_size': 9
        })

        # ================= REPORT =================
        for report in reports:

            company = report.company_id

            # ================= HEADER =================
            sheet.write('A1', company.name or '', title)

            sheet.write(
                'A3',
                'MST: %s' % (company.vat or '')
            )

            sheet.write(
                'E1',
                'Run Report: ' + str(datetime.now()),
                small
            )

            sheet.merge_range(
                'A5:F5',
                'CONTACT REGISTERS',
                title
            )

            # ================= FILTER INFO =================
            sheet.write(
                'A6',
                'Company: %s' % (company.name or '')
            )

            sheet.write(
                'A7',
                'Customer: %s' % (
                    'Yes' if report.customer else 'All'
                )
            )

            sheet.write(
                'A8',
                'Supplier: %s' % (
                    'Yes' if report.supplier else 'All'
                )
            )

            status = 'All'

            if report.active and not report.inactive:
                status = 'Active'

            elif report.inactive and not report.active:
                status = 'Inactive'

            sheet.write(
                'A9',
                'Status: %s' % status
            )

            # ================= TABLE HEADER =================
            headers = [
                'No',
                'Name',
                'Email',
                'Phone',
                'Company',
                'Status'
            ]

            row = 11

            for col, h in enumerate(headers):
                sheet.write(row, col, h, header)

            # ================= DATA =================
            row += 1
            no = 1

            for line in report.line_ids:

                sheet.write(row, 0, no, normal)
                sheet.write(row, 1, line.name or '', normal)
                sheet.write(row, 2, line.email or '', normal)
                sheet.write(row, 3, line.phone or '', normal)
                sheet.write(row, 4, line.company or '', normal)
                sheet.write(row, 5, line.status or 'Active', normal)

                row += 1
                no += 1

        # ================= COLUMN WIDTH =================
        sheet.set_column('A:A', 5)
        sheet.set_column('B:B', 30)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 25)
        sheet.set_column('F:F', 15)