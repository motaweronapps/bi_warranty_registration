odoo.define('ye_dynamic_odoo.PivotViewContent', function (require) {
"use strict";

    var core = require('web.core');
    // var FieldBasic = require('odoo_dynamic.FieldBasic');
    // var FormRenderer = require('web.FormRenderer');
    // var ListViewEdit = require('odoo_dynamic.ListViewEdit');
    var PivotView = require('web.PivotView');
    var PivotController = require('web.PivotController');
    var ActionManager = require('web.ActionManager');
    var session = require('web.session');

    var QWeb = core.qweb;
    var Base = require('ye_dynamic_odoo.BaseEdit');
    var Context = require('web.Context');

    PivotController.include({
        init: function (parent, model, renderer, params) {
            this._super(parent, model, renderer, params);
            this.props = params;
        },
        _pushState: function () {
            const {fromEdit} = this.props;
            if (!fromEdit) {
                this._super();
            }
        }
    });

    var PivotEditContent = Base.ContentBase.extend({
        template: 'PivotViewEdit.Content',
        init: function(parent, params) {
            this._super(parent, params);
            this.parent = parent;
        },
        start: function () {
            const {action} = this.props;
            this.action = action;
        },
        bindAction: function () {
        },
        renderView: function () {
            let self = this;
            const {context, domain, limit, res_model, filter} = this.action, {viewInfo} = this.props;
            let params = {
                action: this.action,
                context: context,
                domain: domain || [],
                groupBy: [],
                limit: limit,
                filter: filter || [],
                modelName: res_model,
                withControlPanel: false,
                withSearchPanel: false,
            };
            let pivotView = new PivotView(viewInfo, params);
            pivotView.controllerParams.fromEdit = true;
            pivotView.getController(self).then(function (widget) {
                widget.appendTo(self.$el);
                self.bindAction();
            });
        },
    });

    return PivotEditContent;

});
