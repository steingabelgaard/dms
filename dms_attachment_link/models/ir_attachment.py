# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo import api, fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    dms_file_id = fields.Many2one(comodel_name="dms.file")

    @api.depends("dms_file_id", "dms_file_id.content")
    def _compute_datas(self):
        """Get the contents of the attachment directly from the DMS file."""
        _self = self.filtered("dms_file_id")
        res = super(IrAttachment, (self - _self))._compute_datas()
        for item in _self:
            item.datas = item.dms_file_id.content
        return res

    @api.depends("store_fname", "db_datas", "dms_file_id", "dms_file_id.content")
    def _compute_raw(self):
        _self = self.filtered("dms_file_id")
        res = super(IrAttachment, (self - _self))._compute_raw()
        for item in _self:
            item.raw = base64.b64decode(item.dms_file_id.content)
        return res
