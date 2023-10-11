odoo.define('dashboard_frame.smart_analytics.form_renderer', function (require) {
    "use strict";

    var FormRenderer = require('web.FormRenderer');

    var SmartAnalyticsFormRenderer = FormRenderer.extend({
        _updateView: function ($newContent) {
            var self = this;
            this._super.apply(this, arguments);
            this.$el.css('height', '100%').css('padding', '4px');
        },
    });

    return SmartAnalyticsFormRenderer;
});
