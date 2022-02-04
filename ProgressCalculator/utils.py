import typing
import constants
import pickle


def get_step_by_text(text: str) -> typing.Tuple:
    for step in constants.STEP_TYPES:
        if step[1] == text:
            return step


def get_work_type_by_text(text: str) -> typing.Tuple:
    for work_type in constants.WORK_TYPES:
        if work_type[-1] == text:
            return work_type


def __load_counts():
    default_counts = {
        constants.MODULE_TYPE: 0,
        constants.COURSEWORK_TYPE: 0,
        constants.PROJECT_TYPE: 0,
    }

    try:
        with open(f'{constants.WORK_DIR}/counts.pkl', 'rb') as f:
            counts = pickle.load(f)
            if counts:
                return counts
            else:
                return default_counts
    except:
        return default_counts


def __save_counts(counts):
    with open(f'{constants.WORK_DIR}/counts.pkl', 'wb') as f:
        pickle.dump(counts, f)
