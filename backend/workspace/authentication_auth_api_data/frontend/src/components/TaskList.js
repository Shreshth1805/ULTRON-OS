import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Task from './Task';
import { taskService } from '../services/taskService';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true);
      try {
        const response = await taskService.getTasks();
        setTasks(response.data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchTasks();
  }, []);

  const handleDeleteTask = async (taskId) => {
    try {
      await taskService.deleteTask(taskId);
      setTasks(tasks.filter((task) => task.id !== taskId));
    } catch (error) {
      setError(error.message);
    }
  };

  const handleUpdateTask = async (taskId, updatedTask) => {
    try {
      await taskService.updateTask(taskId, updatedTask);
      setTasks(tasks.map((task) => (task.id === taskId ? updatedTask : task)));
    } catch (error) {
      setError(error.message);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Task List</h1>
      {tasks.map((task) => (
        <Task
          key={task.id}
          task={task}
          onDelete={() => handleDeleteTask(task.id)}
          onUpdate={(updatedTask) => handleUpdateTask(task.id, updatedTask)}
        />
      ))}
    </div>
  );
};

export default TaskList;