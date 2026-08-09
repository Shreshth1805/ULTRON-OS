const express = require('express');
const app = express();
const config = require('./config');
const database = require('./database');
const taskRoutes = require('./routes/taskRoutes');
const userRoutes = require('./routes/userRoutes');
const taskService = require('./services/taskService');
const userService = require('./services/userService');
const authMiddleware = require('./utils/authMiddleware');
const errorMiddleware = require('./utils/errorMiddleware');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/api/tasks', authMiddleware, taskRoutes);
app.use('/api/users', authMiddleware, userRoutes);

app.use(errorMiddleware);

const port = config.port;

database.connect()
    .then(() => {
        app.listen(port, () => {
            console.log(`Server listening on port ${port}`);
        });
    })
    .catch((error) => {
        console.error('Error starting server:', error);
        process.exit(1);
    });

module.exports = app;