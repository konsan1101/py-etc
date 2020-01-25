from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework import status
from .models import Item
from .serializer import ManyItemsSerializer
from item_detection.detection import item_detection
from chainercv.datasets import voc_bbox_label_names


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ManyItemsSerializer

    @list_route(methods=["post"])
    def detection(self, request):

        img = request.FILES["image"]
        names, scores = item_detection(img)

        # Delete the previous data
        pre_vm = Item.objects.all()
        pre_vm.delete()

        for name, score in zip(names, scores):
            name = voc_bbox_label_names[name]
            item = Item(name=name, image=img, score=score)
            item.save()

        serializer = ManyItemsSerializer(data={"name": "items"})

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





