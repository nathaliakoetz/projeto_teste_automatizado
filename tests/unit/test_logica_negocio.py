import unittest
from app.app import validate_task, tasks 

class TestValidacaoTarefa(unittest.TestCase):
    # Cenário de Teste Unitário 1: Validação de entrada de tarefa

    def test_tarefa_vazia(self):
        result = validate_task("")
        self.assertFalse(result, "A tarefa não deve ser válida se for uma string vazia.")

    def test_tarefa_apenas_espacos(self):
        result = validate_task("   ")
        self.assertFalse(result, "A tarefa não deve ser válida se contiver apenas espaços.")

    def test_tarefa_muito_longa(self):
        tarefa_longa = "a" * 101 # 101 caracteres, excedendo o limite de 100
        result = validate_task(tarefa_longa)
        self.assertFalse(result, "A tarefa não deve ser válida se for muito longa.")

    def test_tarefa_valida(self):
        result = validate_task("Comprar pão e leite")
        self.assertTrue(result, "A tarefa deve ser válida.")

    def test_tarefa_com_limite_de_caracteres(self):
        tarefa_no_limite = "a" * 100 # 100 caracteres, no limite
        result = validate_task(tarefa_no_limite)
        self.assertTrue(result, "A tarefa deve ser válida se estiver no limite de caracteres.")


class TestManipulacaoTarefa(unittest.TestCase):
    # Cenário de Teste Unitário 2: Simulação de marcação de tarefa 

    def setUp(self):
        # Limpar a lista de tarefas antes de cada teste para garantir isolamento
        global tasks
        tasks = []
        # Adicionar algumas tarefas de teste
        tasks.append({'id': 1, 'text': 'Tarefa 1', 'completed': False})
        tasks.append({'id': 2, 'text': 'Tarefa 2', 'completed': False})
        tasks.append({'id': 3, 'text': 'Tarefa 3', 'completed': True}) # Tarefa já concluída

    def test_marcar_tarefa_existente_nao_concluida(self):
        from app.app import toggle_complete # Importa a função do app para simular
        toggle_complete(1) # Marca a Tarefa 1 como concluída
        found = False
        for task in tasks:
            if task['id'] == 1:
                self.assertTrue(task['completed'], "Tarefa 1 deve ser marcada como concluída.")
                found = True
                break
        self.assertTrue(found, "Tarefa 1 não encontrada na lista (erro de setUp/lógica).")

    def test_desmarcar_tarefa_existente_concluida(self):
        from app.app import toggle_complete
        toggle_complete(3) # Desmarca a Tarefa 3
        found = False
        for task in tasks:
            if task['id'] == 3:
                self.assertFalse(task['completed'], "Tarefa 3 deve ser desmarcada como concluída.")
                found = True
                break
        self.assertTrue(found, "Tarefa 3 não encontrada na lista (erro de setUp/lógica).")

    def test_marcar_tarefa_inexistente(self):
        from app.app import toggle_complete
        initial_tasks_state = [t.copy() for t in tasks] # Copia o estado inicial
        # Tentar marcar uma tarefa com ID que não existe
        toggle_complete(99)
        # Verifica se o estado das tarefas não mudou
        self.assertEqual(initial_tasks_state, tasks, "O estado das tarefas não deve mudar para ID inexistente.")


if __name__ == '__main__':
    unittest.main()
