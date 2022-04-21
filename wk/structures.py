from dataclasses import dataclass
from datetime import datetime

@dataclass
class Meaning:
    meaning: str
    primary: bool
    accepted_answer: bool

@dataclass
class Reading:
    reading: str
    primary: bool
    accepted_answer: bool
    type: str

@dataclass
class ContextSentence:
    english: str
    japanese: str

class Subject:
    def __init__(self, data: dict) -> None:
        self.data = data['data']
        self.type = data['object']

    def get_auxiliary_meanings(self) -> list[Meaning]:
        d = self.data['auxiliary_meanings']
        arr = []

        for e in d:
            arr.append(Meaning(e['meaning'], e['primary'], False))

        return arr

    def get_characters(self) -> str:
        return self.data['characters']

    def created_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['created_at'])

    def get_lesson_position(self) -> int:
        return self.data['level_position']

    def get_level(self) -> int:
        return self.data['level']

    def get_meaning_mnemonic(self) -> str:
        return self.data['meaning_mnemonic']

    def get_meanings(self) -> list[Meaning]:
        d = self.data['meanings']
        arr = []

        for e in d:
            arr.append(Meaning(e['meaning'], e['primary'], e['accepted_answer']))

        return arr

    def get_slug(self) -> str:
        return self.data['slug']

class Radical(Subject):
    def __init__(self, data: dict) -> None:
        super().__init__(data)

    def get_amalgamation_subject_ids(self) -> list[int]:
        return self.data['amalgamation_subject_ids']

class Kanji(Subject):
    def __init__(self, data: dict) -> None:
        super().__init__(data)

    def get_amalgamation_subject_ids(self) -> list[int]:
        return self.data['amalgamation_subject_ids']

    def get_component_subject_ids(self) -> list[int]:
        return self.data['component_subject_ids']

    def get_meaning_hint(self) -> str:
        return self.data['meaning_hint']

    def get_reading_hint(self) -> str:
        return self.data['reading_hint']

    def get_reading_mnemonic(self) -> str:
        return self.data['reading_mnemonic']

    def get_readings(self) -> list[Reading]:
        d = self.data['readings']
        arr = []

        for e in d:
            arr.append(Reading(e['reading'], e['primary'], e['accepted_answer'], e['type']))

        return arr

    def get_visually_similar_subject_ids(self) -> list[int]:
        return self.data['visually_similar_subject_ids']

class Vocabulary(Subject):
    def __init__(self, data: dict) -> None:
        super().__init__(data)

    def get_component_subject_ids(self) -> list[int]:
        return self.data['component_subject_ids']

    def get_context_sentences(self) -> list[ContextSentence]:
        d = self.data['context_sentences']
        arr = []

        for e in d:
            arr.append(ContextSentence(e['en'], e['ja']))

        return arr

    def get_parts_of_speech(self) -> list[str]:
        return self.data['parts_of_speech']

    def get_readings(self) -> list[Reading]:
        d = self.data['readings']
        arr = []

        for e in d:
            arr.append(Reading(e['reading'], e['primary'], e['accepted_answer'], e['type']))

        return arr

    def get_reading_mnemonic(self) -> str:
        return self.data['reading_mnemonic']

class Assignment:
    def __init__(self, data: dict) -> None:
        self.data = data['data']

    def available_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['available_at'])

    def created_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['crated_at'])

    def is_hidden(self) -> bool:
        return self.data['hidden']

    def passed_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['passed_at'])

    def resurrected_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['resurrected_at'])

    def get_srs_stage(self) -> int:
        return self.data['srs_stage']

    def started_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['started_at'])

    def get_subject_id(self) -> int:
        return self.data['subject_id']

    def get_subject_type(self) -> str:
        return self.data['subject_type']

    def unlocked_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['unlocked_at'])

class LevelProgression:
    def __init__(self, data: dict) -> None:
        self.data = data['data']

    def abandoned_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['abandoned_at'])

    def completed_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['completed_at'])

    def created_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['created_at'])

    def get_level(self) -> int:
        return self.data['level']

    def passed_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['passed_at'])

    def started_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['started_at'])

    def unlocked_at(self) -> datetime | None:
        return _timestamp_to_datetime(self.data['unlocked_at'])

class Review:
    def __init__(self, data: dict) -> None:
        self.data = data['data']

    def get_assignment_id(self) -> int:
        return self.data['assignment_id']

    def created_at(self) -> datetime:
        return _timestamp_to_datetime(self.data['created_at'])

    def get_ending_srs_stage(self) -> int:
        return self.data['ending_srs_stage']

    def get_incorrect_meaning_answers(self) -> int:
        return self.data['incorrect_meaning_answers']

    def get_incorrect_reading_answers(self) -> int:
        return self.data['incorrect_reading_answers']

    def get_srs_id(self) -> int:
        return self.data['spaced_repetition_system_id']

    def get_starting_srs_stage(self) -> int:
        return self.data['starting_srs_stage']

    def get_subject_id(self) -> int:
        return self.data['subject_id']

def _timestamp_to_datetime(timestamp: str) -> datetime | None:
    if str is None:
        return None

    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
