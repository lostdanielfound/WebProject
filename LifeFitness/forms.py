# Form guide: https://ordinarycoders.com/django-custom-user-profile#Creating%20a%20user%20page
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from LifeFitness.models import FitnessProfile, Exercise, Workout, Workout_Session, Workout_Session_Report, Forum, Post, Post_Comment
from django import forms
from LifeFitness.helpfunctions import convertBMI, CompleteExerciseList, CurrentExerciseList

class RegistrationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2')
    
    def save(self, commit=True): 
        user = super().save(commit=False)
        if commit: 
            user.save() 
        return user # return user to login under successfully creation 

class HealthForm(forms.ModelForm):

    class Meta:
        model = FitnessProfile
        fields = ['currentheight', 'currentWeight', 'goalWeight']

    # Save all changes to the Current_user's fitnessprofile. 
    def save(self, current_user):
        curheight = self.cleaned_data['currentheight']
        curweight = self.cleaned_data['currentWeight']

        current_user.fitnessprofile.currentheight = curheight
        current_user.fitnessprofile.currentWeight = curweight
        current_user.fitnessprofile.BMI = convertBMI(curweight, curheight)
        current_user.fitnessprofile.goalWeight = self.cleaned_data['goalWeight']
        current_user.fitnessprofile.save()

class LoginForm(forms.Form):
    Username = forms.CharField(label="Username", max_length=200)
    Password = forms.CharField(label="Password", max_length=200, widget=forms.PasswordInput)
 
class CreateExercise(forms.Form):
    Name = forms.CharField(label="Exercise name", max_length=100)

    def save(self):
        newExercise = Exercise()
        newExercise.name = self.cleaned_data['Name']
        newExercise.save() 

class CreateWorkout(forms.Form):
    Exercise = forms.ChoiceField(label="Choice Exercise", choices=CurrentExerciseList(), )
    RepCount = forms.IntegerField(label="Rep Count", max_value=100, min_value=0)
    SetCount = forms.IntegerField(label="Set Count", max_value=100, min_value=0)

    def save(self, workoutlistID):
        exerciseID = self.cleaned_data['Exercise']
        print(exerciseID)
        newWorkout = Workout() # Creating a new workout object

        newWorkout.exerciseName = Exercise.objects.get(pk=exerciseID) # assign Exercise object to exerciseName
        newWorkout.repCount = self.cleaned_data['RepCount']
        newWorkout.setCount = self.cleaned_data['SetCount'] 
        newWorkout.save() 

        currentWS = Workout_Session.objects.get(pk=workoutlistID)
        currentWS.workoutList.add(newWorkout) # add newWorkout to workoutList of workout_Session
        currentWS.save() 

class CreateWorkoutSession(forms.Form): 
    Name = forms.CharField(label="Session Name", help_text="Session Name")
    Date = forms.DateField(label="Workout Date", widget=forms.DateInput()) 

    def save(self, current_user, WorkoutList):
        newWorkout = Workout_Session()
        newWorkout.name = self.cleaned_data['Name']
        newWorkout.Date = self.cleaned_data['Date']
        newWorkout.fitnesuser = current_user
        newWorkout.save() # Save the workout before adding workouts 

        for workout in WorkoutList: 
            newWorkout.workoutList.add(workout)
        newWorkout.save()

class PostWorkoutReport(forms.Form):
    ...
# https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django


# widgets: https://docs.djangoproject.com/en/4.1/ref/forms/widgets/#django.forms.TextInput

class CreateForum(forms.Form):
    Name = forms.CharField(label="Forum Name", help_text="Forum Name")
    Description = forms.CharField(label="Forum Description", help_text="Forum Description")

    def save(self):
        newForum = Forum()
        newForum.forum_title = self.cleaned_data['Name']
        newForum.description = self.cleaned_data['Description']
        newForum.save()

class CreatePost(forms.Form):
    Title = forms.CharField(label="Post Title", help_text="Post Title")
    Post_Text = forms.CharField(label="Body Text", help_text="Body Text")

    def save(self, current_user, ForumID):
        newPost = Post()
        newPost.user_name = current_user
        newPost.post_title = self.cleaned_data['Title']
        newPost.post_text = self.cleaned_data['Post_Text']
        newPost.forum = Forum.objects.get(pk=ForumID)
        newPost.save()

class CreateComment(forms.Form):
    Comment_Text = forms.CharField(label="Comment...", help_text="Comment...")

    def save(self, current_user, PostId):
        newComment = Post_Comment()
        newComment.user_name = current_user
        newComment.comment = self.cleaned_data['Comment_Text']
        newComment.post = Post.objects.get(pk=PostId)
        newComment.save()