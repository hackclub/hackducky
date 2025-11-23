const express = require('express');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse JSON bodies
app.use(express.json({ limit: '50mb' }));

// Serve static files (html, css, js, images)
app.use(express.static(path.join(__dirname)));

// Airtable Configuration
const AIRTABLE_API_KEY = process.env.AIRTABLE_API_KEY;
const AIRTABLE_BASE_ID = process.env.AIRTABLE_BASE_ID;
const TABLE_NAME = 'Scripts';

// API Route: Handle Scripts
app.all('/api/script', async (req, res) => {
    if (!AIRTABLE_API_KEY || !AIRTABLE_BASE_ID) {
        console.error('Missing Airtable credentials in .env file');
        return res.status(500).json({ error: 'Server configuration error' });
    }

    // Handle POST: Create a new script
    if (req.method === 'POST') {
        try {
            const { fields } = req.body;
            
            const response = await fetch(`https://api.airtable.com/v0/${AIRTABLE_BASE_ID}/${TABLE_NAME}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${AIRTABLE_API_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ fields })
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error?.message || 'Failed to save to Airtable');
            }

            return res.json(data);

        } catch (error) {
            console.error('Airtable Error:', error);
            return res.status(500).json({ error: error.message });
        }
    } 
    
    // Handle GET: Fetch a script by ID
    else if (req.method === 'GET') {
        const { id } = req.query;

        if (!id) {
            return res.status(400).json({ error: 'Missing script ID' });
        }

        try {
            const response = await fetch(`https://api.airtable.com/v0/${AIRTABLE_BASE_ID}/${TABLE_NAME}/${id}`, {
                headers: {
                    'Authorization': `Bearer ${AIRTABLE_API_KEY}`
                }
            });

            const data = await response.json();

            if (!response.ok) {
                if (response.status === 404) {
                    return res.status(404).json({ error: 'Script not found' });
                }
                throw new Error(data.error?.message || 'Failed to fetch from Airtable');
            }

            return res.json(data);

        } catch (error) {
            console.error('Airtable Error:', error);
            return res.status(500).json({ error: error.message });
        }
    }

    return res.status(405).json({ error: 'Method not allowed' });
});

// API Route: Handle Image Upload
app.post('/api/upload', async (req, res) => {
    try {
        const { file, filename } = req.body;

        if (!file) {
            return res.status(400).json({ error: 'No file provided' });
        }

        // Upload to Hackclub CDN directly with the base64 data URL
        try {
            console.log('Uploading to CDN with data URL...');
            const cdnResponse = await fetch('https://cdn.hackclub.com/api/v3/new', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer beans',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify([file])
            });

            if (!cdnResponse.ok) {
                const errorText = await cdnResponse.text();
                console.error('CDN response status:', cdnResponse.status, 'Body:', errorText);
                throw new Error(`CDN upload failed: ${cdnResponse.status}`);
            }

            const cdnResult = await cdnResponse.json();
            const cdnUrl = cdnResult.files[0].deployedUrl;

            res.status(200).json({
                success: true,
                url: cdnUrl,
                filename: cdnResult.files[0].file
            });
        } catch (cdnError) {
            console.error('CDN error:', cdnError);
            res.status(500).json({ error: 'CDN upload failed: ' + cdnError.message });
        }
    } catch (error) {
        console.error('Upload error:', error);
        res.status(500).json({ error: 'Upload failed: ' + error.message });
    }
});

// Fallback for any other request (optional, handled by static middleware usually)
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
