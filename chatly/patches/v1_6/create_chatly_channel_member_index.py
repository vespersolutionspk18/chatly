from chatly.chatly_channel_management.doctype.chatly_channel_member.chatly_channel_member import (
	on_doctype_update,
)


def execute():
	# Indexing all Chatly Channel Members
	on_doctype_update()
