class SerializerByAction:
    default_serializer_class = None
    serializer_classes = None

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)