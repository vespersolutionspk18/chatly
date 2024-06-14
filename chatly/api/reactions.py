import json

import frappe
from frappe import _


@frappe.whitelist(methods=["POST"])
def react(message_id: str, reaction: str):
	"""
	API to react/unreact to a message.
	Checks if the user can react to the message
	First checks if the user has already reacted to the message.
	If yes, then unreacts (deletes), else reacts (creates).
	"""

	channel_id = frappe.get_cached_value("Chatly Message", message_id, "channel_id")
	channel_type = frappe.get_cached_value("Chatly Channel", channel_id, "type")

	if channel_type == "Private":
		if not frappe.db.exists(
			"Chatly Channel Member", {"channel_id": channel_id, "user_id": frappe.session.user}
		):
			frappe.throw(_("You do not have permission to react to this message"), frappe.PermissionError)
	reaction_escaped = reaction.encode("unicode-escape").decode("utf-8").replace("\\u", "")
	user = frappe.session.user
	existing_reaction = frappe.db.exists(
		"Chatly Message Reaction",
		{"message": message_id, "owner": user, "reaction_escaped": reaction_escaped},
	)

	if existing_reaction:
		# Why not use frappe.db.delete?
		# Because frappe won't run the controller method for 'after_delete' if we do so,
		# and we need to calculate the new count of reactions for our message
		frappe.get_doc("Chatly Message Reaction", existing_reaction).delete(delete_permanently=True)

	else:
		frappe.get_doc(
			{
				"doctype": "Chatly Message Reaction",
				"reaction": reaction,
				"message": message_id,
				"owner": user,
			}
		).insert(ignore_permissions=True)
	return "Ok"


def calculate_message_reaction(message_id):

	reactions = frappe.get_all(
		"Chatly Message Reaction",
		fields=["owner", "reaction"],
		filters={"message": message_id},
		order_by="reaction_escaped",
	)

	total_reactions = {}

	for reaction_item in reactions:
		if reaction_item.reaction in total_reactions:
			existing_reaction = total_reactions[reaction_item.reaction]
			new_users = existing_reaction.get("users")
			new_users.append(reaction_item.owner)
			total_reactions[reaction_item.reaction] = {
				"count": existing_reaction.get("count") + 1,
				"users": new_users,
				"reaction": reaction_item.reaction,
			}

		else:
			total_reactions[reaction_item.reaction] = {
				"count": 1,
				"users": [reaction_item.owner],
				"reaction": reaction_item.reaction,
			}
	channel_id = frappe.get_cached_value("Chatly Message", message_id, "channel_id")
	frappe.db.set_value(
		"Chatly Message",
		message_id,
		"message_reactions",
		json.dumps(total_reactions),
		update_modified=False,
	)
	frappe.publish_realtime(
		"message_reacted",
		{
			"channel_id": channel_id,
			"sender": frappe.session.user,
			"message_id": message_id,
			"reactions": json.dumps(total_reactions),
		},
		doctype="Chatly Channel",
		docname=channel_id,  # Adding this to automatically add the room for the event via Frappe
		after_commit=False,
	)
