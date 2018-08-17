from navmazing import NavigateToSibling
from wait_for import wait_for

from airgun.entities.base import BaseEntity
from airgun.navigation import NavigateStep, navigator
from airgun.views.rhai import (
    PlanBuilder,
    Planner,
    PlanEditView,
    PlanModalWindow
)


class PlanEntity(BaseEntity):

    def create(self, name, rules):
        view = self.navigate_to(self, "Add")
        view.name.fill(name)
        for rule in rules:
            view.rules_filter.fill(rule)
            view.actions[0][0].widget.fill(True)
        view.save.click()

    def delete(self, entity_name):
        view = self.navigate_to(
            self, "Details", entity_name=entity_name).plan(entity_name)
        wait_for(lambda: view.delete.is_displayed)
        view.delete.click()
        modal = PlanModalWindow(self.session.browser)
        modal.yes.click()

    def update(self, entity_name, values):
        view = self.navigate_to(
            self, "Details", entity_name=entity_name).plan(entity_name)
        view.edit.click()
        view = PlanEditView(self.session.browser)
        view.fill_with(values, on_change=view.save.click)


@navigator.register(PlanEntity, "All")
class AllPlans(NavigateStep):
    VIEW = Planner

    def step(self, *args, **kwargs):
        self.view.menu.select("Insights", "Planner")


@navigator.register(PlanEntity, "Add")
class AddPlan(NavigateStep):
    VIEW = PlanBuilder
    prerequisite = NavigateToSibling("All")

    def step(self, *args, **kwargs):
        self.parent.create_plan.click()
        wait_for(lambda: self.view.rules_filter.is_displayed, timeout=10)


@navigator.register(PlanEntity, "Details")
class PlanDetails(NavigateStep):
    VIEW = Planner
    prerequisite = NavigateToSibling("All")

    def step(self, *args, **kwargs):
        title = self.view.plan(kwargs["entity_name"]).title
        wait_for(lambda: title.is_displayed, timeout=10)
        self.view.plan(kwargs["entity_name"]).title.click()
