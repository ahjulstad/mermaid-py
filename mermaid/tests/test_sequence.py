import unittest
from unittest import mock

from mermaid.sequence import Actor, ArrowTypes, Box, Link, Loop, Note, NotePosition, Participant,Alt


class TestActor(unittest.TestCase):
    def test_str(self):
        actor = Actor('John')
        expect_str = '\tActor John\n'
        self.assertEqual(str(actor), expect_str)


class TestParticipant(unittest.TestCase):
    def test_str(self):
        participant = Participant('Alice')
        expect_str = '\tparticipant alice as Alice\n'
        self.assertEqual(str(participant), expect_str)


class TestBox(unittest.TestCase):
    def test_str(self):
        # use mocks to create an actor and a participant element
        actor = mock.MagicMock(spec=Actor)
        actor.__str__ = mock.Mock(return_value='\tActor John\n')
        participant = mock.MagicMock(spec=Participant)
        participant.__str__ = mock.Mock(
            return_value='\tparticipant alice as Alice\n')

        box = Box('Test Box', [actor, participant])
        expect_str = """\tbox Test Box
\tActor John
\tparticipant alice as Alice
\tend\n"""
        self.assertEqual(str(box), expect_str)


class TestLink(unittest.TestCase):
    def setUp(self):
        self.source = mock.MagicMock(spec=Actor)
        self.source.id_ = 'John'
        self.target = mock.MagicMock(spec=Participant)
        self.target.id_ = 'Alice'

    def test_str_without_activation_deactivation(self):
        link = Link(self.source, self.target, 'Solid-line', 'Hello World')
        expected_str = '\tJohn->Alice: Hello World\n'
        self.assertEqual(str(link), expected_str)

    def test_str_with_arrow_type_classe(self):
        link = Link(self.source, self.target, ArrowTypes.SOLID_LINE,
                    'Hello World')
        expected_str = '\tJohn->Alice: Hello World\n'
        self.assertEqual(str(link), expected_str)

    def test_str_with_activation(self):
        link = Link(self.source,
                    self.target,
                    'Solid-line',
                    'Hello World',
                    activate_target=True)
        expected_str = '\tJohn->Alice: Hello World\nactivate Alice\n'
        self.assertEqual(str(link), expected_str)

    def test_str_with_deactivation(self):
        link = Link(self.source,
                    self.target,
                    'Solid-line',
                    'Hello World',
                    deactivate_target=True)
        expected_str = '\tJohn->Alice: Hello World\ndeactivate Alice\n'
        self.assertEqual(str(link), expected_str)


class TestNote(unittest.TestCase):
    def setUp(self) -> None:
        self.actor = mock.Mock(spec=Actor)
        self.actor.id_ = 'actor'
        self.participant = mock.Mock(spec=Participant)
        self.participant.id_ = 'participant'
        self.note = 'This is a note'
        return super().setUp()

    def test_note_str_single_element(self) -> None:
        note = Note(self.note, self.actor)
        self.assertEqual(str(note), '\tNote over actor: This is a note\n')

    def test_note_str_multiple_elements(self) -> None:
        note_multiple = Note(self.note, [self.actor, self.participant],
                             NotePosition.OVER)
        self.assertEqual(str(note_multiple),
                         '\tNote over actor,participant: This is a note\n')

    def test_note_position(self) -> None:
        note_left = Note(self.note, self.actor, NotePosition.LEFT_OF)
        self.assertEqual(str(note_left),
                         '\tNote left of actor: This is a note\n')
        note_right = Note(self.note, self.actor, NotePosition.RIGHT_OF)
        self.assertEqual(str(note_right),
                         '\tNote right of actor: This is a note\n')

    def test_note_assertion(self) -> None:
        with self.assertRaises(ValueError):
            Note(self.note, [self.actor, self.participant],
                 NotePosition.LEFT_OF)
        with self.assertRaises(ValueError):
            Note(self.note, [self.actor, self.participant],
                 NotePosition.RIGHT_OF)


class TestLoop(unittest.TestCase):
    def test_loop_str(self) -> None:
        link = mock.MagicMock(spec=Link)
        link.configure_mock(__str__=lambda _: '\tJohn->Alice: Hello World\n')
        loop = Loop('condition', [link])
        self.assertEqual(
            str(loop), '\tloop condition\n\tJohn->Alice: Hello World\n\tend\n')


class TestAlt(unittest.TestCase):
    def setUp(self):
        self.link_1 = mock.MagicMock(spec=Link)
        self.link_1.configure_mock(__str__=lambda _: '\tA-->B: message\n')
        self.link_2 = mock.MagicMock(spec=Link)
        self.link_2.configure_mock(__str__=lambda _: '\tA-->B: message\n')

    def test_str_one_condition(self):
        alt = Alt({'condition': [self.link_1]})
        excepted_str = '\talt condition\n\tA-->B: message\n\tend\n'
        self.assertEqual(str(alt), excepted_str)
    
    def test_str_multiple_condition(self):
        alt = Alt({'condition-1': [self.link_1], 'condition-2': [self.link_2]})
        except_str = '\talt condition-1\n\tA-->B: message\n\telse condition-2\n\tA-->B: message\n\tend\n'
        self.assertEqual(str(alt), except_str)