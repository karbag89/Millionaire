from django.shortcuts import render
from gameApp.forms import UserForm
from gameApp.models import UserScores, Questions, Answers
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from gameApp import views

# Create your views here.

#index page class based view
class IndexView(TemplateView):
    template_name = 'gameApp/index.html'
    def get_context_data(self, **kwargs):
        context  = super().get_context_data( **kwargs)

        if 'score' not in self.request.session:
            self.request.session['score'] = 0

        if 'winner' not in self.request.session:
            self.request.session['winner'] = False

        if 'right_answer' not in self.request.session:
            self.request.session['right_answer'] = ""

        user = self.request.user
        if self.request.user.is_authenticated:
    # getting values from session which was stored in other views
            final_score = self.request.session['score']
            is_finish = self.request.session['winner']
            right_answer = self.request.session['right_answer']
    # getting existing user score and add to it tmp score from last game and then update his score record
            user_score = UserScores.objects.filter(user_id = user.id)
            sc = UserScores.objects.get(user=user)
            sc.score = sc.score + final_score
            sc.save()
    # and after that reset session values to default for the new game
            self.request.session['score'] = 0
            self.request.session['winner'] = False
            self.request.session['right_answer'] = ""
        else:
            final_score = self.request.session['score']
            is_finish = self.request.session['winner']
            right_answer = self.request.session['right_answer']

        context['score'] = final_score
        context['winner'] = is_finish
        context['right_answer'] = right_answer
        return context

# new game view
class GameplayView(TemplateView):
    template_name = 'gameApp/gameplay.html'
    def get_context_data(self, **kwargs):
        context  = super().get_context_data( **kwargs)
        self.request.session['q_count'] = 0
        self.request.session['winner'] =False
        self.request.session['score'] = 0
        self.request.session['right_answer'] = ""
# getting 6 random questions from questions table
        question_list = Questions.objects.all().order_by('?')[:6]
        context['questions'] = question_list
        return context

# logout view, used login_required decoreater to be shure
# that we logging out the user which was previously loged in
@login_required
def user_logout(request):
    logout(request)
    request.session['score']=0
    request.session['winner']=False
    return HttpResponseRedirect(reverse('index'))

# registration view using modelForm from User model
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'gameApp/registration.html',{'user_form':user_form,'registered':registered})

# login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
        else:
            err_msg = "Invalid login details supplied."
            return render(request, 'gameApp/login.html', {'err_msg': err_msg})
    else:
        return render(request, 'gameApp/login.html')

# TOP 10 view which show best players
#from all the time based on their scores form all games
class ToptenView(TemplateView):
    template_name = 'gameApp/topten.html'
    def get_context_data(self,**kwargs):
        context  = super().get_context_data(**kwargs)
        score_list = UserScores.objects.order_by('-score').all()[:10]
        context['scores'] =  score_list
        return context

# checking answer which comes using AJAX in front-end
# and based on was the answer true or false sending back information
# which will used in front-end for farther decisions like
# showing next question and adding this question score to tmp_score
# or for finishing the game with existing tmp_score and showing right answer
def check_answer(request):
    q_count= request.session['q_count']
    if request.GET:
        answer_id = request.GET.get('answer_id', True)
        answer = Answers.objects.get(pk=answer_id)

        if answer.is_true:
            request.session['q_count'] = request.session['q_count'] + 1
            if q_count==5:
                request.session['winner'] = True
            current_point = answer.question_id.point
            request.session['score'] =request.session['score'] + current_point
            return HttpResponse("ok")
        else:
            answers = Answers.objects.filter(question_id=answer.question_id)
            right_answer = ""
            for answer_el in answers:
                if answer_el.is_true:
                    right_answer = answer_el.answer + ", " + right_answer
                    request.session['right_answer'] = right_answer
            return HttpResponse("not")
