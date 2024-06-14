import frappe
from frappe import _
from frappe.query_builder import Order

from chatly.api.chatly_users import get_current_chatly_user


@frappe.whitelist()
def get_all_channels(hide_archived=True):
	"""
	Fetches all channels where current user is a member - both channels and DMs
	To be used on the web app.
	"""

	if hide_archived == "false":
		hide_archived = False

	# 1. Get "channels" - public, open, private, and DMs
	channels = get_channel_list(hide_archived)

	# 3. For every channel, we need to fetch the peer's User ID (if it's a DM)
	parsed_channels = []
	for channel in channels:
		parsed_channel = {
			**channel,
			"peer_user_id": get_peer_user_id(
				channel.get("name"),
				channel.get("is_direct_message"),
				channel.get("is_self_message"),
			),
		}

		parsed_channels.append(parsed_channel)

	channel_list = [channel for channel in parsed_channels if not channel.get("is_direct_message")]
	dm_list = [channel for channel in parsed_channels if channel.get("is_direct_message")]

	return {"channels": channel_list, "dm_channels": dm_list}


def get_channel_list(hide_archived=False):
	"""
	get List of all channels where current user is a member (all includes public, private, open, and DM channels)
	"""
	channel = frappe.qb.DocType("Chatly Channel")
	channel_member = frappe.qb.DocType("Chatly Channel Member")

	query = (
		frappe.qb.from_(channel)
		.select(
			channel.name,
			channel.channel_name,
			channel.type,
			channel.channel_description,
			channel.is_archived,
			channel.is_direct_message,
			channel.is_self_message,
			channel.creation,
			channel.owner,
			channel.last_message_timestamp,
			channel.last_message_details,
		)
		.distinct()
		.left_join(channel_member)
		.on(channel.name == channel_member.channel_id)
		.where((channel.type != "Private") | (channel_member.user_id == frappe.session.user))
	)

	if hide_archived:
		query = query.where(channel.is_archived == 0)

	query = query.orderby(channel.last_message_timestamp, order=Order.desc)

	return query.run(as_dict=True)


@frappe.whitelist()
def get_last_message_details(channel_id: str):

	if frappe.has_permission(doctype="Chatly Channel", doc=channel_id, ptype="read"):
		last_message_timestamp = frappe.get_cached_value(
			"Chatly Channel", channel_id, "last_message_timestamp"
		)
		last_message_details = frappe.get_cached_value(
			"Chatly Channel", channel_id, "last_message_details"
		)

		return {
			"last_message_timestamp": last_message_timestamp,
			"last_message_details": last_message_details,
		}


@frappe.whitelist()
def get_channels(hide_archived=False):
	channels = get_channel_list(hide_archived)
	for channel in channels:
		peer_user_id = get_peer_user_id(
			channel.get("name"), channel.get("is_direct_message"), channel.get("is_self_message")
		)
		channel["peer_user_id"] = peer_user_id
		if peer_user_id:
			user_full_name = frappe.get_cached_value("User", peer_user_id, "full_name")
			channel["full_name"] = user_full_name
	return channels


def get_peer_user_id(channel_id, is_direct_message, is_self_message=False):
	"""
	For a given channel, fetches the user id of the peer
	"""
	if is_direct_message == 0:
		return None
	if is_self_message:
		return frappe.session.user
	return frappe.db.get_value(
		"Chatly Channel Member",
		{"channel_id": channel_id, "user_id": ["!=", frappe.session.user]},
		"user_id",
	)


@frappe.whitelist(methods=["POST"])
def create_direct_message_channel(user_id):
	"""
	Creates a direct message channel between current user and the user with user_id
	The user_id can be the peer or the user themself
	1. Check if a channel already exists between the two users
	2. If not, create a new channel
	3. Check if the user_id is the current user and set is_self_message accordingly
	"""
	# TODO: this logic might break if the user_id changes
	channel_name = frappe.db.get_value(
		"Chatly Channel",
		filters={
			"is_direct_message": 1,
			"channel_name": [
				"in",
				[frappe.session.user + " _ " + user_id, user_id + " _ " + frappe.session.user],
			],
		},
		fieldname="name",
	)
	if channel_name:
		return channel_name
	# create direct message channel with user and current user
	else:
		channel = frappe.get_doc(
			{
				"doctype": "Chatly Channel",
				"channel_name": frappe.session.user + " _ " + user_id,
				"is_direct_message": 1,
				"is_self_message": frappe.session.user == user_id,
			}
		)
		channel.insert()
		return channel.name


@frappe.whitelist(methods=["POST"])
def toggle_pinned_channel(channel_id):
	"""
	Toggles the pinned status of the channel
	"""
	chatly_user = get_current_chatly_user()
	pinned_channels = chatly_user.pinned_channels or []

	is_pinned = False
	for pin in pinned_channels:
		if pin.channel_id == channel_id:
			chatly_user.remove(pin)
			is_pinned = True
			break

	if not is_pinned:
		chatly_user.append("pinned_channels", {"channel_id": channel_id})

	chatly_user.save()

	return chatly_user
