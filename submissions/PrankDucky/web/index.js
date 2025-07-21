let pranksData = [];

function createPrankCard(prank) {
    return `
        <div class="bg-white/10 backdrop-blur-md rounded-lg p-6 hover:bg-white/20 transition-all duration-300 border border-white/20">
            
            <h3 class="text-xl font-bold text-white mb-2">${prank.name}</h3>
            <p class="text-gray-300 mb-4 text-sm">${prank.description}</p>
            
            <details class="mb-4" ontoggle="handleCodeToggle(event, '${prank.filename}')">
                <summary class="cursor-pointer text-blue-400 hover:text-blue-300 text-sm font-medium">View Code</summary>
                <div class="mt-2" id="code-container-${prank.filename}">
                    <div class="text-xs text-gray-400 mb-2">Click to load code...</div>
                </div>
            </details>
            
            <div class="flex gap-2">
                <button onclick="downloadPrank('${prank.filename}')" class="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 text-white px-4 py-2 rounded hover:from-green-600 hover:to-emerald-700 transition-all text-sm">
                    📥 Download
                </button>
                <button onclick="copyCode('${prank.filename}')" class="flex-1 bg-gradient-to-r from-blue-500 to-cyan-600 text-white px-4 py-2 rounded hover:from-blue-600 hover:to-cyan-700 transition-all text-sm">
                    📋 Copy Code
                </button>
            </div>
        </div>
    `;
}

async function loadPranks() {
    try {
        showLoading(true);
        hideError();
        
        const response = await fetch('/pranks');
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Failed to load pranks');
        }
        
        pranksData = data.pranks;
        displayPranks(pranksData);
        
    } catch (error) {
        console.error('Error loading pranks:', error);
    } finally {
        showLoading(false);
    }
}

function displayPranks(pranks) {
    const container = document.getElementById('pranksContainer');
    
    if (pranks.length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <div class="text-6xl mb-4">🦆</div>
                <h3 class="text-xl text-white mb-2">No Pranks Found</h3>
                <p class="text-gray-400">Add some prank files to the pranks/ directory to get started!</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = pranks.map(createPrankCard).join('');
}

// Handle details toggle to auto-load code
function handleCodeToggle(event, filename) {
    const details = event.target;
    const container = document.getElementById(`code-container-${filename}`);
    
    // Only load if opening and hasn't been loaded yet
    if (details.open && container.innerHTML.includes('Click to load code')) {
        loadPrankCode(filename);
    }
}

async function loadPrankCode(filename) {
    try {
        const containerElement = document.getElementById(`code-container-${filename}`);
        containerElement.innerHTML = '<div class="text-xs text-gray-400 mb-2">Loading...</div>';
        
        const response = await fetch(`http://localhost:3000/getPranks/${filename}`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error);
        }
        
        // Only show JavaScript Code Section
        if (data.code) {
            const codeHtml = `
                <div class="mb-4">
                    <div class="flex items-center justify-between mb-2">
                        <h4 class="text-sm font-medium text-yellow-400">🟨 JavaScript Code</h4>
                        <button onclick="copyToClipboard(\`${escapeForTemplate(data.code)}\`)" class="text-xs text-blue-400 hover:text-blue-300">📋 Copy</button>
                    </div>
                    <pre class="p-3 bg-black/50 rounded text-xs overflow-x-auto max-h-40 overflow-y-auto border border-yellow-500/20"><code class="javascript hljs">${escapeHtml(data.code)}</code></pre>
                </div>
            `;
            
            containerElement.innerHTML = codeHtml;
            
            // Apply syntax highlighting with Highlight.js
            if (typeof hljs !== 'undefined') {
                const codeBlock = containerElement.querySelector('code');
                hljs.highlightElement(codeBlock);
            }
        } else {
            containerElement.innerHTML = '<div class="text-xs text-gray-400">No JavaScript code available</div>';
        }
        
    } catch (error) {
        const containerElement = document.getElementById(`code-container-${filename}`);
        containerElement.innerHTML = `<div class="text-xs text-red-400">Error loading code: ${error.message}</div>`;
    }
}

async function downloadPrank(filename) {
    try {
        const response = await fetch(`/api/download/${filename}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Download failed');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        showNotification(`Downloaded ${filename}!`, 'success');
    } catch (error) {
        showNotification(`Download failed: ${error.message}`, 'error');
    }
}

async function copyCode(filename) {
    try {
        const response = await fetch(`http://localhost:3000/getPranks/${filename}`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error);
        }
        
        // Only copy the JavaScript code
        if (data.code) {
            await navigator.clipboard.writeText(data.code);
            showNotification(`Copied ${filename} JavaScript code to clipboard!`, 'success');
        } else {
            showNotification('No JavaScript code available to copy', 'error');
        }
    } catch (error) {
        showNotification(`Copy failed: ${error.message}`, 'error');
    }
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Helper function to escape text for template literals
function escapeForTemplate(text) {
    return text.replace(/`/g, '\\`').replace(/\$/g, '\\$').replace(/\\/g, '\\\\');
}

// Helper function to copy text to clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copied to clipboard!', 'success');
    } catch (error) {
        showNotification('Failed to copy to clipboard', 'error');
    }
}

function showLoading(show) {
    document.getElementById('loadingIndicator').classList.toggle('hidden', !show);
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorSection').classList.remove('hidden');
}

function hideError() {
    document.getElementById('errorSection').classList.add('hidden');
}

// Notification system
function showNotification(message, type = 'info') {
    // Create notification element if it doesn't exist
    let notificationContainer = document.getElementById('notification-container');
    if (!notificationContainer) {
        notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        notificationContainer.className = 'fixed top-4 right-4 z-50 space-y-2';
        document.body.appendChild(notificationContainer);
    }
    
    const notification = document.createElement('div');
    const bgColor = type === 'success' ? 'bg-green-600' : type === 'error' ? 'bg-red-600' : 'bg-blue-600';
    
    notification.className = `${bgColor} text-white px-4 py-2 rounded-lg shadow-lg transform transition-all duration-300 translate-x-full opacity-0`;
    notification.textContent = message;
    
    notificationContainer.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full', 'opacity-0');
    }, 10);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('translate-x-full', 'opacity-0');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

document.addEventListener('DOMContentLoaded', () => {
    loadPranks();
});

