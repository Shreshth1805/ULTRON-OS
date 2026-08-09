const express = require('express');
const router = express.Router();
const userService = require('../services/userService');
const authMiddleware = require('../utils/authMiddleware');
const validationMiddleware = require('../utils/validationMiddleware');
const { validateUser } = require('../utils/validation');

router.use(authMiddleware.authenticate);

router.get('/', async (req, res) => {
    try {
        const users = await userService.getAllUsers();
        res.json(users);
    } catch (error) {
        res.status(500).json({ message: 'Failed to retrieve users' });
    }
});

router.get('/:id', async (req, res) => {
    try {
        const id = req.params.id;
        const user = await userService.getUserById(id);
        if (!user) {
            res.status(404).json({ message: 'User not found' });
        } else {
            res.json(user);
        }
    } catch (error) {
        res.status(500).json({ message: 'Failed to retrieve user' });
    }
});

router.post('/', validationMiddleware(validateUser), async (req, res) => {
    try {
        const user = await userService.createUser(req.body);
        res.json(user);
    } catch (error) {
        res.status(500).json({ message: 'Failed to create user' });
    }
});

router.put('/:id', validationMiddleware(validateUser), async (req, res) => {
    try {
        const id = req.params.id;
        const user = await userService.updateUser(id, req.body);
        if (!user) {
            res.status(404).json({ message: 'User not found' });
        } else {
            res.json(user);
        }
    } catch (error) {
        res.status(500).json({ message: 'Failed to update user' });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        const id = req.params.id;
        await userService.deleteUser(id);
        res.json({ message: 'User deleted successfully' });
    } catch (error) {
        res.status(500).json({ message: 'Failed to delete user' });
    }
});

module.exports = router;