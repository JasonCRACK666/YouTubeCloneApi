from django.urls import reverse

from rest_framework import status

from tests.setups import APITestCaseWithAuth

from tests.factories.comment import CommentFactory, DislikeCommentFactory, LikeCommentFactory

from apps.comment.models import Comment, LikedComment


class TestDislikeComment(APITestCaseWithAuth):
    def setUp(self):
        super().setUp()

        self.comment: Comment = CommentFactory.create(channel=self.user.current_channel)
        self.url = reverse('dislike_comment')

    def test_success_response_if_dislike_comment_added(self):
        """
        Should return a success response if the dislike to the comment has been added
        """
        response = self.client.post(
            self.url,
            {
                'comment_id': self.comment.pk
            },
            format='json'
        )

        self.assertDictEqual(response.data, {'message': 'Dislike comment added'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislike_comment_added(self):
        """
        Should verify if the dislike to the comment has been added successfully
        """
        self.client.post(
            self.url,
            {
                'comment_id': self.comment.pk
            },
            format='json'
        )

        dislike_comment = LikedComment.objects.filter(
            channel=self.user.current_channel,
            comment=self.comment,
            liked=False
        )

        self.assertTrue(dislike_comment.exists())

    def test_success_response_if_dislike_comment_removed(self):
        """
        Should return a success response if the dislike to the comment has been removed
        """
        DislikeCommentFactory.create(
            channel=self.user.current_channel,
            comment=self.comment
        )

        response = self.client.post(
            self.url,
            {
                'comment_id': self.comment.pk
            },
            format='json'
        )

        self.assertDictEqual(response.data, {'message': 'Dislike comment removed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislike_comment_removed(self):
        """
        Should verify if the dislike to the comment has been removed successfully
        """
        DislikeCommentFactory.create(
            channel=self.user.current_channel,
            comment=self.comment
        )

        self.client.post(
            self.url,
            {
                'comment_id': self.comment.pk
            },
            format='json'
        )

        dislike_comment = LikedComment.objects.filter(
            channel=self.user.current_channel,
            comment=self.comment
        )

        self.assertFalse(dislike_comment.exists())

    def test_like_comment_to_dislike_comment(self):
        LikeCommentFactory.create(
            channel=self.user.current_channel,
            comment=self.comment
        )

        self.client.post(
            self.url,
            {
                'comment_id': self.comment.pk
            },
            format='json'
        )

        dislike_comment = LikedComment.objects.filter(
            channel=self.user.current_channel,
            comment=self.comment,
            liked=False
        )

        self.assertTrue(dislike_comment.exists())

    def test_comment_does_not_exist(self):
        """
        Should return an error response and a 404 status code if the comment does not exist
        """
        non_exist_comment_id = self.comment.pk

        self.comment.delete()

        response = self.client.post(
            self.url,
            {
                'comment_id': non_exist_comment_id
            },
            format='json'
        )

        self.assertDictEqual(response.data, {'message': 'The comment does not exist'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_id_is_not_a_number(self):
        """
        Should return an error response and a 400 status code if the comment ID is not a number
        """
        response = self.client.post(
            self.url,
            {
                'comment_id': 'a'
            },
            format='json'
        )

        self.assertDictEqual(response.data, {'message': 'The comment ID must be a number'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
