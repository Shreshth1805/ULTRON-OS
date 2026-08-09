const express = require('express');
const router = express.Router();
const taskService = require('../services/taskService');
const authService = require('../services/authService');
const { validateTask } = require('../utils/validation');

router.use(express.json());

router.get('/', authService.authenticate, async (req, res) => {
    try {
        const tasks = await taskService.getTasks(req.user.id);
        res.json(tasks);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to retrieve tasks' });
    }
});

router.get('/:id', authService.authenticate, async (req, res) => {
    try {
        const id = req.params.id;
        const task = await taskService.getTask(id, req.user.id);
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

router.post('/', authService.authenticate, async (req, res) => {
    try {
        const task = req.body;
        const errors = validateTask(task);
        if (errors.length > 0) {
            res.status(400).json({ errors });
        } else {
            const newTask = await taskService.createTask(task, req.user.id);
            res.json(newTask);
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to create task' });
    }
});

router.put('/:id', authService.authenticate, async (req, res) => {
    try {
        const id = req.params.id;
        const task = req.body;
        const errors = validateTask(task);
        if (errors.length > 0) {
            res.status(400).json({ errors });
        } else {
            const updatedTask = await taskService.updateTask(id, task, req.user.id);
            if (!updatedTask) {
                res.status(404).json({ message: 'Task not found' });
            } else {
                res.json(updatedTask);
            }
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to update task' });
    }
});

router.delete('/:id', authService.authenticate, async (req, res) => {
    try {
        const id = req.params.id;
        await taskService.deleteTask(id, req.user.id);
        res.json({ message: 'Task deleted successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Failed to delete task' });
    }
});

module.exports = router;