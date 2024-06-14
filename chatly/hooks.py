from . import __version__ as app_version

app_name = "chatly"
app_title = "Chatly"
app_publisher = "The Commit Company (Algocode Technologies Pvt. Ltd.)"
app_description = "Messaging Application"
app_email = "support@thecommit.company"
app_license = "AGPLv3"
source_link="https://github.com/The-Commit-Company/Chatly"
app_logo = "/assets/chatly/chatly-logo.png"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "chatly.bundle.css"
# app_include_css = "/assets/chatly/css/chatly.css"
# app_include_js = "/assets/chatly/js/chatly.js"                 ]
app_include_js = "chatly.bundle.js"


sounds = [
	{
		"name": "chatly_notification",
		"src": "/assets/chatly/sounds/chatly_notification.mp3",
		"volume": 0.2,
	},
]

extend_bootinfo = "chatly.boot.boot_session"
# include js, css files in header of web template
# web_include_css = "/assets/chatly/css/chatly.css"
# web_include_js = "/assets/chatly/js/chatly.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "chatly/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# "Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# "methods": "chatly.utils.jinja_methods",
# "filters": "chatly.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "chatly.install.before_install"
after_install = "chatly.install.after_install"
# after_sync = ""

# Uninstallation
# ------------

# before_uninstall = "chatly.uninstall.before_uninstall"
after_uninstall = "chatly.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "chatly.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# "ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"User": {
		"after_insert": "chatly.chatly.doctype.chatly_user.chatly_user.add_user_to_chatly",
		"on_update": "chatly.chatly.doctype.chatly_user.chatly_user.add_user_to_chatly",
		"on_trash": "chatly.chatly.doctype.chatly_user.chatly_user.remove_user_from_chatly",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# "all": [
# "chatly.tasks.all"
# ],
# "daily": [
# "chatly.tasks.daily"
# ],
# "hourly": [
# "chatly.tasks.hourly"
# ],
# "weekly": [
# "chatly.tasks.weekly"
# ],
# "monthly": [
# "chatly.tasks.monthly"
# ],
# }

# Testing
# -------

# before_tests = "chatly.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# "frappe.desk.doctype.event.event.get_events": "chatly.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# "Task": "chatly.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

ignore_links_on_delete = ["Chatly Message"]


# User Data Protection
# --------------------

# user_data_fields = [
# {
# "doctype": "{doctype_1}",
# "filter_by": "{filter_by}",
# "redact_fields": ["{field_1}", "{field_2}"],
# "partial": 1,
# },
# {
# "doctype": "{doctype_2}",
# "filter_by": "{filter_by}",
# "partial": 1,
# },
# {
# "doctype": "{doctype_3}",
# "strict": False,
# },
# {
# "doctype": "{doctype_4}"
# }
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# "chatly.auth.validate"
# ]

additional_timeline_content = {"*": ["chatly.api.chatly_message.get_timeline_message_content"]}

website_route_rules = [
	{"from_route": "/chatly/<path:app_path>", "to_route": "chatly"},
	{"from_route": "/chatly_mobile/<path:app_path>", "to_route": "chatly"},
]

permission_query_conditions = {
	"Chatly Channel": "chatly.permissions.chatly_channel_query",
	"Chatly Message": "chatly.permissions.chatly_message_query",
	"Chatly Poll Vote": "chatly.permissions.chatly_poll_vote_query",
}

has_permission = {
	"Chatly Channel": "chatly.permissions.channel_has_permission",
	"Chatly Channel Member": "chatly.permissions.channel_member_has_permission",
	"Chatly Message": "chatly.permissions.message_has_permission",
	"Chatly Poll Vote": "chatly.permissions.chatly_poll_vote_has_permission",
	"Chatly Poll": "chatly.permissions.chatly_poll_has_permission",
	"Chatly User": "chatly.permissions.chatly_user_has_permission",
}

on_session_creation = "chatly.api.user_availability.set_user_active"
on_logout = "chatly.api.user_availability.set_user_inactive"

export_python_type_annotations = True
