/**@odoo-module */
const {Component, onMounted, useState} = owl;
import {registry} from "@web/core/registry";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToString } from "@web/core/utils/render";
const actionRegistry = registry.category("actions");

export class SmartAnalyticsDashboard extends Component {
    // every time setup is called, dashboard data is loaded.
    setup(){
        super.setup();
        this.smaDashboard = useState({ data: [] })
        onMounted(()=>{
            this.loadData();
        })
    }
    // With Json RPC, dashboard data is called up via a controller and returned to the view.
    loadData(){
        let self = this;
        jsonrpc('/get/dashboard',{}).then(function (data) {
            self.smaDashboard.data = data;
        });
    }
    // When a dashboard is selected, its Id is sent back to the controller in order to receive the url of the dashboard to be displayed.
    getUrl(ev, id) {
        jsonrpc('/get/url', {item: id}).then(function (data) {
            var modalHtml = window.$(renderToString("smart_analytics_dashboard_modal",
                {
                    url: data.url,
                    name: data.name,
                }));
            $('.js-smart-analytics').append(modalHtml);
            $(modalHtml).modal('toggle');
        });
    }
}
SmartAnalyticsDashboard.template = "SmartanalyticsDashboard";
actionRegistry.add("smart_analytics_dashboard", SmartAnalyticsDashboard);