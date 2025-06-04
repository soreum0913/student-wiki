from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from django.utils import timezone
from django.db.models import Count

# 질문 목록
def question_list(request):
    questions = Question.objects.filter(is_deleted=False).annotate(
        answer_count=Count('answers')
    ).order_by('-votes', '-created_at')  # 인기순 정렬
    return render(request, 'qna/question_list.html', {'questions': questions})

# 질문 상세 페이지
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id, is_deleted=False)
    answers = question.answers.filter(is_deleted=False).order_by('-recommend', '-created_at')
    return render(request, 'qna/question_detail.html', {'question': question, 'answers': answers})

# 질문 작성
@login_required
def question_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        Question.objects.create(
            title=title,
            content=content,
            author=request.user,
            created_at=timezone.now()
        )
        return redirect('question_list')
    return render(request, 'qna/question_form.html')

# 답변 작성
@login_required
def answer_create(request, question_id):
    if request.method == "POST":
        question = get_object_or_404(Question, id=question_id, is_deleted=False)
        content = request.POST.get("content")
        Answer.objects.create(
            question=question,
            content=content,
            author=request.user,
            created_at=timezone.now()
        )
        return redirect('question_detail', question_id=question.id)
    return redirect('question_detail', question_id=question_id)

@login_required
def recommend_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id, is_deleted=False)
    answer.recommend += 1
    answer.save()
    return redirect('question_detail', question_id=answer.question.id)
