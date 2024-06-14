import frappe


def execute():
	"""Creating Chatly Users for existing users with the "Chatly User" role."""

	# In Chatly v1.2, we introduced the "Chatly User" doctype.
	#  Reference: [#427](https://github.com/The-Commit-Company/Chatly/issues/427)
	# This doctype is used to store the user's profile picture and full name.
	# However, existing users with the "Chatly User" role will not have a corresponding Chatly User record.
	# This patch creates Chatly Users for all users with the "Chatly User" role.
	users = frappe.get_all(
		"User",
		filters=[["name", "not in", ["Guest"]], ["Has Role", "role", "=", "Chatly User"]],
	)

	for user in users:
		if not frappe.db.exists("Chatly User", {"user": user.name}):
			chatly_user = frappe.new_doc("Chatly User")
			chatly_user.user = user.name
			chatly_user.insert()
