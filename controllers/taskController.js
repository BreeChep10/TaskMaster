const Task = require('../models/task');

const getTasks = async (req, res) => {
    const tasks = await Task.find({ user: req.user.id });
    res.json(tasks);
};

const createTask = async (req, res) => {
    const { title, description } = req.body;
    const task = new Task({ title, description, user: req.user.id });
    await task.save();
    res.status(201).
	json(task);
};

const updateTask = async (req, res) => {
    const task = await Task.findById(req.params.id);

    if (!task || task.user.toString() !== req.user.id) {
        return res.status(404).json({ message: 'Task not found or not authorized' });
    }

    const updatedTask = await Task.findByIdAndUpdate(req.params.id, req.body, { new: true });
    res.json(updatedTask);
};

const deleteTask = async (req, res) => {
    const task = await Task.findById(req.params.id);

    if (!task || task.user.toString() !== req.user.id) {
        return res.status(404).json({ message: 'Task not found or not authorized' });
    }

    await task.remove();
    res.json({ message: 'Task removed' });
};

module.exports = {
    getTasks,
    createTask,
    updateTask,
    deleteTask,
};

