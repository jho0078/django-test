# from django.test import TestCase
from test_plus.test import TestCase
from django.conf import settings
from .models import Board
from .forms import BoardForm

# 1. settings test
class SettingsTest(TestCase):
    def test_01_settings(self):
        self.assertEqual(settings.USE_I18N, True)
        self.assertEqual(settings.USE_TZ, False)
        self.assertEqual(settings.LANGUAGE_CODE, 'ko-kr')
        self.assertEqual(settings.TIME_ZONE, 'Asia/Seoul')
        
# 2. Model test + ModelForm test
class BoardModelTest(TestCase):
    def test_01_model(self):
        # board = Board.objects.create(title='test title', content='test content')
        board = Board.objects.create(title='test title', content='test content', user_id=1)
        self.assertEqual(str(board), f'Board{board.pk}', msg='출력 값이 일치하지 않음')
    
    def test_02_boardform(self):
        # given
        data = {'title': '제목', 'content': '내용'}
        # when then
        self.assertEqual(BoardForm(data).is_valid(), True)
        
    def test_03_boardform_without_title(self):
        data = {'content': '내용'}
        self.assertEqual(BoardForm(data).is_valid(), False)
        
    def test_04_boardform_without_content(self):
        data = {'title': '제목'}
        self.assertEqual(BoardForm(data).is_valid(), False)
        
# 3. View test
# 기본 구조 : given - when - then
class BoardViewTest(TestCase):
    # 공통적인 given 상황을 구성하기에 유용하다.
    def setUp(self):
        user = self.make_user(username='test', password='qawsedrf!')
        
    # create test 에서의 포인트는 form 을 제대로 주느냐이다. 가장 기본은 get_check_200
    def test_01_get_create(self):
        # when 로그인이 유지 된 상태에서 테스트
        with self.login(username='test', password='qawsedrf!'):
            response = self.get_check_200('boards:create')
            # then
            # self.assertContains(response, '<form')  
            self.assertIsInstance(response.context['form'], BoardForm)
            
    def test_02_get_create_login_required(self):
        self.assertLoginRequired('boards:create')
        
    def test_03_post_create(self):
        # given 사용자와 작성한 글 데이터
        data = {'title': 'test_title', 'content': 'test_content'}
        # when 로그인을 해서 post 요청으로 해당 url 로 요청 보낸경우
        with self.login(username='test', password='qawsedrf!'):
            self.post('boards:create', data=data)
        # then 글이 작성되고, 페이지가 detail 로 redirect 된다.
        
    def test_04_board_create_without_content(self):
        # given
        data = {'title': 'test_title'}
        # when
        with self.login(username='test', password='qawsedrf!'):
            response = self.post('boards:create', data=data)
            self.assertContains(response, '')
            # form.is_valid() 를 통과하지 못해서 팅겨져 나옴.
            
# 4. ModelForm
# class BoardModelTest(TestCase):
            