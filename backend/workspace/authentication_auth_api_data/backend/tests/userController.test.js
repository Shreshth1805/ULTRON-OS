const request = require('supertest');
const app = require('../../app');
const { User } = require('../../app/models/userModel');
const { Task } = require('../../app/models/taskModel');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

describe('User Controller', () => {
  let token;
  let userId;

  beforeAll(async () => {
    await User.deleteMany({});
    const user = new User({
      name: 'Test User',
      email: 'test@example.com',
      password: await bcrypt.hash('password', 10),
    });
    await user.save();
    const response = await request(app).post('/api/v1/users/login').send({
      email: 'test@example.com',
      password: 'password',
    });
    token = response.body.token;
    userId = response.body.userId;
  });

  afterAll(async () => {
    await User.deleteMany({});
  });

  it('should register a new user', async () => {
    const response = await request(app)
      .post('/api/v1/users')
      .send({
        name: 'New User',
        email: 'new@example.com',
        password: 'password',
      })
      .expect(201);
    expect(response.body.name).toBe('New User');
    expect(response.body.email).toBe('new@example.com');
  });

  it('should login an existing user', async () => {
    const response = await request(app)
      .post('/api/v1/users/login')
      .send({
        email: 'test@example.com',
        password: 'password',
      })
      .expect(200);
    expect(response.body.token).not.toBeNull();
    expect(response.body.userId).not.toBeNull();
  });

  it('should get the current user', async () => {
    const response = await request(app)
      .get('/api/v1/users/me')
      .set("Authorization", `Bearer ${token}`)
      .expect(200);
    expect(response.body.name).toBe('Test User');
    expect(response.body.email).toBe('test@example.com');
  });

  it('should update the current user', async () => {
    const response = await request(app)
      .patch('/api/v1/users/me')
      .set("Authorization", `Bearer ${token}`)
      .send({
        name: 'Updated User',
      })
      .expect(200);
    expect(response.body.name).toBe('Updated User');
    expect(response.body.email).toBe('test@example.com');
  });

  it('should delete the current user', async () => {
    const response = await request(app)
      .delete('/api/v1/users/me')
      .set("Authorization", `Bearer ${token}`)
      .expect(204);
    expect(response.body).toBeNull();
  });

  it('should return 401 for unauthorized requests', async () => {
    const response = await request(app)
      .get('/api/v1/users/me')
      .expect(401);
    expect(response.body.error).toBe('Please authenticate.');
  });

  it('should return 404 for non-existent users', async () => {
    const response = await request(app)
      .get('/api/v1/users/12345')
      .set("Authorization", `Bearer ${token}`)
      .expect(404);
    expect(response.body.error).toBe('User not found');
  });
});