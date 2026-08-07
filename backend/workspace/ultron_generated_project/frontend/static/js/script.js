const todoList = document.getElementById('todo-list');
const todoInput = document.getElementById('todo-input');
const todoForm = document.getElementById('todo-form');

let todos = [];

// Fetch todos from API on page load
fetch('/api/todos')
  .then(response => response.json())
  .then(data => {
    todos = data;
    renderTodos();
  })
  .catch(error => console.error('Error fetching todos:', error));

// Render todos in the list
function renderTodos() {
  const todoHtml = todos.map(todo => {
    return `
      <li>
        <input type="checkbox" id="todo-${todo.id}" ${todo.completed ? 'checked' : ''}>
        <span>${todo.title}</span>
        <button class="delete-btn" data-id="${todo.id}">Delete</button>
      </li>
    `;
  }).join('');
  todoList.innerHTML = todoHtml;
}

// Handle form submission to create a new todo
todoForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const title = todoInput.value.trim();
  if (title) {
    fetch('/api/todos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title }),
    })
      .then(response => response.json())
      .then(data => {
        todos.push(data);
        renderTodos();
        todoInput.value = '';
      })
      .catch(error => console.error('Error creating todo:', error));
  }
});

// Handle checkbox toggle to update a todo's completion status
todoList.addEventListener('change', (event) => {
  if (event.target.type === 'checkbox') {
    const todoId = event.target.id.split('-')[1];
    const todo = todos.find((todo) => todo.id === parseInt(todoId));
    if (todo) {
      fetch(`/api/todos/${todoId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: event.target.checked }),
      })
        .then(response => response.json())
        .then(data => {
          todo.completed = data.completed;
          renderTodos();
        })
        .catch(error => console.error('Error updating todo:', error));
    }
  }
});

// Handle delete button click to delete a todo
todoList.addEventListener('click', (event) => {
  if (event.target.classList.contains('delete-btn')) {
    const todoId = event.target.dataset.id;
    fetch(`/api/todos/${todoId}`, {
      method: 'DELETE',
    })
      .then(response => response.json())
      .then(data => {
        todos = todos.filter((todo) => todo.id !== parseInt(todoId));
        renderTodos();
      })
      .catch(error => console.error('Error deleting todo:', error));
  }
});