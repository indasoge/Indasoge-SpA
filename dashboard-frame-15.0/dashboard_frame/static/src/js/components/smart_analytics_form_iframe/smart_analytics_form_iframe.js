/** @odoo-module **/

const { Component, onMounted, useState } = owl;
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

// Main component for displaying analytics dashboards in an iframe
class SmartAnalyticsDashboardIframe extends Component {
    setup() {
        // Initialize ORM and action services
        this.orm = useService("orm");
        this.action = useService("action");

        // Retrieve dashboard ID and name from session storage
        const dashboardId = sessionStorage.getItem('currentDashboardId');
        const dashboardName = sessionStorage.getItem('currentDashboardName');

        // Initialize component state
        this.state = useState({
            dashboards: [],
            currentIndex: 0,
            loading: true,
            error: null,
            dashboard: null,
            dashboard_id: dashboardId,
            dashboard_name: dashboardName
        });

        // Load all dashboards when component is mounted
        onMounted(() => {
            this.loadAllDashboards();
        });
    }

    // Fetch all dashboards from the server
    async loadAllDashboards() {
        try {
            this.state.loading = true;
            const result = await this.orm.call(
                "smart.analytics.dashboard",
                "get_all_dashboards",
                []
            );
            this.state.dashboards = result;
            // Find the index of the current dashboard
            const currentIndex = result.findIndex(dash => dash.id === parseInt(this.state.dashboard_id));
            this.state.currentIndex = currentIndex !== -1 ? currentIndex : 0;
            this.state.dashboard = result[this.state.currentIndex];
            this.state.loading = false;
        } catch (error) {
            this.state.error = error.message || "An error occurred while loading dashboards.";
            this.state.loading = false;
        }
    }

    // Navigate to the previous dashboard
    previousDashboard() {
        if (this.state.currentIndex > 0) {
            this.state.currentIndex--;
            this.state.dashboard = this.state.dashboards[this.state.currentIndex];
            this.updateSessionStorage();
        }
    }

    // Navigate to the next dashboard
    nextDashboard() {
        if (this.state.currentIndex < this.state.dashboards.length - 1) {
            this.state.currentIndex++;
            this.state.dashboard = this.state.dashboards[this.state.currentIndex];
            this.updateSessionStorage();
        }
    }

    // Update session storage with current dashboard information
    updateSessionStorage() {
        sessionStorage.setItem('currentDashboardId', this.state.dashboard.id);
        sessionStorage.setItem('currentDashboardName', this.state.dashboard.name);
    }

    // Return to the dashboard kanban view
    returnToKanban() {
        this.action.doAction({
            type: 'ir.actions.client',
            tag: 'smart_analytics_dashboard',
            target: 'main'
        });
    }

    // Open dashboard settings
    openDashboardSettings() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'smart.analytics.dashboard',
            name: `Dashboard Settings - ${this.state.dashboard.name}`,
            views: [[false, 'list'], [false, 'form']],
            target: 'current',
            flags: {
                withControlPanel: true,
                hideBreadcrumbs: false,
            },
        }, {
            clear_breadcrumbs: false,
            pushState: true,
        });
    }

    // Capture screenshot and open email wizard
    async captureAndSendScreenshot() {
        try {
            // Capture the current tab using MediaDevices API
            const stream = await navigator.mediaDevices.getDisplayMedia({preferCurrentTab: true});
            const video = document.createElement('video');
            video.srcObject = stream;
            await video.play();

            // Create a canvas and draw the video frame
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);

            // Convert canvas to base64 image data
            const screenshot = canvas.toDataURL('image/png').split(',')[1]; // Get base64 data without mime type
            stream.getTracks().forEach(track => track.stop());

            // Open email wizard with screenshot data
            this.env.services.action.doAction({
                type: 'ir.actions.act_window',
                res_model: 'dashboard.email.wizard',
                view_mode: 'form',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
                context: {
                    'default_dashboard_id': this.state.dashboard.id,
                    'default_dashboard_name': this.state.dashboard.name,
                    'default_screenshot': screenshot
                }
            });
        } catch (error) {
            console.error("Error capturing screenshot:", error);
        }
    }
}

// Set the component template
SmartAnalyticsDashboardIframe.template = "SmartanalyticsDashboardIframe";

// Register the component in the actions registry
registry.category("actions").add("smart_analytics_dashboard_iframe", SmartAnalyticsDashboardIframe);
