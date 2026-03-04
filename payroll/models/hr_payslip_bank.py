# hr_payslip_bank.py
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, _
from odoo.exceptions import UserError

class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    def action_print_bank_advice(self):
        """Prints the bank advice report for selected payslips."""
        slips = self

        if not slips:
            raise UserError(_("No payslips selected."))

        if any(slip.state != 'done' for slip in slips):
            raise UserError(_("All selected payslips must be in Done state."))

        # Reference the report by external ID
        report = self.env.ref("payroll.report_bank_advice")
        if not report:
            raise UserError(_("Bank Advice report not found. Check XML file."))

        return report.report_action(slips)