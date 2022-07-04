odoo.define('ye_dynamic_odoo.GraphViewContent', function (require) {
"use strict";

    var core = require('web.core');
    var GraphView = require('web.GraphView');
    var GraphController = require('web.GraphController');
    var ActionManager = require('web.ActionManager');
    var session = require('web.session');

    var Base = require('ye_dynamic_odoo.BaseEdit');

    GraphController.include({
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

    var GraphViewContent = Base.ContentBase.extend({
        template: 'GraphViewEdit.Content',
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
                groupedBy: [],
                limit: limit,
                filter: filter || [],
                currentId: undefined,
                disableCustomFilters: undefined,
                footerToButtons: false,
                hasSearchView: true,
                hasSidebar: true,
                headless: false,
                timeRange: [],
                ids: undefined,
                mode: false,
                modelName: res_model,
                withControlPanel: false,
                withSearchPanel: false,
            };
            let graphView = new GraphView(viewInfo, params);
            graphView.controllerParams.fromEdit = true;
            graphView.loadParams.groupedBy = [];
            graphView.loadParams.timeRange = [];
            graphView.getController(self).then(function (widget) {
                widget.renderer.isInDOM = true;
                widget.appendTo(self.$el);
                self.bindAction();
            });
        },
    });

    return GraphViewContent;

});
