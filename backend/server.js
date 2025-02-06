import OpenAI from "openai";
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

const app = express();
const port = process.env.PORT || 8080;

app.use(cors());
app.use(express.json());

app.get('/config', (req, res) => {
    res.json({ OPENAI_API_KEY: process.env.OPENAI_API_KEY });
});

app.post('/api/chat', async (req, res) => {
    const { messages } = req.body;

    try {
        const response = await openai.chat.completions.create({
            model: 'gpt-4o',
            store: true,
            messages: messages,
        });

        res.json(response);
    } catch (error) {
        console.error('Error:', error.response ? error.response.data : error.message);
        res.status(500).json({ error: 'Error communicating with the chatbot.' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});