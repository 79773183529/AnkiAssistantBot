from PIL import ImageDraw, Image
from with_files import open_csv, record_data
from text_make import center, text_separator, y_position, code_separator
from fonts import font, font_h, font_code, font_big


def make_cards(
        file_data='Data/wifi.csv',
        image_question_file='static/images/result/image_q.png',
        image_answer_file='static/images/result/image_answer.png',
):
    data = open_csv(file_data)

    for row in data:
        number_question = row[0]
        number_topic = row[1]
        heading = row[2]
        text_question = text_separator(row[3])
        text_answer = text_separator(row[4])
        try:
            code_answer = code_separator(row[5].replace('\\n', '\n'))
        except IndexError:
            code_answer = None

        is_big = False  # параметр который включает огромный шрифт и распологает текст в центре карточки
        if len(text_answer) <= 5 and not code_answer:
            is_big = True

        image_question = Image.open(image_question_file)
        draw_question = ImageDraw.Draw(image_question)

        image_answer = Image.open(image_answer_file)
        draw_answer = ImageDraw.Draw(image_answer)

        # Прописываем оглавление на обоих картинках
        for draw in (draw_question, draw_answer):
            draw.text(
                (center(heading), 15),
                heading,
                font=font_h,
                fill='#1C0606'
            )

        # Записываем текст вопроса
        draw_question.text(
            (50, 150),
            text_question,
            font=font,
            fill='#1C0606'
        )

        # Записываем текст ответа
        draw_answer.text(
            [(50, 110), (180, 270)][is_big],
            text_answer,
            font=(font, font_big)[is_big],
            fill='#1C0606'
        )

        # Высчитываем координатy 'Y' и записываем код под ответом
        if code_answer:
            draw.text(
                (20, y_position(text_answer)),
                code_answer,
                font=font_code,
                fill='#1C0606'
            )

        # сохраняем изображения в .png  файлах - создаём карточки
        src_question = f'static/images/result_card/image_{number_topic}_{number_question}_q.png'
        src_answer = f'static/images/result_card/image_{number_topic}_{number_question}_an.png'
        image_question.save(src_question)
        image_answer.save(src_answer)

        # Записываем данные о созданных карточках в .txt файл
        record_data(number_question, number_topic, src_question, src_answer)


make_cards()
