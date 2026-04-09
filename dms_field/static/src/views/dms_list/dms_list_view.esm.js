/** @odoo-module **/

/* Copyright 2024 Tecnativa - Carlos Roca
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
import {DmsListArchParser} from "./dms_list_arch_parser.esm";
import {DmsListController} from "./dms_list_controller.esm";
import {DmsListRenderer} from "./dms_list_renderer.esm";
import {RelationalModel} from "@web/model/relational_model/relational_model";
import {registry} from "@web/core/registry";
import {_t} from "@web/core/l10n/translation";

export const dmsListView = {
    type: "dms_list",
    
    // --- PROPIEDADES OBLIGATORIAS PARA ODOO 17 ---
    display_name: _t("DMS"),
    icon: "fa fa-folder-open-o",
    multiRecord: true,
    // ---------------------------------------------

    Controller: DmsListController,
    ArchParser: DmsListArchParser,
    Renderer: DmsListRenderer,
    Model: RelationalModel,

    props(genericProps, view) {
        const {ArchParser} = view;
        const {arch, relatedModels, resModel} = genericProps;
        const archInfo = new ArchParser().parse(arch, relatedModels, resModel);

        return {
            ...genericProps,
            Model: view.Model,
            Renderer: view.Renderer,
            archInfo,
        };
    },
};

registry.category("views").add("dms_list", dmsListView);
