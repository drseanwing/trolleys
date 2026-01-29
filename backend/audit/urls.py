"""
URL configuration for the audit app.
"""

from django.urls import path

from . import views

app_name = 'audit'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),

    # Trolley / Location management
    path('trolleys/', views.TrolleyListView.as_view(), name='trolley_list'),
    path('trolleys/<uuid:pk>/', views.TrolleyDetailView.as_view(), name='trolley_detail'),
    path('trolleys/<uuid:pk>/edit/', views.TrolleyEditView.as_view(), name='trolley_edit'),

    # Audit management
    path('audits/', views.AuditListView.as_view(), name='audit_list'),
    path('audits/start/<uuid:location_id>/', views.AuditStartView.as_view(), name='audit_start'),
    path('audits/<uuid:pk>/', views.AuditDetailView.as_view(), name='audit_detail'),
    path('audits/<uuid:pk>/documents/', views.AuditDocumentsView.as_view(), name='audit_documents'),
    path('audits/<uuid:pk>/equipment/', views.AuditEquipmentView.as_view(), name='audit_equipment'),
    path('audits/<uuid:pk>/condition/', views.AuditConditionView.as_view(), name='audit_condition'),
    path('audits/<uuid:pk>/checks/', views.AuditChecksView.as_view(), name='audit_checks'),
    path('audits/<uuid:pk>/review/', views.AuditReviewView.as_view(), name='audit_review'),
    path('audits/<uuid:pk>/submit/', views.AuditSubmitView.as_view(), name='audit_submit'),

    # Issue management
    path('issues/', views.IssueListView.as_view(), name='issue_list'),
    path('issues/create/', views.IssueCreateView.as_view(), name='issue_create'),
    path('issues/<uuid:pk>/', views.IssueDetailView.as_view(), name='issue_detail'),
    path('issues/<uuid:pk>/transition/<str:action>/', views.IssueTransitionView.as_view(), name='issue_transition'),
    path('issues/<uuid:pk>/comment/', views.IssueCommentView.as_view(), name='issue_comment'),

    # Random Selection
    path('selection/', views.RandomSelectionView.as_view(), name='random_selection'),
    path('selection/generate/', views.GenerateSelectionView.as_view(), name='generate_selection'),

    # Reports
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('reports/compliance/', views.ComplianceReportView.as_view(), name='compliance_report'),
    path('reports/export/', views.ExportView.as_view(), name='export'),
]
