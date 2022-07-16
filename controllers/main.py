# -*- coding: utf-8 -*-
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2017 BulkTP
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import odoo
import base64
from pprint import pprint


class WebsiteForm(odoo.addons.website_form.controllers.main.WebsiteForm):

    def insert_record(self, request, model, values, custom, meta=None):
        record_id = super(WebsiteForm, self).insert_record(request, model, values, custom, meta)
        ids = []
        if len(request.params) > 6:
            i = 0
            while i != -1:
                try:
                    file_name = request.params['attachment[0][' + str(i)+ ']'].filename
                    field_value = base64.b64encode(request.params['attachment[0]['+ str(i)+']'].read())
                    vals = {'name': file_name,
                            'datas': field_value,
                            'res_model': 'ir.ui.view',
                            }
                    at = request.env['ir.attachment'].create(vals)
                    print(at)
                    ids.append(at.id)
                    i += 1
                except:
                    i = -1
        if values.get('email_from'):
            template_id = request.env['ir.model.data'].sudo().get_object_reference('website_contact_notify', 
                                                                                   'website_contact_notify_mail')[1]
            mail_id = request.env['mail.template'].sudo().browse(template_id).send_mail(int(record_id), force_send=True, 
                                                                                                        email_values = {'attachment_ids': ids})
        return record_id
