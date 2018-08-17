from widgetastic_patternfly import Button
from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import (
    Checkbox,
    ParametrizedView,
    Text,
    TextInput,
    View
)

from airgun.views.common import BaseLoggedInView
from airgun.widgets import SatTable


class Planner(BaseLoggedInView):
    create_plan = Text(".//a[@class='create-plan']")

    @ParametrizedView.nested
    class plan(ParametrizedView):
        PARAMETERS = ("plan_name", )
        ROOT = ParametrizedLocator(
            ".//h2[contains(normalize-space(.), {plan_name|quote})]/"
            "ancestor::div[contains(@id, 'maintenance-plan')]")

        delete = Text(".//i[@tooltip='Delete this plan']")
        edit = Text(".//i[@tooltip='Click to edit this plan']")
        run_playbook = Button("Run Playbook")
        export_csv = Button("Export CSV")
        add_actions = Button("Add actions")

    @property
    def is_displayed(self):
        return self.menu.currently_selected == ["Insights", "Planner"]


class PlanEditView(View):
    plan_name = TextInput(name="name")
    date = TextInput(name="date")
    start_time = TextInput(name="time")
    duration = TextInput(name="duration")
    cancel = Button("Cancel")
    save = Button("Save")


class PlanBuilder(BaseLoggedInView):
    name = TextInput(name="name")
    actions = SatTable(
        ".//div[contains(@class, 'maintenance-plan')]//table",
        column_widgets={0: Checkbox(locator=".//input")}
    )
    rules_filter = TextInput(
        locator=".//input[@placeholder='Filter by rule name']")
    cancel = Button("Cancel")
    save = Button("Save")

    @property
    def is_displayed(self):
        return self.menu.currently_selected == ["Insights", "Planner"]


class PlanModalWindow(View):
    yes = Text(".//button[contains(@class, 'swal2-confirm')]")
    cancel = Text(".//button[contains(@class, 'swal2-cancel')]")
