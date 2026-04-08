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
        # 1. Obtener el padre de forma segura para evitar el FutureWarning de lxml
        parent = node.getparent()
        parent_name = parent.get("name") if parent is not None else None
        
        # 2. Inicializamos el NameManager por defecto para Odoo 17
        new_name_manager = name_manager
        
        # 3. Si la vista está dentro de un campo (x2many), adaptamos el modelo
        if parent_name:
            field = name_manager.model._fields.get(parent_name)
            if field:
                model_name = field.comodel_name
                if model_name not in self.env:
                    self._raise_view_error(
                        _("Model not found: %(model)s", model=model_name), node
                    )
                model = self.env[model_name]
                new_name_manager = NameManager(model, parent=name_manager)

        root_info = {
            "view_type": node.tag,
            "view_editable": self._editable_node(node, name_manager),
            "name_manager": name_manager,
        }
        new_node_info = dict(
            root_info,
            modifiers={},
            editable=self._editable_node(node, new_name_manager),
        )
        
        # 4. CRÍTICO: El bucle FOR debe estar FUERA del 'if' para que 
        # siempre se procesen los campos hijos de la vista dms_list.
        for child in node:
            self._postprocess_tag_field(child, new_name_manager, new_node_info)
