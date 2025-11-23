import { createWriteStream, mkdirSync } from 'fs';
import { resolve } from 'path';
import { randomBytes } from 'crypto';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Handle multipart form data (file upload)
    if (req.headers['content-type']?.includes('multipart/form-data')) {
      // This is a simplified approach - in production, use multer or similar
      const boundary = req.headers['content-type'].split('boundary=')[1];
      // Parse multipart data
      // For now, we'll use a simpler approach with base64
    }

    // Handle base64 file data
    const { file, filename } = req.body;
    
    if (!file) {
      return res.status(400).json({ error: 'No file provided' });
    }

    // Generate unique filename
    const fileExt = filename?.split('.').pop() || 'jpg';
    const uniqueName = `${randomBytes(8).toString('hex')}.${fileExt}`;
    const uploadPath = resolve(process.cwd(), 'uploads', uniqueName);

    // Ensure uploads directory exists
    mkdirSync(resolve(process.cwd(), 'uploads'), { recursive: true });

    // Convert base64 to buffer and write
    const buffer = Buffer.from(file.split(',')[1] || file, 'base64');
    
    // Write file
    const writeStream = createWriteStream(uploadPath);
    writeStream.write(buffer);
    writeStream.end();

    // Wait for stream to finish
    await new Promise((resolve, reject) => {
      writeStream.on('finish', resolve);
      writeStream.on('error', reject);
    });

    // Return local URL
    const fileUrl = `${process.env.VERCEL_URL ? 'https://' + process.env.VERCEL_URL : 'http://localhost:3000'}/uploads/${uniqueName}`;
    
    res.status(200).json({ 
      success: true, 
      url: fileUrl,
      filename: uniqueName 
    });
  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ error: 'Upload failed: ' + error.message });
  }
}
