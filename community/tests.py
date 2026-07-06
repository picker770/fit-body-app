from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import ProgressPost, Comment

User = get_user_model()


class ProgressPostModelTest(TestCase):
    """Test the ProgressPost Model"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = ProgressPost.objects.create(
            user=self.user,
            title='My Progress',
            caption='Great workout today!'
        )

    def test_post_creation(self):
        self.assertEqual(self.post.user.username, 'testuser')
        self.assertEqual(self.post.title, 'My Progress')
        self.assertEqual(self.post.caption, 'Great workout today!')

    def test_post_str_method(self):
        self.assertEqual(str(self.post), 'testuser - My Progress')

    def test_post_total_likes(self):
        self.assertEqual(self.post.total_likes(), 0)

    def test_post_get_comments_count(self):
        self.assertEqual(self.post.get_comments_count(), 0)

    def test_post_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), f'/community/post/{self.post.id}/')


class CommentModelTest(TestCase):
    """Test the Comment Model"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = ProgressPost.objects.create(
            user=self.user,
            title='My Progress',
            caption='Great workout today!'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='Great job!'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.post.title, 'My Progress')
        self.assertEqual(self.comment.user.username, 'testuser')
        self.assertEqual(self.comment.content, 'Great job!')

    def test_comment_str_method(self):
        self.assertEqual(str(self.comment), 'testuser - Great job!')


class CommunityFeedTest(TestCase):
    """Test the Community Feed View"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        ProgressPost.objects.create(
            user=self.user,
            title='Post 1',
            caption='First post'
        )
        ProgressPost.objects.create(
            user=self.user,
            title='Post 2',
            caption='Second post'
        )

    def test_feed_view(self):
        response = self.client.get(reverse('community:feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/feed.html')
        self.assertEqual(len(response.context['posts']), 2)


class CreatePostTest(TestCase):
    """Test the Create Post View"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_create_post_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('community:create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/create_post.html')

    def test_create_post_view_unauthenticated(self):
        response = self.client.get(reverse('community:create_post'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_create_post_post_valid(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('community:create_post'), {
            'title': 'New Post',
            'caption': 'This is a test post'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to feed
        self.assertTrue(ProgressPost.objects.filter(title='New Post').exists())


class LikePostTest(TestCase):
    """Test the Like Post AJAX View"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = ProgressPost.objects.create(
            user=self.user,
            title='Test Post',
            caption='Test caption'
        )

    def test_like_post_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('community:like_post', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_likes'], 1)
        self.assertTrue(response.json()['liked'])

    def test_like_post_unauthenticated(self):
        response = self.client.post(reverse('community:like_post', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_like_post_unlike(self):
        self.client.login(username='testuser', password='testpass123')
        # Like first
        self.client.post(reverse('community:like_post', kwargs={'pk': self.post.id}))
        # Unlike
        response = self.client.post(reverse('community:like_post', kwargs={'pk': self.post.id}))
        self.assertEqual(response.json()['total_likes'], 0)
        self.assertFalse(response.json()['liked'])


class CommentPostTest(TestCase):
    """Test the Comment Post View"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = ProgressPost.objects.create(
            user=self.user,
            title='Test Post',
            caption='Test caption'
        )

    def test_add_comment_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('community:add_comment', kwargs={'pk': self.post.id}), {
            'content': 'Nice progress!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to post detail
        self.assertTrue(Comment.objects.filter(content='Nice progress!').exists())

    def test_add_comment_unauthenticated(self):
        response = self.client.post(reverse('community:add_comment', kwargs={'pk': self.post.id}), {
            'content': 'Nice progress!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_add_comment_empty(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('community:add_comment', kwargs={'pk': self.post.id}), {
            'content': ''
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(content='').exists())
