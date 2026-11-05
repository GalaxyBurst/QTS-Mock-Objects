from src.custom_stack_class import CustomStack, StackEmptyException


class NumberAscOrder:
    """Coleta os números sorteados da Mega Sena guardados em uma CustomStack
    e os devolve em ordem ascendente."""

    DRAWN_NUMBERS = 6
    MIN_NUMBER = 1
    MAX_NUMBER = 60

    def sort(self, stack):
        """Retorna um list() com os números da pilha em ordem ascendente.

        A pilha é percorrida apenas pela interface pública (is_empty, pop e
        push) e é devolvida ao estado original, ou seja, a ordem do sorteio
        não se perde para quem chamou.

        Raises:
            TypeError: se `stack` não for uma CustomStack ou se algum número
                não for inteiro.
            StackEmptyException: se a pilha estiver vazia.
            ValueError: se a pilha não tiver exatamente 6 números, se algum
                estiver fora do intervalo 1..60 ou se houver repetidos.
        """
        if not isinstance(stack, CustomStack):
            raise TypeError("stack deve ser uma instância de CustomStack")

        if stack.is_empty():
            raise StackEmptyException

        # Esvazia a pilha: o primeiro a sair é o último número sorteado.
        drawn = []
        while not stack.is_empty():
            drawn.append(stack.pop())

        # Restaura a pilha antes de validar, para que ela fique intacta
        # mesmo quando o conteúdo for inválido.
        for number in reversed(drawn):
            stack.push(number)

        self._validate(drawn)

        return sorted(drawn)

    def _validate(self, numbers):
        if len(numbers) != self.DRAWN_NUMBERS:
            raise ValueError(
                f"esperados {self.DRAWN_NUMBERS} números, recebidos {len(numbers)}"
            )

        for number in numbers:
            # bool é subclasse de int, mas não é um número sorteado válido.
            if isinstance(number, bool) or not isinstance(number, int):
                raise TypeError(f"número inválido: {number!r} (esperado int)")
            if not self.MIN_NUMBER <= number <= self.MAX_NUMBER:
                raise ValueError(
                    f"número fora do intervalo "
                    f"{self.MIN_NUMBER}..{self.MAX_NUMBER}: {number}"
                )

        if len(set(numbers)) != len(numbers):
            raise ValueError("números sorteados repetidos")
