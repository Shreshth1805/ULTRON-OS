import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';
import { taskService } from '../services/taskService';
import { userService } from '../services/userService';
import { authHeader } from '../utils/authHeader';

const AppContainer = () => {
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await taskService.getTasks();
        setTasks(response.data);
      } catch (error) {
        setError(error.message);
      }
    };

    const fetchUsers = async () => {
      try {
        const response = await userService.getUsers();
        setUsers(response.data);
      } catch (error) {
        setError(error.message);
      }
    };

    const fetchCurrentUser = async () => {
      try {
        const response = await userService.getCurrentUser();
        setCurrentUser(response.data);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchTasks();
    fetchUsers();
    fetchCurrentUser();
  }, []);

  const handleTaskCreate = async (task) => {
    try {
      const response = await taskService.createTask(task);
      setTasks([...tasks, response.data]);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleTaskUpdate = async (task) => {
    try {
      const response = await taskService.updateTask(task);
      setTasks(tasks.map((t) => (t.id === task.id ? response.data : t)));
    } catch (error) {
      setError(error.message);
    }
  };

  const handleTaskDelete = async (taskId) => {
    try {
      await taskService.deleteTask(taskId);
      setTasks(tasks.filter((task) => task.id !== taskId));
    } catch (error) {
      setError(error.message);
    }
  };

  const handleUserCreate = async (user) => {
    try {
      const response = await userService.createUser(user);
      setUsers([...users, response.data]);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleUserUpdate = async (user) => {
    try {
      const response = await userService.updateUser(user);
      setUsers(users.map((u) => (u.id === user.id ? response.data : u)));
    } catch (error) {
      setError(error.message);
    }
  };

  const handleUserDelete = async (userId) => {
    try {
      await userService.deleteUser(userId);
      setUsers(users.filter((user) => user.id !== userId));
    } catch (error) {
      setError(error.message);
    }
  };

  const handleLogin = async (credentials) => {
    try {
      const response = await userService.login(credentials);
      setCurrentUser(response.data);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleLogout = async () => {
    try {
      await userService.logout();
      setCurrentUser(null);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <BrowserRouter>
      <Switch>
        <Route
          path="/tasks"
          render={(props) => (
            <TaskList
              tasks={tasks}
              users={users}
              currentUser={currentUser}
              handleTaskCreate={handleTaskCreate}
              handleTaskUpdate={handleTaskUpdate}
              handleTaskDelete={handleTaskDelete}
              {...props}
            />
          )}
        />
        <Route
          path="/tasks/create"
          render={(props) => (
            <TaskForm
              handleTaskCreate={handleTaskCreate}
              {...props}
            />
          )}
        />
        <Route
          path="/tasks/:taskId/edit"
          render={(props) => (
            <TaskForm
              task={tasks.find((task) => task.id === props.match.params.taskId)}
              handleTaskUpdate={handleTaskUpdate}
              {...props}
            />
          )}
        />
        <Route
          path="/users"
          render={(props) => (
            <div>
              <h1>Users</h1>
              <ul>
                {users.map((user) => (
                  <li key={user.id}>{user.name}</li>
                ))}
              </ul>
            </div>
          )}
        />
        <Route
          path="/login"
          render={(props) => (
            <div>
              <h1>Login</h1>
              <form onSubmit={(event) => handleLogin(event)}>
                <label>
                  Username:
                  <input type="text" name="username" />
                </label>
                <br />
                <label>
                  Password:
                  <input type="password" name="password" />
                </label>
                <br />
                <button type="submit">Login</button>
              </form>
            </div>
          )}
        />
        <Route
          path="/logout"
          render={(props) => (
            <div>
              <h1>Logout</h1>
              <button onClick={handleLogout}>Logout</button>
            </div>
          )}
        />
      </Switch>
    </BrowserRouter>
  );
};

export default AppContainer;