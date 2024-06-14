# Copyright (c) 2023, The Commit Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

from chatly.notification import subscribe_user_to_topic, unsubscribe_user_to_topic


class ChatlyChannelMember(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		allow_notifications: DF.Check
		channel_id: DF.Link
		is_admin: DF.Check
		last_visit: DF.Datetime
		user_id: DF.Link
	# end: auto-generated types

	def before_validate(self):
		self.last_visit = frappe.utils.now()

	def before_insert(self):
		# 1. A user cannot be a member of a channel more than once
		if frappe.db.exists(
			"Chatly Channel Member", {"channel_id": self.channel_id, "user_id": self.user_id}
		):
			frappe.throw(_("You are already a member of this channel"), frappe.DuplicateEntryError)
		# if there are no members in the channel, then the member becomes admin
		if frappe.db.count("Chatly Channel Member", {"channel_id": self.channel_id}) == 0:
			self.is_admin = 1

		self.allow_notifications = 1

	def after_delete(self):
		if (
			frappe.db.count("Chatly Channel Member", {"channel_id": self.channel_id}) == 0
			and frappe.db.get_value("Chatly Channel", self.channel_id, "type") == "Private"
		):
			frappe.db.set_value("Chatly Channel", self.channel_id, "is_archived", 1)
		if (
			self.get_admin_count() == 0
			and frappe.db.count("Chatly Channel Member", {"channel_id": self.channel_id}) > 0
		):
			first_member = frappe.db.get_value(
				"Chatly Channel Member",
				{"channel_id": self.channel_id},
				["name"],
				as_dict=1,
				order_by="creation",
			)
			frappe.db.set_value("Chatly Channel Member", first_member.name, "is_admin", 1)

	def on_trash(self):
		# if the leaving member is admin, then the first member becomes new admin
		if (
			self.is_admin == 1
			and frappe.db.count("Chatly Channel Member", {"channel_id": self.channel_id}) > 0
		):
			first_member = frappe.db.get_value(
				"Chatly Channel Member",
				{"channel_id": self.channel_id},
				["name"],
				as_dict=1,
				order_by="creation",
			)
			frappe.db.set_value("Chatly Channel Member", first_member.name, "is_admin", 1)

		if self.flags.ignore_permissions:
			return
		if not self.check_if_user_is_member():
			frappe.throw(
				_("You don't have permission to remove members from this channel"),
				frappe.PermissionError,
			)

	def check_if_user_is_member(self):
		is_member = True
		channel = frappe.db.get_value("Chatly Channel", self.channel_id, ["type", "owner"], as_dict=True)
		if channel.type == "Private":
			# A user can only add members to a private channel if they are themselves member of the channel or if they are the owner of a new channel
			if (
				channel.owner == frappe.session.user
				and frappe.db.count("Chatly Channel Member", {"channel_id": self.channel_id}) == 0
			):
				# User is the owner of a channel and there are no members in the channel
				pass
			elif frappe.db.exists(
				"Chatly Channel Member",
				{"channel_id": self.channel_id, "user_id": frappe.session.user},
			):
				# User is a member of the channel
				pass
			elif frappe.session.user == "Administrator":
				# User is Administrator
				pass
			else:
				is_member = False
		return is_member

	def after_insert(self):
		"""
		Subscribe the user to the topic if the channel is not a DM
		"""
		is_direct_message = frappe.db.get_value("Chatly Channel", self.channel_id, "is_direct_message")

		if not is_direct_message and self.allow_notifications:
			subscribe_user_to_topic(self.channel_id, self.user_id)

	def on_update(self):
		"""
		Check if the notification preference is changed and update the subscription
		"""
		old_doc = self.get_doc_before_save()
		if old_doc:
			if old_doc.allow_notifications != self.allow_notifications:
				is_direct_message = frappe.db.get_value("Chatly Channel", self.channel_id, "is_direct_message")

				if not is_direct_message:
					if self.allow_notifications:
						subscribe_user_to_topic(self.channel_id, self.user_id)
					else:
						unsubscribe_user_to_topic(self.channel_id, self.user_id)

	def get_admin_count(self):
		return frappe.db.count("Chatly Channel Member", {"channel_id": self.channel_id, "is_admin": 1})


def on_doctype_update():
	"""
	Add indexes to Chatly Channel Member table
	"""
	# Index the selector (channel or message type) first for faster queries (less rows to sort in the next step)
	frappe.db.add_index("Chatly Channel Member", ["channel_id", "user_id"])
