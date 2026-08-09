const Task = require('../models/taskModel');
const asyncHandler = require('async-handler');
const { NotFoundError, BadRequestError } = require('../utils/errors');

const getTasks = asyncHandler(async (req, res) => {
  const tasks = await Task.find().populate('assignee');
  res.json(tasks);
});

const getTask = asyncHandler(async (req, res) => {
  const taskId = req.params.taskId;
  const task = await Task.findById(taskId).populate('assignee');
  if (!task) {
    throw new NotFoundError(`Task not found with id ${taskId}`);
  }
  res.json(task);
});

const createTask = asyncHandler(async (req, res) => {
  const { title, description, assignee } = req.body;
  if (!title || !description) {
    throw new BadRequestError('Title and description are required');
  }
  const task = await Task.create({ title, description, assignee });
  res.status(201).json(task);
});

const updateTask = asyncHandler(async (req, res) => {
  const taskId = req.params.taskId;
  const task = await Task.findById(taskId);
  if (!task) {
    throw new NotFoundError(`Task not found with id ${taskId}`);
  }
  const { title, description, assignee } = req.body;
  if (title) task.title = title;
  if (description) task.description = description;
  if (assignee) task.assignee = assignee;
  await task.save();
  res.json(task);
});

const deleteTask = asyncHandler(async (req, res) => {
  const taskId = req.params.taskId;
  const task = await Task.findByIdAndDelete(taskId);
  if (!task) {
    throw new NotFoundError(`Task not found with id ${taskId}`);
  }
  res.status(204).json();
});

module.exports = {
  getTasks,
  getTask,
  createTask,
  updateTask,
  deleteTask,
};