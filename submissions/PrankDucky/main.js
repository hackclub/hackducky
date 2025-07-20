const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;
const PRANKS_DIR = path.join(__dirname, 'pranks');

app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));


app.get('/pranks', async (req, res) => {
    try {
        const files = await fs.readdir(PRANKS_DIR);
        const pranks = [];

        for (const file of files) {
            if (file.startsWith('.')) continue;
            
            const filePath = path.join(PRANKS_DIR, file);
            const stats = await fs.stat(filePath);
            console.log(stats)
            
            if (stats.isFile()) {
                try {
                    const code = await fs.readFile(filePath, 'utf8');
                    
                    const lines = code.split('\n');
                    const firstComment = lines.find(line => line.trim().startsWith('//'));
                    
                    let prankName, prankDescription;
                    if (firstComment) {
                        const commentText = firstComment.replace('//', '').trim();
                        const dashIndex = commentText.indexOf(' - ');
                        if (dashIndex > -1) {
                            prankName = commentText.substring(0, dashIndex).trim();
                            prankDescription = commentText.substring(dashIndex + 3).trim();
                        } else {
                            prankName = commentText;
                            prankDescription = '';
                        }
                    } else {
                        prankName = path.parse(file).name
                            .replace(/[-_]/g, ' ')
                            .split(' ')
                            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                            .join(' ');
                        prankDescription = '';
                    }

                    pranks.push({
                        name: prankName,
                        description: prankDescription,
                        filename: file,
                        size: stats.size,
                    });
                } catch (readError) {
                    console.error(`Error reading file ${file}:`, readError);
                }
            }
        }

        res.json({
            success: true,
            count: pranks.length,
            pranks: pranks
        });
    } catch (error) {
        console.error('Error reading pranks directory:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to read pranks directory',
            message: error.message
        });
    }
});

app.get('/getPranks/:filename', async (req, res) => {
    try {
        const filename = req.params.filename;
        const filePath = path.join(PRANKS_DIR, filename);
        
        // Security check - prevent directory traversal
        if (!filePath.startsWith(PRANKS_DIR)) {
            return res.status(400).json({
                success: false,
                error: 'Invalid filename'
            });
        }

        const code = await fs.readFile(filePath, 'utf8');
        const stats = await fs.stat(filePath);

        res.json({
            success: true,
            filename: filename,
            code: code,
            size: stats.size,
            modified: stats.mtime,
            type: getPrankType(filename)
        });
    } catch (error) {
        if (error.code === 'ENOENT') {
            res.status(404).json({
                success: false,
                error: 'Prank not found'
            });
        } else {
            console.error('Error reading prank file:', error);
            res.status(500).json({
                success: false,
                error: 'Failed to read prank file',
                message: error.message
            });
        }
    }
});

app.get('/api/download/:filename', async (req, res) => {
});


app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'web', 'index.html'));
});


app.use((error, req, res, next) => {
    console.error('Unhandled error:', error);
    res.status(500).json({
        success: false,
        error: 'Internal server error'
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

module.exports = app;


