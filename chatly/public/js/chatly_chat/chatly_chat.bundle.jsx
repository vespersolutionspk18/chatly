import * as React from "react";
import { App } from "./App";
import { createRoot } from "react-dom/client";


class ChatlyChat {
	constructor({ wrapper }) {
		this.$wrapper = $(wrapper);

		this.init();
	}

	init() {
		this.setup_app();
	}

	setup_app() {
		// create and mount the react app
		const root = createRoot(this.$wrapper.get(0));
		root.render(<App />);
		this.$chatly_chat = root;
	}
}

frappe.provide("frappe.ui");
frappe.ui.ChatlyChat = ChatlyChat;
export default ChatlyChat;