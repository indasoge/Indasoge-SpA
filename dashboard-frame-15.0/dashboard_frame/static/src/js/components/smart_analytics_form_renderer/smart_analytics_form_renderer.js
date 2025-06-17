/** @odoo-module **/

// Import necessary Owl components and Odoo services
const { Component, onMounted, useState } = owl;
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

// Define the main component for Smart Analytics Dashboard
class SmartAnalyticsDashboard extends Component {
    setup() {
        // Initialize ORM and action services
        this.orm = useService("orm");
        this.action = useService("action");

        // Set up reactive state
        this.state = useState({
            dashboards: [],
            loading: true,
            error: null
        });

        // Load data when component is mounted
        onMounted(() => {
            this.loadData();
        });
    }

    // Fetch all dashboards from the server
    async loadData() {
        try {
            this.state.loading = true;
            // Call the ORM to get all dashboards
            const result = await this.orm.call(
                "smart.analytics.dashboard",
                "get_all_dashboards",
                []
            );
            // Update state with fetched dashboards
            this.state.dashboards = result;
        } catch (error) {
            // Handle any errors that occur during data fetching
            this.state.error = error.message || "An error occurred while loading data.";
            console.error("Error loading data:", error);
        } finally {
            // Set loading to false regardless of success or failure
            this.state.loading = false;
        }
    }

    // Open the iframe view for a specific dashboard
    openDashboardIframe(dashboardId, dashboardName) {
        // Store the dashboard ID in sessionStorage
        sessionStorage.setItem('currentDashboardId', dashboardId);
        sessionStorage.setItem('currentDashboardName', dashboardName);

        // Trigger the action to open the iframe view
        this.action.doAction({
            type: 'ir.actions.client',
            tag: 'smart_analytics_dashboard_iframe',
            params: {
                dashboard_id: dashboardId,
                dashboard_name: dashboardName
            },
            target: 'current'
        });
    }
}

// Set the component template
SmartAnalyticsDashboard.template = "SmartanalyticsDashboard";

// Register the component in the actions registry
registry.category("actions").add("smart_analytics_dashboard", SmartAnalyticsDashboard);
