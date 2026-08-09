const request = require('supertest');
const app = require('../../app/app');
const Task = require('../../app/models/taskModel');
const User = require('../../app/models/userModel');
const taskService = require('../../app/services/taskService');
const userService = require('../../app/services/userService');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

describe('Task Controller', () => {
  let token;
  let taskId;

  beforeAll(async () => {
    await Task.deleteMany({});
    await User.deleteMany({});

    const user = new User({
      name: 'Test User',
      email: 'test@example.com',
      password: bcrypt.hashSync('password', 10),
    });

    await user.save();

    const response = await request(app)
      .post('/api/v1/users/login')
      .send({ email: 'test@example.com', password: 'password' });

    token = response.body.token;

    const task = new Task({
      title: 'Test Task',
      description: 'This is a test task',
      assignedTo: user._id,
    });

    await task.save();
    taskId = task._id;
  });

  afterAll(async () => {
    await Task.deleteMany({});
    await User.deleteMany({});
  });

  it('should create a new task', async () => {
    const response = await request(app)
      .post('/api/v1/tasks')
      .set("Authorization", `Bearer ${token}`)
      .send({ title: 'New Task', description: 'This is a new task' });

    expect(response.status).toBe(201);
    expect(response.body.title).toBe('New Task');
    expect(response.body.description).toBe('This is a new task');
  });

  it('should get all tasks', async () => {
    const response = await request(app)
      .get('/api/v1/tasks')
      .set("Authorization", `Bearer ${token}`);

    expect(response.status).toBe(200);
    expect(response.body.length).toBeGreaterThan(0);
  });

  it('should get a task by id', async () => {
    const response = await request(app)
      .get(`/api/v1/tasks/${taskId}`)
      .set("Authorization", `Bearer ${token}`);

    expect(response.status).toBe(200);
    expect(response.body.title).toBe('Test Task');
    expect(response.body.description).toBe('This is a test task');
  });

  it('should update a task', async () => {
    const response = await request(app)
      .patch(`/api/v1/tasks/${taskId}`)
      .set("Authorization", `Bearer ${token}`)
      .send({ title: 'Updated Task' });

    expect(response.status).toBe(200);
    expect(response.body.title).toBe('Updated Task');
  });

  it('should delete a task', async () => {
    const response = await request(app)
      .delete(`/api/v1/tasks/${taskId}`)
      .set("Authorization", `Bearer ${token}`);

    expect(response.status).toBe(204);
  });

  it('should return 401 for unauthorized requests', async () => {
    const response = await request(app)
      .get('/api/v1/tasks');

    expect(response.status).toBe(401);
  });

  it('should return 404 for non-existent tasks', async () => {
    const response = await request(app)
      .get('/api/v1/tasks/1234567890')
      .set("Authorization", `Bearer ${token}`);

    expect(response.status).toBe(404);
  });
});