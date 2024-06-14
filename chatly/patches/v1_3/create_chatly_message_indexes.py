from chatly.chatly_messaging.doctype.chatly_message.chatly_message import on_doctype_update


def execute():
	# Indexing all Chatly Messages
	on_doctype_update()
