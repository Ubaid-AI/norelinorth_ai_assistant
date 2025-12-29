"""
Migration patch: Clean up old 'ai_assistant' app references

This patch handles migration from the old 'ai_assistant' app name
to the new 'norelinorth_ai_assistant' app name.
"""
import json

import frappe


def execute():
    """
    Clean up old 'ai_assistant' references in the database.

    This patch:
    1. Removes 'ai_assistant' from installed_apps global
    2. Updates Module Def to use new app name
    3. Updates Installed Application table
    """
    try:
        # 1. Fix installed_apps global in tabDefaultValue
        installed_apps_json = frappe.db.get_default("installed_apps")
        if installed_apps_json:
            installed_apps = json.loads(installed_apps_json)

            # Remove old app name if present
            if "ai_assistant" in installed_apps:
                installed_apps.remove("ai_assistant")
                print("Removed 'ai_assistant' from installed_apps")

            # Ensure new app name is present
            if "norelinorth_ai_assistant" not in installed_apps:
                installed_apps.append("norelinorth_ai_assistant")
                print("Added 'norelinorth_ai_assistant' to installed_apps")

            # Update the global value
            frappe.db.set_default("installed_apps", json.dumps(installed_apps))
            frappe.db.commit()
            print("Updated installed_apps global")

        # 2. Update Module Def if needed
        if frappe.db.exists("Module Def", "AI Assistant"):
            current_app = frappe.db.get_value("Module Def", "AI Assistant", "app_name")
            if current_app == "ai_assistant":
                frappe.db.set_value("Module Def", "AI Assistant", "app_name", "norelinorth_ai_assistant")
                frappe.db.commit()
                print("Updated Module Def app_name")

        # 3. Clean up Installed Application table
        if frappe.db.exists("Installed Application", {"app_name": "ai_assistant"}):
            frappe.db.delete("Installed Application", {"app_name": "ai_assistant"})
            frappe.db.commit()
            print("Removed old 'ai_assistant' from Installed Application")

        print("Migration from old app name completed successfully")

    except Exception as e:
        frappe.log_error(
            message=f"Error during migration: {str(e)}\n{frappe.get_traceback()}",
            title="AI Assistant Migration Error"
        )
        print(f"Migration note: {e}")
