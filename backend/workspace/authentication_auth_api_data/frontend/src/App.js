import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import AppContainer from './containers/AppContainer';
import TaskList from './components/TaskList';
import TaskForm from './components/TaskForm';
import taskService from './services/taskService';
import userService from './services/userService';
import config from './utils/config';

function App() {
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const tasks = await taskService.getAllTasks();
        setTasks(tasks);
      } catch (error) {
        setError(error.message);
      }
    };

    const fetchUsers = async () => {
      try {
        const users = await userService.getAllUsers();
        setUsers(users);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchTasks();
    fetchUsers();
  }, []);

  const handleLogin = async (username, password) => {
    try {
      const user = await userService.login(username, password);
      setCurrentUser(user);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
  };

  const handleCreateTask = async (task) => {
    try {
      const newTask = await taskService.createTask(task);
      setTasks([...tasks, newTask]);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleUpdateTask = async (task) => {
    try {
      const updatedTask = await taskService.updateTask(task);
      setTasks(tasks.map((t) => (t.id === updatedTask.id ? updatedTask : t)));
    } catch (error) {
      setError(error.message);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await taskService.deleteTask(taskId);
      setTasks(tasks.filter((task) => task.id !== taskId));
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <AppContainer>
      <BrowserRouter>
        <Switch>
          <Route
            path="/"
            exact
            render={() => (
              <TaskList
                tasks={tasks}
                users={users}
                currentUser={currentUser}
                handleCreateTask={handleCreateTask}
                handleUpdateTask={handleUpdateTask}
                handleDeleteTask={handleDeleteTask}
              />
            )}
          />
          <Route
            path="/create-task"
            render={() => (
              <TaskForm
                handleCreateTask={handleCreateTask}
                currentUser={currentUser}
              />
            )}
          />
          <Route
            path="/login"
            render={() => (
              <div>
                <h2>Login</h2>
                <form>
                  <label>Username:</label>
                  <input type="text" name="username" />
                  <br />
                  <label>Password:</label>
                  <input type="password" name="password" />
                  <br />
                  <button onClick={(e) => handleLogin('username', 'password')}>Login</button>
                </form>
              </div>
            )}
          />
          <Route
            path="/logout"
            render={() => (
              <div>
                <h2>Logout</h2>
                <button onClick={handleLogout}>Logout</button>
              </div>
            )}
          />
        </Switch>
      </BrowserRouter>
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </AppContainer>
  );
}

export default App;