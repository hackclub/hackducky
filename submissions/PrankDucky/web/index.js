let pranksData = [];

function createPrankCard(prank) {
    return `
        <div class="bg-white/10 backdrop-blur-md rounded-lg p-6 hover:bg-white/20 transition-all duration-300 border border-white/20">
            <div class="flex items-start justify-between mb-4">
                <div class="text-4xl">${prank.icon}</div>
            </div>
            
            <h3 class="text-xl font-bold text-white mb-2">${prank.name}</h3>
            <p class="text-gray-300 mb-4 text-sm">${prank.description}</p>
            
            <div class="grid grid-cols-2 gap-2 mb-4 text-xs text-gray-400">
                <div>Type: ${prank.type}</div>
                <div>File: ${prank.filename}</div>
            </div>
            
            <details class="mb-4">
                <summary class="cursor-pointer text-blue-400 hover:text-blue-300 text-sm font-medium">View Code</summary>
                <div class="mt-2">
                    <pre class="p-3 bg-black/30 rounded text-xs text-green-400 overflow-x-auto max-h-40 overflow-y-auto" id="code-${prank.filename}">Loading...</pre>
                    <button onclick="loadPrankCode('${prank.filename}')" class="mt-2 text-xs text-blue-400 hover:text-blue-300">🔄 Load Code</button>
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

async function loadPrankCode(filename) {
    try {
        const codeElement = document.getElementById(`code-${filename}`);
        codeElement.textContent = 'Loading...';
        
        const response = await fetch(`/api/pranks/${filename}`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error);
        }
        
        codeElement.textContent = data.code;
    } catch (error) {
        const codeElement = document.getElementById(`code-${filename}`);
        codeElement.textContent = `Error loading code: ${error.message}`;
        codeElement.className = codeElement.className.replace('text-green-400', 'text-red-400');
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
        const response = await fetch(`/api/pranks/${filename}`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error);
        }
        
        await navigator.clipboard.writeText(data.code);
        showNotification(`Copied ${filename} code to clipboard!`, 'success');
    } catch (error) {
        showNotification(`Copy failed: ${error.message}`, 'error');
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

document.addEventListener('DOMContentLoaded', () => {
    loadPranks();
});
