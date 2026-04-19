/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class ShipiqoLifecycleWidget extends Component {
    static template = "shipiqo_shipping.LifecycleWidget";
    static props = ["*"];

    setup() {
        this.action = useService("action");
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        this.state = useState({ url: this.props.record.data.shipiqo_widget_url || "" });

        this._messageHandler = (event) => {
            const data = event.data;
            if (!data || typeof data !== "object" || !data.type) return;
            if (data.type === "shipiqo.rate.selected") {
                this.rpc(`/shipiqo/order/${this.props.record.resId}/select_rate`, data.payload || {})
                    .then(() => {
                        this.notification.add("Carrier added to order", { type: "success" });
                        this.props.record.load();
                    });
            } else if (data.type === "shipiqo.rate.skipped") {
                this.rpc(`/shipiqo/order/${this.props.record.resId}/skip_rate`, {})
                    .then(() => {
                        this.notification.add("Customer-arranged shipping noted", { type: "info" });
                        this.props.record.load();
                    });
            }
        };

        onMounted(() => window.addEventListener("message", this._messageHandler));
        onWillUnmount(() => window.removeEventListener("message", this._messageHandler));
    }
}

export const shipiqoLifecycleWidget = {
    component: ShipiqoLifecycleWidget,
    fieldDependencies: [{ name: "shipiqo_widget_url", type: "char" }],
};
registry.category("view_widgets").add("shipiqo_lifecycle_widget", shipiqoLifecycleWidget);
