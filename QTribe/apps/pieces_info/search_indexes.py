from haystack import indexes

from pieces_info.models import ArticleModel,VideoModel


class ArticleModelIndex(indexes.SearchIndex, indexes.Indexable):
     """Article索引数据模型类"""

     text = indexes.CharField(document=True, use_template=True)
     def get_model(self):
        """返回建⽴索引的模型类"""
        return ArticleModel

     def index_queryset(self, using=None):
        """返回要建⽴索引的数据查询集"""
        return self.get_model().objects.order_by('-id')


class VideoModelIndex(indexes.SearchIndex, indexes.Indexable):
    """Article索引数据模型类"""

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """返回建⽴索引的模型类"""
        return VideoModel

    def index_queryset(self, using=None):
        """返回要建⽴索引的数据查询集"""
        return self.get_model().objects.order_by('-id')