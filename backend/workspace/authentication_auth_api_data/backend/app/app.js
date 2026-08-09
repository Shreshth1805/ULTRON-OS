const express = require('express');
const app = express();
const config = require('./config');
const database = require('./database');
const taskRoutes = require('./routes/taskRoutes');
const userRoutes = require('./routes/userRoutes');
const taskService = require('./services/taskService');
const userService = require('./services/userService');
const logger = require('./utils/logger');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/api/tasks', taskRoutes);
app.use('/api/users', userRoutes);

app.use((req, res, next) => {
  const error = new Error('Not Found');
  error.status = 404;
  next(error);
});

app.use((error, req, res, next) => {
  logger.error(error);
  res.status(error.status || 500);
  res.json({ error: error.message });
});

database.connect()
  .then(() => {
    app.listen(config.port, () => {
      logger.info(`Server listening on port ${config.port}`);
    });
  })
  .catch((error) => {
    logger.error(error);
    process.exit(1);
  });

module.exports = app;