const express = require('express');
const router = express.Router();
const taskService = require('../services/taskService');
const userService = require('../services/userService');
const authMiddleware = require('../utils/authMiddleware');
const { validateTask } = require('../utils/validation');

router.use(authMiddleware);

router.get('/', async (req, res) => {
    try {
        const tasks = await taskService.getTasks(req.user.id);
        res.json(tasks);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to retrieve tasks' });
    }
});

router.get('/:id', async (req, res) => {
    try {
        const taskId = req.params.id;
        const task = await taskService.getTask(taskId, req.user.id);
        if (!task) {
            res.status(404).json({ message: 'Task not found' });
        } else {
            res.json(task);
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to retrieve task' });
    }
});

router.post('/', async (req, res) => {
    try {
        const taskData = req.body;
        const validationError = validateTask(taskData);
        if (validationError) {
            res.status(400).json({ message: validationError });
        } else {
            const task = await taskService.createTask(taskData, req.user.id);
            res.json(task);
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to create task' });
    }
});

router.put('/:id', async (req, res) => {
    try {
        const taskId = req.params.id;
        const taskData = req.body;
        const validationError = validateTask(taskData);
        if (validationError) {
            res.status(400).json({ message: validationError });
        } else {
            const task = await taskService.updateTask(taskId, taskData, req.user.id);
            if (!task) {
                res.status(404).json({ message: 'Task not found' });
            } else {
                res.json(task);
            }
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to update task' });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        const taskId = req.params.id;
        await taskService.deleteTask(taskId, req.user.id);
        res.json({ message: 'Task deleted successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to delete task' });
    }
});

module.exports = router;