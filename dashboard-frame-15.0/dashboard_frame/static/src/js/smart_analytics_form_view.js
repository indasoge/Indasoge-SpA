odoo.define('dashboard_frame.smart_analytics.form_view', function (require) {
    "use strict";

    var viewRegistry = require('web.view_registry');
    var FormView = require('web.FormView');
    var SmartAnalyticsFormRenderer = require('dashboard_frame.smart_analytics.form_renderer');

    var SmartAnalyticsFormView = FormView.extend({
        config: Object.assign({}, FormView.prototype.config, {
            Renderer: SmartAnalyticsFormRenderer,
        }),
    });

    viewRegistry.add('smartanalytics_form', SmartAnalyticsFormView);

    return SmartAnalyticsFormView;
});
