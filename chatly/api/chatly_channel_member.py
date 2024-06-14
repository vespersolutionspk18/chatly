import frappe
from frappe import _

from chatly.utils import track_channel_visit


@frappe.whitelist()
def remove_channel_member(user_id, channel_id):
	# Get chatly channel member name where user_id and channel_id match
	member = frappe.db.get_value(
		"Chatly Channel Member", {"user_id": user_id, "channel_id": channel_id}, ["name"]
	)
	# Delete chatly channel member
	if member:
		frappe.delete_doc("Chatly Channel Member", member)
	else:
		frappe.throw(_("User is not a member of this channel"))

	return True


@frappe.whitelist(methods=["POST"])
def track_visit(channel_id):
	"""
	Track the last visit of the user to the channel.
	This is usually called when the user exits the channel (unmounts the component) after loading the latest messages in it.
	"""
	track_channel_visit(channel_id=channel_id, commit=True)
	return True
