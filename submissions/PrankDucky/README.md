# 💻 PrankDucky 
**Author**: Ajay Anto

Generates "harmless" prank scripts for HackDucky (USB Rubber Ducky).

## Features

- ⚙️ **Configurable Options**: Set execution delays and startup persistence
- 🔄 **Auto-Generation**: Automatically converts JavaScript pranks to PowerShell and Ducky Scripts

## Available Pranks

- **👻 Creepy**: Says spooky messages every 83.2 seconds
- **⌨️ Broken Keyboard**: Simulates typing and random characters and beeps
- **💥 Error Bomb**: When you really want to annoy people
- **💬 Infinite Messages**: You can never close them haha
- **🎲 Random Keys**: Types random characters

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AjayAntoIsDev/hackducky
   cd hackducky/submissions/PrankDucky
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the server**:
   ```bash
   npm start
   ```

4. **Open your browser** and navigate to `http://localhost:3000`

## Usage

### Web Interface

1. Open the web interface at `http://localhost:3000`
3. Configure options:
   - **Execution Delay**: Set a delay before the prank starts (in seconds)
   - **Add to Startup**: Make the prank persistent across reboots
4. Click "Download" on any prank to get the Ducky Script

## Adding New Pranks

To add a new prank:

1. Create a new `.js` file in the `pranks/` directory
2. Add a comment at the top with format: `// Name - Description`
3. Write your prank using Windows Script Host APIs
4. Restart the server to see your new prank in the web interface

Example prank structure:
```javascript
// My Prank - Does something amusing
var shell = WScript.CreateObject("WScript.Shell");
// Your prank code here...
```

## License

MIT License - Feel free to use, modify, and distribute as needed.

---

**Happy Pranking! 🦆** (Legally, of course!)