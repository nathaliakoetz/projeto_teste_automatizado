import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

class TestGerenciadorTarefasSistema(unittest.TestCase):

    def setUp(self):
        # Configure o driver do navegador. Certifique-se de que o chromedriver está no seu PATH
        # ou especifique o caminho completo: executable_path="/caminho/para/chromedriver"
        self.driver = webdriver.Firefox()
        self.base_url = "http://127.0.0.1:5000/" # Onde sua aplicação Flask está rodando
        self.driver.get(self.base_url)
        # Maximize a janela para garantir que todos os elementos estejam visíveis
        self.driver.maximize_window()

    def tearDown(self):
        # Feche o navegador após cada teste
        self.driver.quit()

    def test_adicionar_e_verificar_tarefa(self):
        # Cenário de Teste de Sistema 1: Adicionar uma tarefa e verificar se ela aparece
        driver = self.driver
        tarefa_texto = "Estudar para a prova de testes"

        # 1. Encontrar o campo de entrada e digitar o texto da tarefa
        campo_tarefa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nova-tarefa"))
        )
        campo_tarefa.send_keys(tarefa_texto)

        # 2. Clicar no botão "Adicionar"
        botao_adicionar = driver.find_element(By.ID, "btn-adicionar")
        botao_adicionar.click()

        # 3. Verificar se a nova tarefa aparece na lista
        # Espera até que a tarefa com o texto desejado esteja visível na lista
        # O XPATH abaixo procura por um elemento li dentro de #lista-tarefas que contenha o texto da tarefa.
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//ul[@id='lista-tarefas']/li[contains(., '{tarefa_texto}')]"))
            )
            self.assertTrue(True, f"Tarefa '{tarefa_texto}' adicionada e visível na lista.")
        except:
            self.fail(f"Tarefa '{tarefa_texto}' não foi adicionada ou não está visível.")

        time.sleep(1) # Pequena pausa para visualização

    def test_marcar_e_desmarcar_tarefa(self):
        # Cenário de Teste de Sistema 2: Marcar e desmarcar uma tarefa como concluída 
        driver = self.driver
        tarefa_inicial = "Fazer exercícios físicos"

        # Adicionar uma tarefa que será marcada/desmarcada
        campo_tarefa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nova-tarefa"))
        )
        campo_tarefa.send_keys(tarefa_inicial)
        driver.find_element(By.ID, "btn-adicionar").click()

        # Esperar a tarefa aparecer na lista
        task_item_xpath = f"//li[contains(., '{tarefa_inicial}')]"
        task_item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, task_item_xpath))
        )
        
        # 1. Clicar no botão "Concluir" para a tarefa
        # Assumindo que o botão "Concluir" está dentro do item da lista
        toggle_button = task_item.find_element(By.CLASS_NAME, "toggle-btn")
        toggle_button.click()

        # 2. Verificar se a tarefa agora tem a classe 'completed' 
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"{task_item_xpath}[contains(@class, 'completed')]"))
        )
        self.assertIn("completed", task_item.get_attribute("class"), "Tarefa não foi marcada como concluída.")

        time.sleep(0.5) # Pausa para visualização

        # 3. Clicar no botão "Desfazer" para a tarefa
        # O texto do botão muda após ser clicado
        toggle_button = task_item.find_element(By.CLASS_NAME, "toggle-btn") # Re-encontrar o elemento
        toggle_button.click()

        # 4. Verificar se a tarefa não tem mais a classe 'completed'
        WebDriverWait(driver, 10).until_not(
            EC.presence_of_element_located((By.XPATH, f"{task_item_xpath}[contains(@class, 'completed')]"))
        )
        self.assertNotIn("completed", task_item.get_attribute("class"), "Tarefa não foi desmarcada.")

        time.sleep(1) # Pequena pausa para visualização


    def test_excluir_tarefa(self):
        # Cenário de Teste de Sistema Opcional: Excluir uma tarefa 
        driver = self.driver
        tarefa_para_excluir = "Comprar ingredientes para o jantar"

        # Adicionar uma tarefa para ser excluída
        campo_tarefa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nova-tarefa"))
        )
        campo_tarefa.send_keys(tarefa_para_excluir)
        driver.find_element(By.ID, "btn-adicionar").click()

        # Esperar a tarefa aparecer
        task_item_xpath = f"//li[contains(., '{tarefa_para_excluir}')]"
        task_item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, task_item_xpath))
        )

        # Clicar no botão "Excluir"
        delete_button = task_item.find_element(By.CLASS_NAME, "delete-btn")
        delete_button.click()

        # Verificar se a tarefa não está mais na lista
        WebDriverWait(driver, 10).until(
            EC.staleness_of(task_item) # Espera que o elemento fique "stale" 
        )
        # Uma verificação extra: tentar encontrar o texto da tarefa na lista (deve falhar)
        lista_tarefas = driver.find_element(By.ID, "lista-tarefas")
        self.assertNotIn(tarefa_para_excluir, lista_tarefas.text, "Tarefa não foi excluída da lista.")

        time.sleep(1)


if __name__ == '__main__':
    unittest.main()
