import axios from 'axios';
import taskService from '../../services/taskService';
import config from '../../utils/config';

jest.mock('axios');

describe('taskService', () => {
  const taskId = '12345';
  const task = {
    id: taskId,
    title: 'Test Task',
    description: 'This is a test task',
    status: 'pending',
  };

  beforeEach(() => {
    jest.resetAllMocks();
  });

  it('should get all tasks', async () => {
    const tasks = [task];
    axios.get.mockResolvedValue({ data: tasks });
    const result = await taskService.getTasks();
    expect(result).toEqual(tasks);
    expect(axios.get).toHaveBeenCalledTimes(1);
    expect(axios.get).toHaveBeenCalledWith(`${config.apiUrl}/tasks`);
  });

  it('should get a task by id', async () => {
    axios.get.mockResolvedValue({ data: task });
    const result = await taskService.getTask(taskId);
    expect(result).toEqual(task);
    expect(axios.get).toHaveBeenCalledTimes(1);
    expect(axios.get).toHaveBeenCalledWith(`${config.apiUrl}/tasks/${taskId}`);
  });

  it('should create a new task', async () => {
    axios.post.mockResolvedValue({ data: task });
    const result = await taskService.createTask(task);
    expect(result).toEqual(task);
    expect(axios.post).toHaveBeenCalledTimes(1);
    expect(axios.post).toHaveBeenCalledWith(`${config.apiUrl}/tasks`, task);
  });

  it('should update a task', async () => {
    axios.put.mockResolvedValue({ data: task });
    const result = await taskService.updateTask(taskId, task);
    expect(result).toEqual(task);
    expect(axios.put).toHaveBeenCalledTimes(1);
    expect(axios.put).toHaveBeenCalledWith(`${config.apiUrl}/tasks/${taskId}`, task);
  });

  it('should delete a task', async () => {
    axios.delete.mockResolvedValue({ data: task });
    const result = await taskService.deleteTask(taskId);
    expect(result).toEqual(task);
    expect(axios.delete).toHaveBeenCalledTimes(1);
    expect(axios.delete).toHaveBeenCalledWith(`${config.apiUrl}/tasks/${taskId}`);
  });

  it('should handle error when getting all tasks', async () => {
    axios.get.mockRejectedValue(new Error('Error getting tasks'));
    await expect(taskService.getTasks()).rejects.toThrowError('Error getting tasks');
    expect(axios.get).toHaveBeenCalledTimes(1);
    expect(axios.get).toHaveBeenCalledWith(`${config.apiUrl}/tasks`);
  });

  it('should handle error when getting a task by id', async () => {
    axios.get.mockRejectedValue(new Error('Error getting task'));
    await expect(taskService.getTask(taskId)).rejects.toThrowError('Error getting task');
    expect(axios.get).toHaveBeenCalledTimes(1);
    expect(axios.get).toHaveBeenCalledWith(`${config.apiUrl}/tasks/${taskId}`);
  });

  it('should handle error when creating a new task', async () => {
    axios.post.mockRejectedValue(new Error('Error creating task'));
    await expect(taskService.createTask(task)).rejects.toThrowError('Error creating task');
    expect(axios.post).toHaveBeenCalledTimes(1);
    expect(axios.post).toHaveBeenCalledWith(`${config.apiUrl}/tasks`, task);
  });

  it('should handle error when updating a task', async () => {
    axios.put.mockRejectedValue(new Error('Error updating task'));
    await expect(taskService.updateTask(taskId, task)).rejects.toThrowError('Error updating task');
    expect(axios.put).toHaveBeenCalledTimes(1);
    expect(axios.put).toHaveBeenCalledWith(`${config.apiUrl}/tasks/${taskId}`, task);
  });

  it('should handle error when deleting a task', async () => {
    axios.delete.mockRejectedValue(new Error('Error deleting task'));
    await expect(taskService.deleteTask(taskId)).rejects.toThrowError('Error deleting task');
    expect(axios.delete).toHaveBeenCalledTimes(1);
    expect(axios.delete).toHaveBeenCalledWith(`${config.apiUrl}/tasks/${taskId}`);
  });
});