from django.db import models

# Create your models here.
class Image(models.Model):
    image = models.ImageField()
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    artice = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField
    images = models.ManyToManyField(Image)
    
    def __str__(self) -> str:
        return f'({self.article}) {self.name}'

    
    
    
    # sales: {
    #     type: Array,
    #     default: []
    # },
    # orderCount: {
    #     type: Number,
    #     required: true,
    #     default: 0
    # },
    # orders: {
    #     type: Array,
    #     default: []
    # },
    # description: {
    #     type: String,
    #     default: ''
    # },
    # author: {
    #     type: String,
    #     default: ''
    # },
    # imgUrl: String, 
    # categories: {
    #     type: Array,
    #     default: []
    # },
    # ageRestriction: {
    #     type: Number,
    #     default: 18
    # },
    # complexity: {
    #     type: String,
    #     default: "Junior"
    # },
    # rating: {
    #     type: Number,
    #     default: 3
    # },
    # user: {
    #     type: mongoose.Schema.Types.ObjectId,
    #     ref: 'Admin'
    # },
    # provider: {
    #     type: mongoose.Schema.Types.ObjectId,
    #     ref: 'Provider',
    #     default: null
    # }