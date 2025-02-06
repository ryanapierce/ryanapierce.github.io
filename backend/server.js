import OpenAI from "openai";
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import rateLimit from 'express-rate-limit';

dotenv.config();

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

const app = express();
const port = process.env.PORT || 8080;

app.use(cors());
app.use(express.json());

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per `window` (here, per 15 minutes)
    message: 'Too many requests from this IP, please try again after 15 minutes'
});

// Apply the rate limiting middleware to all requests
app.use(limiter);

app.post('/api/chat', async (req, res) => {
    const { messages } = req.body;

    try {
        const response = await openai.chat.completions.create({
            model: 'gpt-4o-mini',
            store: true,
            messages: messages,
            max_tokens: 200
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