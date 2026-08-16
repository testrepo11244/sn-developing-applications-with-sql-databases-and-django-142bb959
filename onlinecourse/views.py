from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Question, Choice, Submission, Enrollment


def submit(request, course_id):
    """
    Handles exam submission.
    - Retrieves the course and the learner's enrollment.
    - Creates a Submission instance.
    - Associates selected Choice objects with the submission.
    - Redirects to the result view.
    """
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, course=course, learner=request.user)

    if request.method == 'POST':
        submission = Submission.objects.create(enrollment=enrollment)

        selected_choices = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                try:
                    choice = Choice.objects.get(pk=int(value))
                    selected_choices.append(choice)
                except (ValueError, Choice.DoesNotExist):
                    continue

        submission.choices.set(selected_choices)
        return redirect('onlinecourse:show_exam_result',
                        course_id=course.id,
                        submission_id=submission.id)

    return render(request, 'onlinecourse/submit.html', {'course': course})


def show_exam_result(request, course_id, submission_id):
    """
    Displays the exam result.
    - Calculates total questions, correct answers, and score.
    - Determines pass/fail based on a 70% threshold.
    - Renders the result template with all relevant context.
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission,
                                   pk=submission_id,
                                   enrollment__course=course)

    total_questions = Question.objects.filter(lesson__course=course).count()
    correct_answers = 0

    for question in Question.objects.filter(lesson__course=course):
        selected = submission.choices.filter(question=question)
        correct_choices = question.choice_set.filter(is_correct=True)

        # A question is correct if the learner selected all correct choices
        # and did not select any incorrect ones.
        if set(selected) == set(correct_choices):
            correct_answers += 1

    score = int((correct_answers / total_questions) * 100) if total_questions else 0
    passed = score >= 70

    context = {
        'course': course,
        'submission': submission,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score': score,
        'passed': passed,
    }
    return render(request, 'onlinecourse/exam_result.html', context)