from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Simples lista de tarefas em memória.
tasks = []
task_id_counter = 1

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    global task_id_counter
    task_text = request.form.get('task_text')
    if not task_text or not validate_task(task_text):
        return redirect(url_for('index'))

    tasks.append({
        'id': task_id_counter,
        'text': task_text,
        'completed': False
    })
    task_id_counter += 1
    return redirect(url_for('index'))

@app.route('/toggle_complete/<int:task_id>')
def toggle_complete(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('index'))

# --- Funções de Lógica de Negócio para Teste Unitário ---
def validate_task(task_text):
    """Valida o texto de uma tarefa."""
    if not task_text or len(task_text.strip()) == 0:
        return False # A tarefa não pode ser vazia
    if len(task_text) > 100:
        return False # A tarefa não pode ter mais de 100 caracteres
    return True

if __name__ == '__main__':
    # Em ambiente de desenvolvimento, podemos rodar diretamente
    app.run(debug=True)
