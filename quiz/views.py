
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import Test, Question, Attempt, Answer
from .forms import TestForm, QuestionForm


def test_list(request):
    tests = Test.objects.filter(is_active=True)
    return render(request, 'quiz/test_list.html', {'tests': tests})



@login_required
def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id, is_active=True)
    questions = test.questions.all()

    if request.method == 'POST':

        # Validate all submitted answers.
        selected_answers = {}

        for question in questions:
            selected_option = request.POST.get(
                f'question_{question.id}'
            )

            if selected_option not in ['A', 'B', 'C', 'D']:
                return render(request, 'quiz/test_detail.html', {
                    'test': test,
                    'questions': questions,
                    'error': 'Please answer every question before submitting.'
                })

            selected_answers[question.id] = selected_option

        # Calculate the score.
        score = 0
        max_score = questions.count()

        for question in questions:
            if selected_answers[question.id] == question.correct_option:
                score += 1

        # Save the test attempt.
        attempt = Attempt.objects.create(
            student=request.user,
            test=test,
            score=score,
            max_score=max_score
        )

        # Save every individual answer.
        answers = []

        for question in questions:
            selected_option = selected_answers[question.id]

            answers.append(
                Answer(
                    attempt=attempt,
                    question=question,
                    selected_option=selected_option,
                    is_correct=(
                        selected_option == question.correct_option
                    )
                )
            )

        Answer.objects.bulk_create(answers)

        # Calculate percentage.
        percentage = round(
            (score / max_score) * 100
        ) if max_score > 0 else 0

        return render(request, 'quiz/result.html', {
            'attempt': attempt,
            'percentage': percentage
        })

    return render(request, 'quiz/test_detail.html', {
        'test': test,
        'questions': questions
    })



@login_required
def my_results(request):
    attempts = Attempt.objects.filter(
        student=request.user
    ).order_by('-submitted_at')

    return render(request, 'quiz/my_results.html', {
        'attempts': attempts
    })





@staff_member_required
def teacher_dashboard(request):
    tests = Test.objects.filter(
        created_by=request.user
    ).prefetch_related('questions')

    total_tests = tests.count()

    total_questions = Question.objects.filter(
        test__created_by=request.user
    ).count()

    attempts = Attempt.objects.filter(
        test__created_by=request.user
    )

    total_attempts = attempts.count()

    valid_attempts = [
        attempt for attempt in attempts
        if attempt.max_score > 0
    ]

    if valid_attempts:
        average_percentage = round(
            sum(
                (attempt.score / attempt.max_score) * 100
                for attempt in valid_attempts
            ) / len(valid_attempts)
        )
    else:
        average_percentage = 0

    return render(request, 'quiz/teacher_dashboard.html', {
        'tests': tests,
        'total_tests': total_tests,
        'total_questions': total_questions,
        'total_attempts': total_attempts,
        'average_percentage': average_percentage
    })




@staff_member_required
def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)

        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            test.save()

            return redirect('teacher_dashboard')
    else:
        form = TestForm()

    return render(request, 'quiz/create_test.html', {
        'form': form
    })

@staff_member_required
def edit_test(request, test_id):
    test = get_object_or_404(
        Test,
        id=test_id,
        created_by=request.user
    )

    if request.method == 'POST':
        form = TestForm(request.POST, instance=test)

        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = TestForm(instance=test)

    return render(request, 'quiz/edit_test.html', {
        'form': form,
        'test': test
    })

@staff_member_required
def delete_test(request, test_id):
    test = get_object_or_404(
        Test,
        id=test_id,
        created_by=request.user
    )

    if request.method == 'POST':
        test.delete()
        return redirect('teacher_dashboard')

    return render(request, 'quiz/delete_test.html', {
        'test': test
    })


@staff_member_required
def create_question(request, test_id):
    test = get_object_or_404(
        Test,
        id=test_id,
        created_by=request.user
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()

            return redirect('teacher_dashboard')
    else:
        form = QuestionForm()

    return render(request, 'quiz/create_question.html', {
        'form': form,
        'test': test
    })


@staff_member_required
def edit_question(request, question_id):
    question = get_object_or_404(
        Question,
        id=question_id,
        test__created_by=request.user
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = QuestionForm(instance=question)

    return render(request, 'quiz/edit_question.html', {
        'form': form,
        'question': question
    })


@staff_member_required
def delete_question(request, question_id):
    question = get_object_or_404(
        Question,
        id=question_id,
        test__created_by=request.user
    )

    if request.method == 'POST':
        question.delete()
        return redirect('teacher_dashboard')

    return render(request, 'quiz/delete_question.html', {
        'question': question
    })


@staff_member_required
def teacher_results(request):
    attempts = Attempt.objects.filter(
        test__created_by=request.user
    ).select_related(
        'student',
        'test'
    ).order_by('-submitted_at')

    return render(request, 'quiz/teacher_results.html', {
        'attempts': attempts
    })


@staff_member_required
def attempt_detail(request, attempt_id):
    attempt = get_object_or_404(
        Attempt,
        id=attempt_id,
        test__created_by=request.user
    )

    answers = attempt.answers.select_related(
        'question'
    ).all()

    return render(request, 'quiz/attempt_detail.html', {
        'attempt': attempt,
        'answers': answers
    })
