from datacenter.models import Schoolkid, Mark
from datacenter.models import Chastisement, Lesson, Commendation
import random


def fix_marks(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем '{schoolkid_name}' не найден. "
              f"Проверьте, правильно ли вы написали имя")
        return
    except Schoolkid.MultipleObjectsReturned:
        print(
            f"Найдено несколько учеников с именем '{schoolkid_name}'. "
            f"Уточните запрос.")
        return
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lte=3)
    bad_marks.update(points=5)


def remove_chastisements(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем '{schoolkid_name}' не найден. "
              f"Проверьте, правильно ли вы написали имя")
        return
    except Schoolkid.MultipleObjectsReturned:
        print(
            f"Найдено несколько учеников с именем '{schoolkid_name}'. "
            f"Уточните запрос.")
        return
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid_name, subject_title):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем '{schoolkid_name}' не найден. "
              f"Проверьте, правильно ли вы написали имя")
        return
    except Schoolkid.MultipleObjectsReturned:
        print(
            f"Найдено несколько учеников с именем '{schoolkid_name}'. "
            f"Уточните запрос.")
        return

    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_title
    ).order_by('-date')

    if not lessons.exists():
        print(
            f"Уроки по предмету '{subject_title}' "
            f"для ученика '{schoolkid_name}' не найдены. "
            f"Убедитесь, что вы правильно написали название предмета"
        )
        return

    last_lesson = lessons.first()

    commendation_texts = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!',
        'Хвалю!'
    ]

    commendation_text = random.choice(commendation_texts)

    Commendation.objects.create(
        text=commendation_text,
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
    )

