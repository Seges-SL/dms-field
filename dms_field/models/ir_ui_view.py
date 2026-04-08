# Copyright 2020 Creu Blanca
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, fields, models

from odoo.addons.base.models.ir_ui_view import NameManager


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    type = fields.Selection(selection_add=[("dms_list", "DMS Tree")])

    def _get_view_info(self):
        res = super()._get_view_info()
        res["dms_list"] = {"icon": "fa fa-file-o"}
        return res

    def _postprocess_tag_dms_list(self, node, name_manager, node_info):
        # 1. CRÍTICO: Actualizar el node_info original para que el framework sepa el tipo de vista
        node_info['view_type'] = node.tag

        parent = node.getparent()
        parent_name = parent.get("name") if parent is not None else None
        
        new_name_manager = name_manager
        
        # 2. Si la vista está dentro de un campo (x2many), adaptamos el modelo
        if parent_name:
            field = name_manager.model._fields.get(parent_name)
            if field:
                model_name = field.comodel_name
                if model_name in self.env:
                    model = self.env[model_name]
                    new_name_manager = NameManager(model, parent=name_manager)

        # 3. Procesar los campos hijos usando el node_info actualizado
        for child in node:
            self._postprocess_tag_field(child, new_name_manager, node_info)
