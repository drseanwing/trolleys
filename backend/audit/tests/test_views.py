"""Tests for audit app views."""
from django.test import TestCase, Client
from django.urls import reverse

from .factories import (
    create_audit, create_audit_period, create_issue, create_location,
    create_service_line, create_user, setup_all_roles,
)


class AuthenticationTest(TestCase):
    """Test that all views require authentication."""

    def setUp(self):
        self.client = Client()

    def test_dashboard_redirects_anonymous(self):
        response = self.client.get(reverse('audit:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_trolley_list_redirects_anonymous(self):
        response = self.client.get(reverse('audit:trolley_list'))
        self.assertEqual(response.status_code, 302)

    def test_audit_list_redirects_anonymous(self):
        response = self.client.get(reverse('audit:audit_list'))
        self.assertEqual(response.status_code, 302)

    def test_issue_list_redirects_anonymous(self):
        response = self.client.get(reverse('audit:issue_list'))
        self.assertEqual(response.status_code, 302)


class DashboardViewTest(TestCase):
    """Tests for DashboardView."""

    def setUp(self):
        setup_all_roles()
        self.user = create_user(groups=['Viewer'])
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_dashboard_renders(self):
        response = self.client.get(reverse('audit:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'audit/dashboard.html')

    def test_dashboard_context(self):
        response = self.client.get(reverse('audit:dashboard'))
        self.assertIn('total_locations', response.context)
        self.assertIn('total_audits', response.context)
        self.assertIn('open_issues', response.context)


class TrolleyListViewTest(TestCase):
    """Tests for TrolleyListView."""

    def setUp(self):
        setup_all_roles()
        self.user = create_user(groups=['Viewer'])
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        self.service_line = create_service_line()
        self.location = create_location(service_line=self.service_line)

    def test_trolley_list_renders(self):
        response = self.client.get(reverse('audit:trolley_list'))
        self.assertEqual(response.status_code, 200)

    def test_trolley_list_filter_by_service_line(self):
        response = self.client.get(
            reverse('audit:trolley_list'),
            {'service_line': str(self.service_line.pk)},
        )
        self.assertEqual(response.status_code, 200)

    def test_trolley_list_search(self):
        response = self.client.get(
            reverse('audit:trolley_list'),
            {'q': 'Emergency'},
        )
        self.assertEqual(response.status_code, 200)


class RoleAccessTest(TestCase):
    """Test role-based access control."""

    def setUp(self):
        setup_all_roles()

    def test_viewer_cannot_create_issue(self):
        user = create_user(username='viewer', groups=['Viewer'])
        self.client.login(username='viewer', password='testpass123')
        response = self.client.get(reverse('audit:issue_create'))
        self.assertEqual(response.status_code, 403)

    def test_auditor_can_create_issue(self):
        user = create_user(username='auditor', groups=['Auditor'])
        self.client.login(username='auditor', password='testpass123')
        response = self.client.get(reverse('audit:issue_create'))
        self.assertEqual(response.status_code, 200)

    def test_viewer_cannot_access_selection(self):
        user = create_user(username='viewer2', groups=['Viewer'])
        self.client.login(username='viewer2', password='testpass123')
        response = self.client.get(reverse('audit:random_selection'))
        self.assertEqual(response.status_code, 403)

    def test_educator_can_access_selection(self):
        user = create_user(username='educator', groups=['MERT Educator'])
        self.client.login(username='educator', password='testpass123')
        response = self.client.get(reverse('audit:random_selection'))
        self.assertEqual(response.status_code, 200)
