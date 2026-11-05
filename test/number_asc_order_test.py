import random

import pytest

from src.custom_stack_class import CustomStack, StackEmptyException
from src.number_asc_order import NumberAscOrder


def make_stack_mock(mocker, numbers, limit=6):
    """Cria um mock de CustomStack que se comporta como uma pilha com `numbers`
    (o último da lista é o topo), sem usar a implementação real."""
    content = list(numbers)
    stack = mocker.Mock(spec=CustomStack)
    stack.limit = limit
    stack.is_empty.side_effect = lambda: len(content) == 0
    stack.pop.side_effect = lambda: content.pop()
    stack.push.side_effect = lambda element: content.append(element)
    stack.content = content  # facilita conferir o estado final nos testes
    return stack


def draw_six_numbers(seed):
    """Simula um sorteio da Mega Sena: 6 números distintos entre 1 e 60,
    na ordem em que saíram. A semente deixa a falha reproduzível."""
    return random.Random(seed).sample(range(1, 61), 6)


@pytest.fixture
def cut():
    return NumberAscOrder()


# ------------------------------------- cenário 1: pilha de 6 com 6 sorteados
@pytest.mark.parametrize("seed", range(5))
def test_sort_returns_the_six_drawn_numbers_in_ascending_order(mocker, cut, seed):
    drawn = draw_six_numbers(seed)
    stack = make_stack_mock(mocker, drawn)

    result = cut.sort(stack)

    assert isinstance(result, list)
    assert result == sorted(drawn)


def test_sort_with_known_draw(mocker, cut):
    stack = make_stack_mock(mocker, [42, 5, 60, 1, 33, 17])

    assert cut.sort(stack) == [1, 5, 17, 33, 42, 60]


def test_sort_with_numbers_already_in_ascending_order(mocker, cut):
    stack = make_stack_mock(mocker, [1, 2, 3, 4, 5, 6])

    assert cut.sort(stack) == [1, 2, 3, 4, 5, 6]


def test_sort_with_numbers_in_descending_order(mocker, cut):
    stack = make_stack_mock(mocker, [60, 59, 58, 57, 56, 55])

    assert cut.sort(stack) == [55, 56, 57, 58, 59, 60]


def test_sort_pops_exactly_six_times(mocker, cut):
    stack = make_stack_mock(mocker, draw_six_numbers(0))

    cut.sort(stack)

    assert stack.pop.call_count == 6


def test_sort_leaves_the_stack_as_it_was(mocker, cut):
    drawn = draw_six_numbers(1)
    stack = make_stack_mock(mocker, drawn)

    cut.sort(stack)

    assert stack.push.call_count == 6
    assert stack.content == drawn  # mesma ordem do sorteio, topo incluso


# ------------------------------------------- cenário 2: pilha de 6 e vazia
def test_sort_empty_stack_raises_stack_empty_exception(mocker, cut):
    stack = make_stack_mock(mocker, [])

    with pytest.raises(StackEmptyException):
        cut.sort(stack)


def test_sort_empty_stack_does_not_pop_or_push(mocker, cut):
    stack = make_stack_mock(mocker, [])

    with pytest.raises(StackEmptyException):
        cut.sort(stack)

    stack.pop.assert_not_called()
    stack.push.assert_not_called()


# ------------------------------------------------- demais verificações
@pytest.mark.parametrize("invalid_stack", [None, [1, 2, 3, 4, 5, 6], "123456", 42])
def test_sort_rejects_anything_that_is_not_a_custom_stack(cut, invalid_stack):
    with pytest.raises(TypeError):
        cut.sort(invalid_stack)


@pytest.mark.parametrize("numbers", [[1], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6, 7]])
def test_sort_rejects_stack_without_exactly_six_numbers(mocker, cut, numbers):
    stack = make_stack_mock(mocker, numbers, limit=7)

    with pytest.raises(ValueError):
        cut.sort(stack)


@pytest.mark.parametrize("out_of_range", [0, 61, -3, 100])
def test_sort_rejects_number_out_of_range(mocker, cut, out_of_range):
    stack = make_stack_mock(mocker, [1, 2, 3, 4, 5, out_of_range])

    with pytest.raises(ValueError):
        cut.sort(stack)


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]),  # menor valor válido (1)
        ([60, 2, 3, 4, 5, 6], [2, 3, 4, 5, 6, 60]),  # maior valor válido (60)
    ],
)
def test_sort_accepts_boundary_numbers(mocker, cut, numbers, expected):
    stack = make_stack_mock(mocker, numbers)

    assert cut.sort(stack) == expected


def test_sort_rejects_repeated_numbers(mocker, cut):
    stack = make_stack_mock(mocker, [7, 7, 1, 2, 3, 4])

    with pytest.raises(ValueError):
        cut.sort(stack)


@pytest.mark.parametrize("invalid", [3.5, "7", None, True])
def test_sort_rejects_non_integer_numbers(mocker, cut, invalid):
    stack = make_stack_mock(mocker, [1, 2, 3, 4, 5, invalid])

    with pytest.raises(TypeError):
        cut.sort(stack)


def test_sort_restores_the_stack_even_when_content_is_invalid(mocker, cut):
    invalid = [7, 7, 1, 2, 3, 4]
    stack = make_stack_mock(mocker, invalid)

    with pytest.raises(ValueError):
        cut.sort(stack)

    assert stack.content == invalid


# ------------------------------------- integração com a CustomStack real
def test_sort_with_real_custom_stack_keeps_draw_order(cut):
    drawn = draw_six_numbers(2)
    stack = CustomStack(6)
    for number in drawn:
        stack.push(number)

    assert cut.sort(stack) == sorted(drawn)
    assert stack.size() == 6
    assert [stack.pop() for _ in range(6)] == drawn[::-1]


def test_sort_with_real_empty_custom_stack_of_six_positions(cut):
    stack = CustomStack(6)

    with pytest.raises(StackEmptyException):
        cut.sort(stack)
