from django.shortcuts import render

def question_list(request):
    questions = Question.objects.all().annotate(answer_count=Count('answers')).order_by('-votes')
    return render(request, 'qna/question_list.html', {'questions': questions})

