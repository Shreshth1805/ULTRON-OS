import axios from 'axios';
import { apiUrl } from '../utils/config';

const taskService = {
  async getTasks() {
    try {
      const response = await axios.get(`${apiUrl}/tasks`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getTaskById(id) {
    try {
      const response = await axios.get(`${apiUrl}/tasks/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async createTask(task) {
    try {
      const response = await axios.post(`${apiUrl}/tasks`, task);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async updateTask(id, task) {
    try {
      const response = await axios.put(`${apiUrl}/tasks/${id}`, task);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async deleteTask(id) {
    try {
      const response = await axios.delete(`${apiUrl}/tasks/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async assignTask(id, userId) {
    try {
      const response = await axios.patch(`${apiUrl}/tasks/${id}/assign`, { userId });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async completeTask(id) {
    try {
      const response = await axios.patch(`${apiUrl}/tasks/${id}/complete`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default taskService;