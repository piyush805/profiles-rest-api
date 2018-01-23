from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from .import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile',views.UserProfileViewSet)
router.register('login',views.LoginViewSet, base_name = 'login')#base_name becuz its not a model viewset
#when registering a modelviewset, dont need a base_name,
#django rest can figure this out
#by looking at the model that's registered with the serailizer,
#that's registered on our vieswset
router.register('feed',views.UserProfileFeedViewSet)

urlpatterns = [
    url(r'^hello-view/', views.HelloApiView.as_view()),
    url(r'',include(router.urls))
]
