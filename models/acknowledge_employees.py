from odoo import models, api, fields


class AcknowledgeEmployees(models.Model):
    _name = 'acknowledge.employees'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    data_id = fields.Many2one('logic.rules')
    self_declaration = fields.Binary(string="Self Declaration Form", )
    acknowledge_date = fields.Datetime(String="DateTime")
    designation = fields.Char(string="Designation")
