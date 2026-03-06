from odoo import models
from odoo.exceptions import UserError
import io
import xlsxwriter
import base64


class BankAdviceXlsx(models.TransientModel):
    _name = "bank.advice.xlsx"
    _description = "Bank Advice Excel Export"

    def export_xlsx(self):
        payslips = self.env.context.get("active_ids")

        if not payslips:
            raise UserError("No payslips selected")

        slips = self.env["hr.payslip"].browse(payslips)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet("Bank Advice")

        headers = [
            "Employee",
            "Account Number",
            "Bank",
            "Net Salary",
        ]

        for col, header in enumerate(headers):
            sheet.write(0, col, header)

        row = 1

        for slip in slips:
            sheet.write(row, 0, slip.employee_id.name)
            sheet.write(row, 1, slip.employee_id.bank_account_id.acc_number or "")
            sheet.write(row, 2, slip.employee_id.bank_account_id.bank_id.name or "")
            sheet.write(row, 3, slip.get_salary_line_total("NET"))

            row += 1

        workbook.close()

        output.seek(0)

        file = base64.b64encode(output.read())

        attachment = self.env["ir.attachment"].create({
            "name": "Bank_Advice.xlsx",
            "type": "binary",
            "datas": file,
            "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        })

        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/%s?download=true" % attachment.id,
            "target": "self",
        }