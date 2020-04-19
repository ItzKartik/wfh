from django.db import models
from django.contrib.auth.models import User
import uuid


class inbox_members(models.Model):
    inbox_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    people_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)


class direct_message(models.Model):
    inbox_id = models.CharField(max_length=300)
    user = models.CharField(max_length=100)
    text = models.CharField(max_length=1200)
    attachments = models.FileField(null=True, blank=True)
    seen = models.BooleanField(default=0)
    datetime = models.DateTimeField(auto_now=True)


class buyer_request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    rst = models.CharField(max_length=1200)
    rst_attach = models.FileField(null=True, blank=True)
    created_by = models.DateTimeField(auto_now=True)


class order_chat(models.Model):
    order_id = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    created_by = models.DateTimeField(auto_now=True)


class orders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.CharField(max_length=100)
    buyer = models.CharField(max_length=100)
    order_title = models.CharField(max_length=100)
    order_pricing = models.IntegerField()
    requirement = models.CharField(max_length=1000)
    requirement_assets = models.FileField(null=True, blank=True)
    delivery = models.BooleanField(default=0)
    order_completed = models.BooleanField(default=0)


class p_service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=100, blank=True)
    pricing = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=1200, blank=True)
    pic_first = models.FileField(null=True, blank=True)
    pic_second = models.FileField(null=True, blank=True)
    pic_third = models.FileField(null=True, blank=True)
    published_date = models.BooleanField(default=0)


class port_folio(models.Model):
    user_id = models.CharField(max_length=40)
    picture = models.FileField(null=True)
    skills = models.CharField(max_length=40)
    country = models.CharField(max_length=40)
    degree = models.CharField(max_length=100)
    certification = models.CharField(max_length=100)


