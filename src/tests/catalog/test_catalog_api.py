from datetime import timedelta
from copy import deepcopy

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from catalog.models import (
    Categorie, Course, Module, Feature, Study, Filling, TargetAudience,
    Section, Lesson, GetToKnow
)
from skill.models import Client, HomeData, Leader, Switch
from skill.Controllers.Auth.auth import get_tokens_for_user
from .response_examples import course_data, module_data, home_data, clients


class TestCatalogAPI(APITestCase):
    def setUp(self):
        self.category = Categorie.objects.create(
            title='Microsoft',
            name=course_data['category'],
            mnemo='office',
            description='MS Office category description',
        )

        self.excel_course = Course.objects.create(
            name=course_data['name'],
            title='Microsoft',
            mnemo=course_data['mnemo'],
            description=course_data['description'],
            price=course_data['price'],
            old_price=course_data['oldPrice'],
            category=self.category,
            slogan_goal=course_data['sloganGoal']
        )

        self.basic_module = Module.objects.create(
            name=module_data['name'],
            price=module_data['price'],
            old_price=module_data['oldPrice'],
            time=1000,
            description=module_data['description'],
            full_description='Full description of a Basic module',
            mnemo=module_data['mnemo'],
            course=self.excel_course,
        )

        self.section_basic_1 = Section.objects.create(
            module=self.basic_module,
            name=module_data['sections'][0]['name']
        )

        self.lesson_basic_1 = Lesson.objects.create(
            section=self.section_basic_1,
            name=module_data['sections'][0]['lessons'][0]['name'],
            demo=module_data['sections'][0]['lessons'][0]['demo'],
            duration=timedelta(minutes=2)
        )

        self.lesson_basic_2 = Lesson.objects.create(
            section=self.section_basic_1,
            name=module_data['sections'][0]['lessons'][1]['name'],
            express=module_data['sections'][0]['lessons'][1]['express'],
            duration=timedelta(minutes=4, seconds=15)
        )

        self.feature_1 = Feature.objects.create(
            title=course_data['courseFeatures'][0]['title'],
            text=course_data['courseFeatures'][0]['text'],
            logo=course_data['courseFeatures'][0]['logo']
        )
        self.feature_1.courses.add(self.excel_course)
        self.feature_1.modules.add(self.basic_module)


        self.study_1 = Study.objects.create(
            topic=course_data['studyInCourse'][0]['topic'],
        )
        self.study_1.courses.add(self.excel_course)
        self.study_1.modules.add(self.basic_module)


        self.audience_1 = TargetAudience.objects.create(
            profession=course_data['targetAudience'][0]['profession'],
            logo=course_data['targetAudience'][0]['logo']
        )
        self.audience_1.courses.add(self.excel_course)


        self.filling = Filling.objects.create(
            title=course_data['filling'][0]['title'],
            logo=course_data['filling'][0]['logo']
        )
        self.filling.courses.add(self.excel_course)


        self.get_to_know = GetToKnow.objects.create(
            text=course_data['getToKnow'][0]['text']
        )
        self.get_to_know.courses.add(self.excel_course)


        self.home = HomeData.objects.create(
            font=home_data['font'],
            opportunities=home_data['opportunities'],
            why_us=home_data['why_us']
        )

        for client in clients:
            Client.objects.create(
                name=client['name'],
                logo=client['logo'],
                country='RU',
                home=self.home
            )

        self.switch = Switch.objects.create(
            name='leaders_auto_order',
            active=False
        )

        self.leader = Leader.objects.create(
            order='1',
            course=self.excel_course,
            autoupdate=self.switch,
            home=self.home
        )

    def set_credentials(self, user):
        tokens = get_tokens_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens['access'])

    def get_user(self):
        return User.objects.create_user('test_user', 'test@mail.com', 'secretPassword')

    def test_course_info_view_unauthenticated(self):
        response = self.client.get(reverse('course-info', kwargs={'mnemo': course_data['mnemo']}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, course_data)

    def test_course_info_view_authenticated(self):
        """
        Value of 'bought' field for modules that authenticated user has bought must be 'express' or 'full'
        """
        test_user = self.get_user()
        test_user.profile.purchased_modules.add(self.basic_module, through_defaults={'express': True})
        test_user.save()

        # set 'bought' value of a Basic module to True
        temp_course_data = deepcopy(course_data)
        temp_course_data['modules'][0]['bought'] = 'express'
        self.set_credentials(test_user)
        response = self.client.get(reverse('course-info', kwargs={'mnemo': temp_course_data['mnemo']}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, temp_course_data)

    def test_module_info_view_unauthenticated(self):
        response = self.client.get(reverse('module-info', kwargs={'mnemo': module_data['mnemo']}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, module_data)

    def test_module_info_lesson_completed(self):
        """For lessons that user have completed field 'completed' must be True"""
        test_user = self.get_user()
        test_user.profile.lessons.add(self.lesson_basic_1, through_defaults={'completed': True})
        test_user.save()

        temp_module_data = deepcopy(module_data)
        temp_module_data['sections'][0]['lessons'][0]['status'][0]['completed'] = True
        self.set_credentials(test_user)
        response = self.client.get(reverse('module-info', kwargs={'mnemo': temp_module_data['mnemo']}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, temp_module_data)

    def test_module_info_lesson_bought(self):
        """For lessons that user have bought field 'bought' must be True"""
        test_user = self.get_user()
        test_user.profile.lessons.add(self.lesson_basic_1, through_defaults={'bought': True})
        test_user.save()

        temp_module_data = deepcopy(module_data)
        temp_module_data['sections'][0]['lessons'][0]['status'][0]['bought'] = True
        self.set_credentials(test_user)
        response = self.client.get(reverse('module-info', kwargs={'mnemo': temp_module_data['mnemo']}))

        print()
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, temp_module_data)

    def test_home_page_view(self):
        response = self.client.get(reverse('api-home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, home_data)
