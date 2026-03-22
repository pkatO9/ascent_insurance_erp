app_name = "ascent_insurance_erp"
app_title = "Ascent Insurance Erp"
app_publisher = "Ascent"
app_description = "ERP for insurance intermediators"
app_email = "ascent.tech@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "ascent_insurance_erp",
# 		"logo": "/assets/ascent_insurance_erp/logo.png",
# 		"title": "Ascent Insurance Erp",
# 		"route": "/ascent_insurance_erp",
# 		"has_permission": "ascent_insurance_erp.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ascent_insurance_erp/css/ascent_insurance_erp.css"
# app_include_js = "/assets/ascent_insurance_erp/js/ascent_insurance_erp.js"

# include js, css files in header of web template
# web_include_css = "/assets/ascent_insurance_erp/css/ascent_insurance_erp.css"
# web_include_js = "/assets/ascent_insurance_erp/js/ascent_insurance_erp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ascent_insurance_erp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Lead" : "ascent_insurance_erp/public/js/lead.js",
	"Policy Proposal": "ascent_insurance_erp/public/js/policy_proposal.js",
	"Policy": "ascent_insurance_erp/public/js/policy.js",
	"Sales Agent": "ascent_insurance_erp/public/js/sales_agent.js",
	"Client": "ascent_insurance_erp/public/js/client.js",
	"Lead Enquiry": "ascent_insurance_erp/public/js/lead_enquiry.js"
}

doctype_list_js = {
	"Lead": "public/js/lead_list.js",
	"Policy": "ascent_insurance_erp/ascent_insurance_erp/doctype/policy/policy_list.js"
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ascent_insurance_erp/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ascent_insurance_erp.utils.jinja_methods",
# 	"filters": "ascent_insurance_erp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ascent_insurance_erp.install.before_install"
# after_install = "ascent_insurance_erp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ascent_insurance_erp.uninstall.before_uninstall"
# after_uninstall = "ascent_insurance_erp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ascent_insurance_erp.utils.before_app_install"
# after_app_install = "ascent_insurance_erp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ascent_insurance_erp.utils.before_app_uninstall"
# after_app_uninstall = "ascent_insurance_erp.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ascent_insurance_erp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

fixtures = [
    {"dt": "Custom Field", "filters": [["dt", "in", ["Lead"]]]},
    {"dt": "Property Setter", "filters": [["doc_type", "in", ["Lead"]]]},
    {"dt": "Kanban Board", "filters": [["kanban_board_name", "in", ["Lead Pipeline"]]]},
    {"dt": "LOB"},
    {"dt": "Policy Type"},
    {"dt": "Plan Name"},
    {"dt": "Plan Option"},
    {"dt": "Sales Agent"},
    {"dt": "Referral Source"},
    {"dt": "Client"},
    {"dt": "Lead Enquiry"}
]

doc_events = {
	"Lead": {
		"validate": "ascent_insurance_erp.ascent_insurance_erp.lead.validate",
		"before_insert": "ascent_insurance_erp.ascent_insurance_erp.lead.before_insert"
	},
	"Policy Proposal": {
		"validate": "ascent_insurance_erp.ascent_insurance_erp.doctype.policy_proposal.policy_proposal.validate_hook",
		"on_submit": "ascent_insurance_erp.ascent_insurance_erp.doctype.policy_proposal.policy_proposal.on_submit_hook",
		"on_update": "ascent_insurance_erp.ascent_insurance_erp.doctype.policy_proposal.policy_proposal.on_update_hook"
	}
}



# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"ascent_insurance_erp.ascent_insurance_erp.tasks.update_policy_statuses"
	]
}

# Testing
# -------

# before_tests = "ascent_insurance_erp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ascent_insurance_erp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ascent_insurance_erp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ascent_insurance_erp.utils.before_request"]
# after_request = ["ascent_insurance_erp.utils.after_request"]

# Job Events
# ----------
# before_job = ["ascent_insurance_erp.utils.before_job"]
# after_job = ["ascent_insurance_erp.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ascent_insurance_erp.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

