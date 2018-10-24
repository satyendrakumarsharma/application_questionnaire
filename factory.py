import constants as const
from model import *
from utils import *


class ApplicationFactory:
    """This is a factory class that creates the 'ApplicationData' objects"""

    @staticmethod
    def create_question_answer_mapping(mapping):
        q_id, q_value, ans_value, tag, q_type, q_default = mapping
        print('[Configuring Question] ' + q_id + ':' + q_value + ':' + ans_value + ':' + tag + ':' + q_type)
        q_type = str_to_type(q_type)

        question = Question.get_question_by_value(q_value)
        if question is None:
            # create new question
            question = Question(q_id, q_value, q_type, tag, q_default)

        if ans_value == const.DEFAULT_QUESTION_TAG:
            question.q_tag = tag
        elif q_type == QuestionType.CHECKBOX:
            answer = ApplicationFactory._create_answer(ans_value, tag, str(q_id) + ans_value) \
                if question.is_nullable else ApplicationFactory._create_answer(ans_value, tag)
            question.all_answer_options.append(answer)
        elif q_type == QuestionType.RADIO:
            answer = ApplicationFactory._create_answer(ans_value, tag, str(q_id) + ans_value)
            question.all_answer_options.append(answer)

    @staticmethod
    def _create_answer(answer_value, answer_tag, ans_id=None):
        answer = Answer.get_answer_by_id(ans_id) if ans_id is not None else Answer.get_answer_by_value(answer_value)
        if answer is None:
            # create new answer
            answer = Answer(answer_value, answer_tag, ans_id)
        return answer

    @staticmethod
    def create_app_data(app_entry):
        app_name, app_question, app_answers = app_entry

        print('[Reading Input] ' + app_name + ' : ' + app_question + ' : ' + app_answers)

        # Input validation
        if is_empty(app_name) or is_empty(app_question):
            print('[Identified an EMPTY application questionnaire]')
            return

        question = Question.get_question_by_value(app_question)

        if question is None:
            print('Invalid question: Not found in configuration details.')
            return

        q_type = question.q_type

        if q_type == QuestionType.CHECKBOX:
            answers = []        # [ Answer ]
            segregated_answers = [] if is_empty_with_none(app_answers) else app_answers.split(',')
            for individual_answer in segregated_answers:
                if question.is_nullable:
                    answers.append(Answer.get_answer_by_id(str(question.q_id) + individual_answer))
                else:
                    answers.append(Answer.get_answer_by_value(individual_answer))
        # elif q_type == QuestionType.RADIO:
        #     answers = Answer.get_answer_by_value(app_answers)
        else:
            answers = app_answers

        app_data = ApplicationData.get_application_data_by_name(app_name)
        if app_data is None:
            # a new app_data is needed only when it is not cached in dict
            app_data = ApplicationData(app_name)

        app_data.update_questionnaire(question, answers)
