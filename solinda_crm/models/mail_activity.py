# action_feedback
from odoo import _, api, fields, models
from odoo.tools.misc import clean_context


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def action_done_schedule_next(self):
        self = self.sudo()
        case = ['PO Received','Contract Signed','Contract Signed / PO Received','11. Contract Signed / PO Received','11.Contract Signed / PO Received']
        if any(self.activity_type_id.name in n for n in case) and self.res_model == 'crm.lead':
            crm_id = self.env["crm.lead"].search([("id", "=",self.res_id)])
            progress = self.activity_type_id.progress * 100
            prob_comp = crm_id.probability + progress
            crm_id.additional_prob = progress
            crm_id.automated_probability = progress
            crm_id.probability += prob_comp
            crm_id.is_po_receive = True
        return super(MailActivity, self).action_done_schedule_next()
        
    
    def action_done(self):
        self = self.sudo()
        case = ['PO Received','Contract Signed','Contract Signed / PO Received','11. Contract Signed / PO Received','11.Contract Signed / PO Received']
        if any(self.activity_type_id.name in n for n in case) and self.res_model == 'crm.lead':
            crm_id = self.env["crm.lead"].search([("id", "=",self.res_id)])
            progress = self.activity_type_id.progress * 100
            prob_comp = crm_id.probability + progress
            crm_id.additional_prob = progress
            crm_id.automated_probability = progress
            crm_id.probability += prob_comp
            crm_id.is_po_receive = True
        res = super(MailActivity, self).action_done()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            }

    def action_close_dialog(self):
        res = super(MailActivity, self).action_close_dialog()
        case = ['PO Received','Contract Signed','Contract Signed / PO Received','11. Contract Signed / PO Received','11.Contract Signed / PO Received']
        if any(self.activity_type_id.name in n for n in case) and self.res_model == 'crm.lead':
            crm_id = self.env["crm.lead"].search([("id", "=",self.res_id)])
            crm_id.is_po_receive = True
        return res
    
    def action_feedback(self, feedback=False, attachment_ids=None):
        if self.res_model == 'crm.lead':
            crm_id = self.env[self.res_model].browse(self.res_id)
            progress = self.activity_type_id.progress * 100
            crm_id.probability += progress
        res = super().action_feedback(feedback=False, attachment_ids=None)
        return res
        