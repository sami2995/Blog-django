from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name
class Artciels(models.Model):
    title = models.CharField(max_length=450)
    image  = models.ImageField(blank=True)
    description = models.TextField()
    date  = models.DateTimeField(auto_now_add=True)
    visble  = models.BooleanField(default=True)
    news_category = models.ForeignKey(Category, 
                                      on_delete=models.SET_NULL,
                                        null=True)
    def __str__(self):
        return self.title


class Comments(models.Model):
    email  = models.EmailField(("user email"), max_length=254)
    comment  = models.TextField()
    date  = models.DateTimeField(auto_now_add=True, null=True)
    post  = models.ForeignKey(Artciels, on_delete=models.CASCADE)

