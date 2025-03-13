from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import Complaint, BuildingGroup
from .views import create_groups
from django.utils import timezone
from django.urls import reverse

class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}

        self.user = User.objects.create_user(**self.credentials)
        self.client.login(username=self.credentials['username'], password=self.credentials['password'])
        self.response = self.client.get('/login/', follow=True)

    def test_user_authentication(self):
        self.assertTrue(self.response.context['user'].is_authenticated)

class ComplaintModelTest(TestCase):
    def test_complaint_creation(self):
        complaint = Complaint.objects.create(
            complaint_title="Loud Noises at Night",
            type_complaint=Complaint.ComplaintType.NOISE_COMPLAINT,
            sent_date= timezone.now(),
            incident_date= timezone.now(),
            location_address="123 Main St",
            incident_description="There was a loud party next door."
        )
        self.assertTrue(isinstance(complaint, Complaint))
        self.assertEqual(complaint.complaint_status, Complaint.ComplaintStatus.NEW)


class BuildingGroupTest(TestCase):
    def test_building_group_creation(self):
        group = BuildingGroup.objects.create(name="Test Building Group")
        self.assertTrue(isinstance(group, BuildingGroup))
        self.assertEqual(group.name, "Test Building Group")

class HomePageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')


class AnonymousFormAccessTest(TestCase):
    def test_anonymous_form_access(self):
        response = self.client.get(reverse('whistleblower:n-a-complaint'))
        self.assertEqual(response.status_code, 200)


class AdminReportViewTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_staff=True)
        self.client.login(username='admin', password='adminpass')
        self.complaint = Complaint.objects.create(
            complaint_title="Urgent: Water Leak",
            type_complaint=Complaint.ComplaintType.MAINTENANCE,
            sent_date= timezone.now(),
            incident_date= timezone.now(),
            location_address="456 Real Street",
            incident_description="Major water leak in ceiling."
        )

    def test_view_report_as_admin(self):
        response = self.client.get(reverse('whistleblower:report_view', kwargs={'pk': self.complaint.id}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Major water leak in ceiling.', response.content.decode())


class AdminAccessControlTest(TestCase):
    def setUp(self):
        if Group.objects.count() < 3:
            create_groups()


        self.user = User.objects.create_user(username='regularuser', password='userpass')
        self.user.groups.add(Group.objects.get(name="User"))

        self.admin = User.objects.create_user(username='adminuser', password='adminpass')
        self.admin.groups.add(Group.objects.get(name="Admin"))
    
    def test_admin_page_access(self):
        self.client.login(username='regularuser', password='userpass')
        response = self.client.get(reverse('whistleblower:home_admin'))
        self.assertNotEqual(response.status_code, 200)  # Expecting redirect or forbidden status
        
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.get(reverse('whistleblower:home_admin'))
        self.assertEqual(response.status_code, 200)


class AnonymousComplaintFormValidationTest(TestCase):
    def test_anonymous_form_validation(self):
        form_data = {
            'complaint_title': '',  
            'type_complaint': Complaint.ComplaintType.NOISE_COMPLAINT.value,
            'incident_date': timezone.now().date().isoformat(),
            'location_address': '123 Fake Street'
        }
        response = self.client.post(reverse('whistleblower:n-a-complaint'), form_data)
        self.assertNotEqual(response.status_code, 302)  
        self.assertTrue('This field is required.' in response.content.decode()) 
        

class UserGroupAssignmentTest(TestCase):
    def setUp(self):
        if Group.objects.count() < 3:
            create_groups()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_group_assignment(self):
        self.client.login(username='testuser', password='testpass')

        response = self.client.get(reverse('whistleblower:level_admin'))
        self.user.refresh_from_db() 
        self.assertTrue(self.user.groups.filter(name='Admin').exists())

        response = self.client.get(reverse('whistleblower:level_user'))
        self.user.refresh_from_db()  
        self.assertTrue(self.user.groups.filter(name='User').exists())


class BuildingGroupJoinTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='joinuser', password='joinpass')
        self.group = BuildingGroup.objects.create(name="Joinable Group")
        self.client.login(username='joinuser', password='joinpass')

    def test_building_group_join(self):
        response = self.client.post(reverse('whistleblower:join_group'), {'building_code': self.group.id})
        self.user.refresh_from_db()  
        self.assertTrue(self.group.users.filter(id=self.user.id).exists())


       
