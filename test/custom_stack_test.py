import pytest

from src.custom_stack_class import CustomStack, StackEmptyException, StackFullException


# ---------------------------------------------------------------- push / top
def test_push_one_elementinstack():
    element_value = 5.0

    cut = CustomStack(5)
    cut.push(element_value)
    assert cut.is_empty() == False
    assert element_value == cut.top()
    assert 1 == cut.size()


def test_push_many_elements_top_is_the_last_one():
    cut = CustomStack(5)
    for element in (1, 2, 3):
        cut.push(element)

    assert cut.size() == 3
    assert cut.top() == 3


def test_push_until_limit_is_allowed():
    cut = CustomStack(3)
    for element in (1, 2, 3):
        cut.push(element)

    assert cut.size() == 3


def test_push_beyond_limit_raises_stack_full_exception():
    cut = CustomStack(2)
    cut.push(1)
    cut.push(2)

    with pytest.raises(StackFullException):
        cut.push(3)


def test_push_beyond_limit_does_not_change_the_stack():
    cut = CustomStack(2)
    cut.push(1)
    cut.push(2)

    with pytest.raises(StackFullException):
        cut.push(3)

    assert cut.size() == 2
    assert cut.top() == 2


def test_push_on_stack_with_limit_zero_raises_stack_full_exception():
    cut = CustomStack(0)

    with pytest.raises(StackFullException):
        cut.push(1)


def test_top_does_not_remove_the_element():
    cut = CustomStack(5)
    cut.push(7)

    assert cut.top() == 7
    assert cut.top() == 7
    assert cut.size() == 1


def test_top_on_empty_stack_raises_stack_empty_exception():
    cut = CustomStack(5)

    with pytest.raises(StackEmptyException):
        cut.top()


# ---------------------------------------------------------------------- pop
def test_pop_returns_last_pushed_element_and_removes_it():
    cut = CustomStack(5)
    cut.push(1)
    cut.push(2)

    assert cut.pop() == 2
    assert cut.size() == 1
    assert cut.top() == 1


def test_pop_follows_lifo_order():
    cut = CustomStack(5)
    for element in (1, 2, 3):
        cut.push(element)

    assert [cut.pop(), cut.pop(), cut.pop()] == [3, 2, 1]
    assert cut.is_empty()


def test_pop_on_empty_stack_raises_stack_empty_exception():
    cut = CustomStack(5)

    with pytest.raises(StackEmptyException):
        cut.pop()


def test_pop_after_emptying_the_stack_raises_stack_empty_exception():
    cut = CustomStack(5)
    cut.push(1)
    cut.pop()

    with pytest.raises(StackEmptyException):
        cut.pop()


# ------------------------------------------------------- size / is_empty
def test_new_stack_is_empty_and_has_size_zero():
    cut = CustomStack(5)

    assert cut.is_empty() is True
    assert cut.size() == 0


def test_stack_is_not_empty_after_push():
    cut = CustomStack(5)
    cut.push(1)

    assert cut.is_empty() is False


def test_stack_keeps_the_limit_given_in_the_constructor():
    cut = CustomStack(6)

    assert cut.limit == 6
    assert cut.elements == []
