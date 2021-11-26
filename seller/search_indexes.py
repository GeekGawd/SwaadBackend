from haystack import indexes
from seller.models import Dish

class DishIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True)
    title = indexes.CharField(model_attr = 'title')
    category = indexes.CharField(model_attr = 'category')

    def get_model(self):
        return Dish

    def index_queryset(self, using=None):
        return self.get_model().objects.all()