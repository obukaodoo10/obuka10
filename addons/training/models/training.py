# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class trainingTraining(models.Model):
    _name = 'training.training'

    name = fields.Char('Name', limit=20, required=True)
    description = fields.Text('Description')
    length_days = fields.Integer('Length In Days')
    start_date = fields.Date('Start Date')
    price = fields.Float('Training Price', digits=(16, 4))
    # create_date = fields.Datetime('Created On', readonly=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')], default='draft')
    student_ids = fields.One2many('training.student', 'training_id', 'Students')
    trainer_id = fields.Many2one('res.partner', 'Trainer', required=True)
    number = fields.Char('Number', readonly=True)
    location = fields.Many2one('location.training')



    _sql_constraints = [
        ('number_uniq', 'unique(number)', 'Training Number must be unique!'),
    ]

    @api.multi
    def action_confirm(self):
        for training in self:
            training.state = 'confirmed'

    @api.multi
    def action_done(self):
        for training in self:
            training.state = 'done'

    @api.multi
    def action_cancel(self):
        for training in self:
            training.state = 'cancel'

    @api.multi
    def action_activate(self):
        for training in self:
            training.state = 'draft'

    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('training') or _('NaV')

        res = super(trainingTraining, self).create(vals)

        return res

    @api.multi
    def unlink(self):
        # for training in self:
        #     if training.state != 'cancel':
        #         raise UserError(_('You cannot delete training that are not canceled!'))

        if self.filtered(lambda x: x.state not in ('cancel')):
            raise UserError(_('You cannot delete training that are not canceled!'))

        return super(trainingTraining, self).unlink()


    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)

    # @api.depends('value')
    # def _value_pc(self):
    #     self.value2 = float(self.value) / 100


class studentTraining(models.Model):
    _name = 'training.student'

    training_id = fields.Many2one('training.training', 'Training', required=True, readonly=True)
    name = fields.Char('Name', limit=20, required=True)
    surname = fields.Char('Surname', limit=30)
    age = fields.Integer('Age')


class trainingLocation(models.Model):
    _name = 'location.training'

    name = fields.Char('Name', limit=20, required=True)
    adress = fields.Char('Adress', limit=20)
    city = fields.Char('City')
    country = fields.Many2one('res.country',string = 'Country')
    surname = fields.Char('Surname', limit=30)
    age = fields.Integer('Age')
    description = fields.Html('Description')
    addition = fields.Text('Practice!')
    All = fields.One2many('training.training', 'location', 'How_many')


