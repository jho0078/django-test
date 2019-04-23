# from django.test import TestCase
from test_plus.test import TestCase
from django.conf import settings
from django.urls import reverse
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
        self.user = self.make_user(username='test', password='qawsedrf!')
        
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
            
            
    # detail 페이지가 제대로 출력되는지 확인
    def test_05_detail_contains(self):
        # given
        # board = Board.objects.create(title='제목', content='내용', user=self.user)
        board = Board.objects.create(title='제목', content='내용', user=self.user)
        # when
        self.get_check_200('boards:detail', board_pk=board.pk)
        # then
        self.assertResponseContains(board.title, html=False)
        self.assertResponseContains(board.content, html=False)
        
    def test_06_detail_template(self):
        board = Board.objects.create(title='제목', content='내용', user=self.user)
        response =  self.get_check_200('boards:detail', board_pk=board.pk)
        self.assertTemplateUsed(response, 'boards/detail.html')
    
    # 페이지가 잘 뜨는지
    def test_07_get_index(self):
        self.get_check_200('boards:index')
        
    # 페이지가 잘 뜨는지 + index.html 을 사용하고 있는지
    def test_08_index_template(self):
        response = self.get_check_200('boards:index')
        self.assertTemplateUsed(response, 'boards/index.html')
        
    def test_09_index_queryset(self):
        Board.objects.create(title='제목', content='내용', user=self.user)
        Board.objects.create(title='제목', content='내용', user=self.user)
        boards = Board.objects.order_by('-pk')
        # when
        response = self.get_check_200('boards:index')
        # then
        self.assertQuerysetEqual(response.context['boards'], map(repr, boards))
        
    # get 방식이기 때문에 오류가 발생
    # def test_10_delete(self):
    #     board = Board.objects.create(title='제목', content='내용', user=self.user)
    #     with self.login(username='test', password='qawsedrf!'):
    #         self.get_check_200('boards:delete', board_pk=board.pk)
            
    def test_11_delete_POST(self):
        board = Board.objects.create(title='제목', content='내용', user=self.user)
        with self.login(username='test', password='qawsedrf!'):
            self.post('boards:delete', board_pk=board.pk)
            self.assertEqual(Board.objects.count(), 0)
            
    def test_12_delete_redirect(self):
        board = Board.objects.create(title='제목', content='내용', user=self.user)
        with self.login(username='test', password='qawsedrf!'):
            response = self.post('boards:delete', board_pk=board.pk)
            # then
            # 삭제 후 요청이 index 로 잘가는지
            self.assertRedirects(response, reverse('boards:index'))
            
    def test_13_get_update(self):
        board = Board.objects.create(title='제목', content='내용', user=self.user)
        with self.login(username='test', password='qawsedrf!'):
            response = self.get_check_200('boards:update', board.pk)
            self.assertEqual(response.context['form'].instance.pk, board.pk)
    
    # 로그인 된 상태로 update로 들어갈 수 있는지
    def test_14_get_update_login_required(self):
        self.assertLoginRequired('boards:update', board_pk=1)
        
# 4. ModelForm
# class BoardModelTest(TestCase):
            