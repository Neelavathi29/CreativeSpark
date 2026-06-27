from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import (
    Task, Milestone, CalendarEvent,
    Workspace, WorkspaceMember, WorkspaceDocument,
)
from apps.ideas.models import StartupIdea

User = get_user_model()


class ProductivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="produser", password="testpass123"
        )
        self.idea = StartupIdea.objects.create(
            user=self.user,
            startup_name="ProdApp",
            founder_name="Tester",
            industry="technology",
            problem_statement="P",
            proposed_solution="S",
            target_customers="M",
            business_model="SaaS",
            revenue_model="Sub",
            competitor_analysis="N",
            unique_selling_proposition="X",
            required_investment=10000,
            team_members="A",
            expected_timeline="3m",
        )

    def test_create_task(self):
        task = Task.objects.create(
            user=self.user,
            title="Setup Django",
            priority="high",
            idea=self.idea,
        )
        self.assertEqual(str(task), "Setup Django")
        self.assertEqual(task.status, "todo")

    def test_create_milestone(self):
        ms = Milestone.objects.create(
            idea=self.idea,
            title="MVP Launch",
            target_date="2026-08-01",
        )
        self.assertEqual(
            str(ms), "ProdApp - MVP Launch"
        )

    def test_calendar_event(self):
        event = CalendarEvent.objects.create(
            user=self.user,
            title="Team Meeting",
            start_date="2026-07-15T10:00:00Z",
            event_type="meeting",
        )
        self.assertEqual(str(event), "Team Meeting")

    def test_workspace(self):
        ws = Workspace.objects.create(
            name="My Workspace",
            created_by=self.user,
        )
        self.assertEqual(str(ws), "My Workspace")

    def test_workspace_member(self):
        ws = Workspace.objects.create(
            name="Team Space",
            created_by=self.user,
        )
        member = WorkspaceMember.objects.create(
            workspace=ws, user=self.user, role="admin"
        )
        self.assertTrue("admin" in str(member))

    def test_workspace_document(self):
        ws = Workspace.objects.create(
            name="Docs",
            created_by=self.user,
        )
        doc = WorkspaceDocument.objects.create(
            workspace=ws,
            title="Plan",
            uploaded_by=self.user,
        )
        self.assertEqual(str(doc), "Plan")


class ProductivityViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="prodview", password="testpass123"
        )
        self.idea = StartupIdea.objects.create(
            user=self.user,
            startup_name="ViewApp",
            founder_name="Tester",
            industry="technology",
            problem_statement="P",
            proposed_solution="S",
            target_customers="M",
            business_model="SaaS",
            revenue_model="Sub",
            competitor_analysis="N",
            unique_selling_proposition="X",
            required_investment=10000,
            team_members="A",
            expected_timeline="3m",
        )

    def test_task_board_login_required(self):
        response = self.client.get(reverse("task_board"))
        self.assertNotEqual(response.status_code, 200)

    def test_task_board_authenticated(self):
        self.client.login(
            username="prodview", password="testpass123"
        )
        response = self.client.get(reverse("task_board"))
        self.assertEqual(response.status_code, 200)

    def test_add_task(self):
        self.client.login(
            username="prodview", password="testpass123"
        )
        response = self.client.post(
            reverse("add_task"),
            {
                "title": "New Task",
                "priority": "medium",
                "idea": self.idea.pk,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)

    def test_update_task_status(self):
        self.client.login(
            username="prodview", password="testpass123"
        )
        task = Task.objects.create(
            user=self.user, title="My Task"
        )
        response = self.client.get(
            reverse(
                "update_task_status",
                args=[task.pk, "done"],
            )
        )
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.status, "done")

    def test_delete_task(self):
        self.client.login(
            username="prodview", password="testpass123"
        )
        task = Task.objects.create(
            user=self.user, title="Delete Me"
        )
        response = self.client.get(
            reverse("delete_task", args=[task.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    def test_calendar_view(self):
        self.client.login(
            username="prodview", password="testpass123"
        )
        response = self.client.get(reverse("calendar_view"))
        self.assertEqual(response.status_code, 200)

    def test_workspace_list(self):
        self.client.login(
            username="prodview", password="testpass123"
        )
        response = self.client.get(reverse("workspace_list"))
        self.assertEqual(response.status_code, 200)

    def test_workspace_create(self):
        self.client.login(
            username="prodview", password="testpass123"
        )
        response = self.client.post(
            reverse("workspace_create"),
            {"name": "New Space"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Workspace.objects.count(), 1)

    def test_workspace_detail(self):
        self.client.login(
            username="prodview", password="testpass123"
        )
        ws = Workspace.objects.create(
            name="Detail Space",
            created_by=self.user,
        )
        WorkspaceMember.objects.create(
            workspace=ws, user=self.user, role="admin"
        )
        response = self.client.get(
            reverse("workspace_detail", args=[ws.pk])
        )
        self.assertEqual(response.status_code, 200)
