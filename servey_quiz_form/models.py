import random
import string
from django.db import models
from accounts.models import UserQuiz,ConductUser,CustomUser


class Choices(models.Model):
    choice = models.CharField(max_length=5000)
    is_answer = models.BooleanField(default=False)

class Questions(models.Model):
    question = models.CharField(max_length= 10000)
    question_type = models.CharField(max_length=20)
    required = models.BooleanField(default= False)
    answer_key = models.CharField(max_length = 5000, blank = True)
    score = models.IntegerField(blank = True, default=0)
    feedback = models.CharField(max_length = 5000, null = True)
    choices = models.ManyToManyField(Choices, related_name = "question_choices")

    def __str__(self):
        return self.question 
    

class Answer(models.Model):
    answer = models.CharField(max_length=5000)
    answer_to = models.ForeignKey(Questions, on_delete = models.CASCADE ,related_name = "answer_to")
    def __str__(self):
        return self.answer

class Form(models.Model):
    code = models.CharField(max_length=30,unique=''.join(random.choice(string.ascii_letters + string.digits) for x in range(30)))
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=10000, blank = True)
    creator = models.ForeignKey(ConductUser, on_delete = models.CASCADE, related_name = "creator")
    background_color = models.CharField(max_length=20, default = "#d9efed")
    text_color = models.CharField(max_length=20, default="#272124")
    collect_email = models.BooleanField(default=False)
    authenticated_responder = models.BooleanField(default = False)
    edit_after_submit = models.BooleanField(default=False)
    confirmation_message = models.CharField(max_length = 10000, default = "Your response has been recorded.")
    is_quiz = models.BooleanField(default=False)
    allow_view_score = models.BooleanField(default= True)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    questions = models.ManyToManyField(Questions, related_name = "questions")
    available_time =models.DateTimeField(blank=True, null=True) 
    exam_duration = models.PositiveIntegerField(blank=True, null=True, help_text="Duration of the exam in minutes")
    form_valid = models.BooleanField(default=True)
    def __str__(self):
        return self.code
    

class Responses(models.Model):
    response_code = models.CharField(max_length=20)
    response_to = models.ForeignKey(Form, on_delete = models.CASCADE, related_name = "response_to")
    responder_ip = models.CharField(max_length=30)
    responder = models.ForeignKey(UserQuiz, on_delete = models.CASCADE, related_name = "responder", blank = True, null = True)
    responder_email = models.EmailField(blank = True, null = True)
    response = models.ManyToManyField(Answer, related_name = "response")
    def save(self, *args, **kwargs):
        super(Responses, self).save(*args, **kwargs)
        if self.response.exists():
            self.response.set(self.response.all())
    def __str__(self):
        return self.response_code
    
class Result(models.Model):
    result_code = models.CharField(max_length=20)
    result_to = models.ForeignKey(Form, on_delete = models.CASCADE, related_name = "result_to")
    responder = models.ForeignKey(UserQuiz, on_delete = models.CASCADE, related_name = "result_responder")
    responder_email = models.EmailField(blank = True, null = True)
    name=models.CharField(max_length=100,blank=True,null=True)
    score = models.IntegerField()
    total_score = models.IntegerField()
    percentage = models.FloatField(blank=True, null=True)
    show_score = models.BooleanField(default=False, blank=True, null=True)
    def __str__(self):
        return self.result_code


