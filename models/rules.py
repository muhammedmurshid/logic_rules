from odoo import models, fields, api, _
from odoo.exceptions import UserError


class LogicRules(models.Model):
    _name = 'logic.rules'
    _description = 'Rules'
    _rec_name = 'display_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    rule_type = fields.Selection(
        [('by_company', 'By Company'), ('by_department', 'By Department'), ('by_employee', 'By Employee')],
        string='Type', default='by_department')
    department_id = fields.Many2one('hr.department', string='Department')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    rule = fields.Text(string='Policies')
    state = fields.Selection([('draft', 'Draft'), ('sent', 'Sent')], default='draft',
                             tracking=1)
    files = fields.Html(string='Files')
    datas_ids = fields.One2many('acknowledge.employees', 'data_id', string='Datas')

    def _compute_display_name(self):
        for i in self:
            if i.rule_type:
                if i.rule_type == 'by_department':
                    i.display_name = 'Rules for ' + i.department_id.name
                if i.rule_type == 'by_company':
                    i.display_name = 'Company Rules'
                elif i.rule_type == 'by_employee':
                    i.display_name = 'Rules for ' + i.employee_id.name
            else:
                i.display_name = 'Rules'

    def action_sent_notification_button(self):
        print('hi')
        for i in self:
            if i.rule_type == 'by_company':
                employees = self.env['hr.employee'].sudo().search([('active', '=', True)])
                for employee in employees:
                    i.activity_schedule('logic_rules.activity_for_logic_rules', user_id=employee.user_id.id,
                                        note=i.rule)
            elif i.rule_type == 'by_employee':
                print(i.employee_id.name, 'employee')
                i.activity_schedule('logic_rules.activity_for_logic_rules', user_id=i.employee_id.user_id.id,
                                    note=i.rule)
            elif i.rule_type == 'by_department':
                employees = self.env['hr.employee'].sudo().search([('department_id', '=', i.department_id.id)])
                for employee in employees:
                    i.activity_schedule('logic_rules.activity_for_logic_rules', user_id=employee.user_id.id,
                                        note=i.rule)
            i.state = 'sent'

    def action_mark_as_done(self):
        print('kkk')
        # self.state = 'acknowledge'
        activity_id = self.env['mail.activity'].search([('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
            'activity_type_id', '=', self.env.ref('logic_rules.activity_for_logic_rules').id)])
        activity_id.action_feedback(feedback='Acknowledge')
        datas = []
        for record in self:
            employee_ids = record.datas_ids.mapped('employee_id')
            print(employee_ids, 'emp')
            for j in employee_ids:
                datas.append(j.id)
        print(datas, 'da')
        if self.env.user.employee_id.id in datas:
            raise UserError(
                _("You have already acknowledged this policy.")
            )
        else:
            self.datas_ids = [(0, 0, {
                'employee_id': self.env.user.employee_id.id
            })]
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Policies Acknowledge.',
                    'type': 'rainbow_man',
                }
            }

    @api.onchange('rule_type')
    def _onchange_rule_type(self):
        for i in self:
            if i.rule_type:
                if i.rule_type == 'by_employee':
                    i.department_id = False
                elif i.rule_type == 'by_company':
                    i.department_id = False
                    i.employee_id = False
                elif i.rule_type == 'by_department':
                    i.employee_id = False

