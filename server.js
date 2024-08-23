const express = require('express');
const dotenv = require('dotenv');
const connectDB = require('./config/db');
const taskRoutes = require('./routes/tasks');
const userRoutes = require('./routes/users');

dotenv.config();
connectDB();

const app = express();

app.use(express.json());

app.use('/api/tasks', taskRoutes);
app.use('/api/users', userRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

