from django.db import models


# Create your models here.
class User(models.Model):
    """ User database"""
    uid = models.BigAutoField(verbose_name="U_ID", primary_key=True)
    username = models.CharField(verbose_name="username", max_length=32, unique=True)
    password = models.CharField(verbose_name="password", max_length=64)
    pass


def avatar_dic_path(instance, filename):
    return '/avatar/user_{0}/{1}'.format(instance.uid, filename)


class UserInfo(models.Model):
    """ User Info database """
    uid = models.OneToOneField(verbose_name="U_ID", to="User", to_field="uid", on_delete=models.CASCADE,
                               primary_key=True)
    name = models.CharField(verbose_name="name", max_length=32, blank=True, null=True)
    avatar = models.ImageField(verbose_name="avatar", max_length=256, upload_to=avatar_dic_path, null=True, blank=True)
    gender_choices = [
        (1, "Male"),
        (2, "Female"),
    ]
    gender = models.PositiveSmallIntegerField(verbose_name="gender", blank=True, null=True, choices=gender_choices)
    age = models.PositiveSmallIntegerField(verbose_name="age", blank=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=256, blank=True, null=True)
    phone = models.CharField(verbose_name="phone_number", max_length=32, blank=True, null=True)
    join_time = models.DateField(verbose_name="join_time", auto_now_add=True)


class UserFollow(models.Model):
    """ User Follow database """
    uid = models.OneToOneField(verbose_name="U_ID", to="User", to_field="uid", on_delete=models.CASCADE,
                               primary_key=True, related_name="+")
    follow = models.ManyToManyField(verbose_name="follow", to="User", symmetrical=False, related_name="+")


class UserFollowed(models.Model):
    """ User Followed database """
    uid = models.OneToOneField(verbose_name="U_ID", to="User", to_field="uid", on_delete=models.CASCADE,
                               primary_key=True, related_name="+")
    followed_by = models.ManyToManyField(verbose_name="followed_by", to="User", symmetrical=False, related_name="+")


class PetInfo(models.Model):
    """ Pet Info database """
    pid = models.BigAutoField(verbose_name="P_ID", primary_key=True)
    master = models.ForeignKey(verbose_name="master_id", to="UserInfo", to_field="uid", on_delete=models.CASCADE)
    pet_name = models.CharField(verbose_name="pet_name", max_length=32)
    pet_avatar = models.ImageField(verbose_name="pet_avatar", max_length=256, upload_to=avatar_dic_path, null=True,
                                   blank=True)
    gender_choices = [
        (1, "Male"),
        (2, "Female"),
    ]
    pet_gender = models.PositiveSmallIntegerField(verbose_name="pet_gender", blank=True, null=True,
                                                  choices=gender_choices)
    pet_age = models.PositiveSmallIntegerField(verbose_name="pet_age", blank=True, null=True)
    pet_type = models.CharField(verbose_name="pet_type", max_length=32, blank=True, null=True)


class Resource(models.Model):
    """ Resource database """
    rid = models.BigAutoField(verbose_name="R_ID", primary_key=True)
    publisher = models.ForeignKey(verbose_name="publisher", to="UserInfo", to_field="uid", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="title", max_length=64)
    r_type_choices = [
        (1, "article"),
        (2, "picture"),
        (3, "video"),
    ]
    r_type = models.PositiveSmallIntegerField(verbose_name="resource_type", choices=r_type_choices)
    views_count = models.PositiveBigIntegerField(verbose_name="numbers_of_views", blank=True, null=True, default=0)
    comments_count = models.PositiveBigIntegerField(verbose_name="numbers_of_comments", blank=True, null=True,
                                                    default=0)
    likes_count = models.PositiveBigIntegerField(verbose_name="numbers_of_likes", blank=True, null=True, default=0)
    content = models.TextField(verbose_name="content", blank=True, null=True)
    media = models.FileField(verbose_name="media", max_length=256, upload_to=avatar_dic_path, null=True, blank=True)
    release_time = models.DateTimeField(verbose_name="release_time", auto_now_add=True)


class ResourceLike(models.Model):
    """ Resource like database """
    uid = models.OneToOneField(verbose_name="U_ID", to="UserInfo", to_field="uid", on_delete=models.CASCADE,
                               primary_key=True, related_name="+")
    like = models.ManyToManyField(verbose_name="like_resource", to="Resource", symmetrical=False, related_name="+")


class Comment(models.Model):
    """ Comment database """
    cid = models.BigAutoField(verbose_name="C_ID", primary_key=True)
    publisher = models.ForeignKey(verbose_name="publisher", to="UserInfo", to_field="uid", on_delete=models.CASCADE)
    parent = models.ForeignKey(verbose_name="resource", to="Resource", to_field="rid", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="content")
    create_time = models.DateTimeField(verbose_name="create_time", auto_now_add=True)
