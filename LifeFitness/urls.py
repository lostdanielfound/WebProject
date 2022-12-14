from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='Login'), 
    path('logout/', views.logout, name='Logout'),
    path('signup/', views.signup, name='Sign Up'),
    path('account/', views.account, name="Account"),
    path('healthsignup/', views.healthsignup, name="healthSignup"),

    path('account/createworkoutsession/', views.createWorkoutSession, name="Create-Workout-Session"),
    path('account/createworkoutsession/<int:workoutlistID>/', views.createWorkoutSession, name='Create-Workout-Session-data'),
    path('account/createworkout/<int:workoutlistID>/', views.createWorkout, name="Create Workout"),

    path('forums/', views.forums, name='forums'),
    path('forums/posts_page/<int:forumsID>/', views.posts_page, name='posts_page'),
    path('forums/posts_page/<int:forumsID>/post/<int:postID>/', views.post, name="post"),

    path('forums/createforum/', views.createforum, name='createforum'),
    path('forums/posts_page/<int:forumsID>/createpost', views.createpost, name='createpost'), 
]