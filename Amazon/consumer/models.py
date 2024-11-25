from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Create your models here.
State_Choices=(
('AndhraPradesh ','AndhraPradesh'),
('Arunachal Pradesh','Arunachal Pradesh'),
('Assam','Assam'),
('Bihar','Bihar'),
('Chhattisgarh','Chhattisgarh'),
('Goa','Goa'),
('Gujarat','Gujarat'),
('Haryana','Haryana'),
('Himachal Pradesh','Himachal Pradesh'),
('Jammu & Kashmir','Jammu & Kashmir'),
('Jharkhand','Jharkhand'),
('Karnataka','Karnataka'),
('Kerala','Kerala'),
('Madhya Pradesh','Madhya Pradesh'),
('Maharashtra','Maharashtra'),
('Manipur','Manipur'),
('Meghalaya','Meghalaya'),
('Mizoram','Mizoram'),
('Nagaland','Nagaland'),
('Orissa','Orissa'),
('Punjab','Punjab'),
('Rajasthan','Rajasthan'),
('Sikkim','Sikkim'),
('Tamil Nadu','Tamil Nadu'),
('Tripura','Tripura'),
('Uttarakhand','Uttarakhand'),
('Uttar Pradesh','Uttar Pradesh'),
('West Bengal','West Bengal'),
('Tripura','Tripura'),
('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
('Chandigarh','Chandigarh'),
('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
('Daman & Diu','Daman & Diu'),
('Delhi','Delhi'),
('Lakshadweep','Lakshadweep'),
('Pondicherry','Pondicherry'),
)
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=300)
    state = models.CharField(choices=State_Choices,max_length=50)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()

    def __str__(self):
        return str(self.id)
    
CATEGORY_CHOICES = (
    ('TW','TopWears'),
    ('BW','BottomWears'),
    ('SW','SleepWear'),
    ('S','Shoes'),
    ('J','Jackets'),
    ('B','Blazzers'),
    ('SS','Shirts'),
    ('JS','Jeans'),
)
class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    brand = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    product_img = models.ImageField(upload_to='productimg')

    def __str__(self) :
        return str(self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
    def __str__(self):
        return str(self.id)
    
STATUS_CHOICES = (
    ('On The Way','On The Way'),
    ('Accepted','Accepted'),
    ('Delivered','Delivered'),
    ('Packed','Packed'),
    ('Cancel','Cancel'),

)
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES , max_length=50, default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    