odoo.define('dashboard_frame.smart_analytics.url2iframe', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var fieldRegistry = require('web.field_registry');

    var QWeb = core.qweb;


    var FieldUrl2Iframe = AbstractField.extend({
        className: 'd-block o_field_url2iframe m-0 h-100',

        _render: function () {
            this.$el.html(QWeb.render('smartanalytics.iframe', {
                url: this.value,
            }));
        },
    });

    fieldRegistry.add('url2iframe', FieldUrl2Iframe);

    return FieldUrl2Iframe;
});
