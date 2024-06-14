# Copyright (c) 2023, The Commit Company and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ChatlySettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		auto_add_system_users: DF.Check
		show_chatly_on_desk: DF.Check
		tenor_api_key: DF.Data | None
	# end: auto-generated types

	pass
