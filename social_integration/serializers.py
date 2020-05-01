class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

comment = Comment(email='leila@example.com', content='foo bar')
serializer = CommentSerializer(comment)
serializer.data