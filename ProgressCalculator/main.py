from dateutil import rrule
import datetime as dt
import numpy as np
import inquirer
import constants
import utils

steps = [constants.MAIN_MENU_STEP_TYPE]
counts = utils.__load_counts()


def __change_step(step_type):
    global steps

    if step_type == constants.BACK_STEP_TYPE:
        steps.pop()
        return

    steps.append(step_type)


def __main_menu():
    questions = [
        inquirer.List(constants.ANSWER,
                      message='What\'re we doing?',
                      choices=[step_type[1] for step_type in constants.STEP_TYPES
                               if step_type[0] not in [constants.MAIN_MENU_STEP_TYPE, constants.BACK_STEP_TYPE]]),
    ]
    answer = inquirer.prompt(questions).get(constants.ANSWER)
    __change_step(utils.get_step_by_text(answer)[0])


def __work_types(step_type):
    questions = [
        inquirer.List(constants.ANSWER,
                      message='Choose the work type',
                      choices=[work_type[-1] for work_type in constants.WORK_TYPES + ((constants.BACK_STEP_TYPE,
                                                                                      constants.BACK_STEP_TEXT),)]),
    ]
    answer = inquirer.prompt(questions).get(constants.ANSWER)
    if answer == constants.BACK_STEP_TEXT:
        __change_step(constants.BACK_STEP_TYPE)
        return

    __quantity(step_type, utils.get_work_type_by_text(answer)[0])


def __quantity(step_type, work_type):
    global counts

    questions = [
        inquirer.Text(constants.ANSWER, message='How many?'),
    ]
    answer = inquirer.prompt(questions).get(constants.ANSWER)

    try:
        count = int(answer)
    except:
        print('Not numeric')
        return

    if step_type == constants.ADDITION_STEP_TYPE:
        counts[work_type] += count
    elif step_type == constants.SUBTRACTION_STEP_TYPE:
        counts[work_type] = (counts[work_type] - count) if count <= counts[work_type] else 0
    elif step_type == constants.SET_STEP_TYPE:
        counts[work_type] = count

    utils.__save_counts(counts)

    del steps[-1:]


def __print_progress(title, current, total, additional=None):
    text = f'{title}\n[{int(current) * "-"}{int(total - current) * " "}] {current} / {total}'
    if additional:
        text += f' ({additional})'
    text += '\n'
    print(text)


def __see_progress():
    start_date = dt.datetime.fromisoformat(constants.START_DATE)
    end_date = dt.datetime.fromisoformat(constants.END_DATE)

    weekdays = rrule.rrule(rrule.DAILY, byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR),
          dtstart=start_date,
          until=end_date)\
        .count()
    total_count = np.sum([work_type[1] * work_type[2] for work_type in constants.WORK_TYPES])

    exact_points_day = total_count / weekdays
    rounded_points_day = np.ceil(exact_points_day * 2) / 2

    elapsed_days =  rrule.rrule(rrule.DAILY, byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR),
          dtstart=start_date,
          until=dt.datetime.now())\
        .count()
    expected_exact = exact_points_day * elapsed_days
    expected_rounded = rounded_points_day * elapsed_days

    done = np.sum([counts[work_type[0]] * work_type[1] for work_type in constants.WORK_TYPES])

    lag_exact = expected_exact - done
    lag_exact = lag_exact if lag_exact >= 0 else 0
    lag_rounded = expected_rounded - done
    lag_rounded = lag_rounded if lag_rounded >= 0 else 0

    __print_progress('Current Progress', done, total_count)
    __print_progress('Expected Rounded Progress', expected_rounded, total_count, f'Lag: {lag_rounded}')
    __print_progress('Expected Exact Progress', expected_exact, total_count, f'Lag: {lag_exact}')

    questions = [
        inquirer.List(constants.ANSWER,
                      choices=[constants.BACK_STEP_TEXT]),
    ]
    inquirer.prompt(questions)
    __change_step(constants.BACK_STEP_TYPE)


def main():
    while True:
        if steps[-1] == constants.MAIN_MENU_STEP_TYPE:
            __main_menu()
        elif steps[-1] == constants.ADDITION_STEP_TYPE:
            __work_types(steps[-1])
        elif steps[-1] == constants.SUBTRACTION_STEP_TYPE:
            __work_types(steps[-1])
        elif steps[-1] == constants.SET_STEP_TYPE:
            __work_types(steps[-1])
        elif steps[-1] == constants.SEE_PROGRESS_STEP_TYPE:
            __see_progress()
        elif steps[-1] == constants.QUIT_STEP_TYPE:
            break


main()