document.addEventListener('DOMContentLoaded', () => {
    // --- State & DOM Elements ---
    const state = {
        currentView: 'dashboard',
        isUploading: false,
        isQuerying: false
    };

    const elements = {
        tabs: document.querySelectorAll('.nav-item'),
        views: document.querySelectorAll('.view'),
        stats: {
            vectors: document.getElementById('stat-vectors'),
            model: document.getElementById('stat-model'),
            docs: document.getElementById('stat-docs')
        },
        upload: {
            zone: document.getElementById('drop-zone'),
            input: document.getElementById('file-input'),
            progress: document.getElementById('upload-progress'),
            result: document.getElementById('upload-result'),
            verify: document.getElementById('verify-integrity')
        },
        chat: {
            history: document.getElementById('chat-history'),
            input: document.getElementById('chat-input'),
            sendBtn: document.getElementById('send-btn'),
            security: document.getElementById('chat-security'),
            chunks: document.getElementById('chat-chunks')
        },
        buttons: {
            refresh: document.getElementById('refresh-stats'),
            clear: document.getElementById('clear-db')
        }
    };

    // --- Navigation ---
    elements.tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.tab;
            switchView(target);
        });
    });

    function switchView(viewId) {
        state.currentView = viewId;

        // Update Tabs
        elements.tabs.forEach(t => t.classList.remove('active'));
        document.querySelector(`[data-tab="${viewId}"]`).classList.add('active');

        // Update Views
        elements.views.forEach(v => v.classList.remove('active'));
        document.getElementById(`view-${viewId}`).classList.add('active');

        // Update Title
        document.getElementById('page-title').innerText = viewId.charAt(0).toUpperCase() + viewId.slice(1);
    }

    // --- API Interactions ---

    // Stats
    async function fetchStats() {
        try {
            const res = await fetch('/stats');
            if (res.ok) {
                const data = await res.json();
                updateStatsUI(data);
            }
        } catch (e) {
            console.error('Stats fetch failed', e);
        }
    }

    function updateStatsUI(data) {
        elements.stats.vectors.innerText = data.vector_store.total_documents || 0;
        elements.stats.model.innerText = data.llm_model || 'Unknown';
        elements.stats.docs.innerText = data.security.cached_analyses || 0;
    }

    // Upload
    elements.upload.zone.addEventListener('click', () => elements.upload.input.click());

    elements.upload.zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.upload.zone.classList.add('dragover');
    });

    elements.upload.zone.addEventListener('dragleave', () => {
        elements.upload.zone.classList.remove('dragover');
    });

    elements.upload.zone.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.upload.zone.classList.remove('dragover');
        if (e.dataTransfer.files.length) handleUpload(e.dataTransfer.files[0]);
    });

    elements.upload.input.addEventListener('change', (e) => {
        if (e.target.files.length) handleUpload(e.target.files[0]);
    });

    async function handleUpload(file) {
        if (file.type !== 'application/pdf') return alert('Only PDF files are supported');

        elements.upload.progress.classList.remove('hidden');
        elements.upload.result.classList.add('hidden');

        const formData = new FormData();
        formData.append('file', file);
        formData.append('verify_integrity', elements.upload.verify.checked);

        try {
            const res = await fetch('/upload_pdf', {
                method: 'POST',
                body: formData
            });

            const data = await res.json();

            if (res.ok) {
                showUploadResult(data, true);
                fetchStats(); // Refresh stats
            } else {
                showUploadResult(data, false);
            }
        } catch (e) {
            showUploadResult({ detail: e.message }, false);
        } finally {
            elements.upload.progress.classList.add('hidden');
        }
    }

    function showUploadResult(data, success) {
        const resultDiv = elements.upload.result;
        resultDiv.classList.remove('hidden');
        resultDiv.innerHTML = success
            ? `<div class="success-box">
                <i class="fa-solid fa-circle-check"></i>
                <div>
                    <h4>Analysis Complete</h4>
                    <p>${data.message}</p>
                    <small>Chunks: ${data.total_chunks} | Verified: ${data.integrity_verified}</small>
                </div>
               </div>`
            : `<div class="error-box">
                <i class="fa-solid fa-triangle-exclamation"></i>
                <p>Error: ${data.detail || 'Upload failed'}</p>
               </div>`;
    }

    // Chat
    elements.chat.sendBtn.addEventListener('click', sendMessage);
    elements.chat.input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    async function sendMessage() {
        const text = elements.chat.input.value.trim();
        if (!text || state.isQuerying) return;

        addMessage('user', text);
        elements.chat.input.value = '';
        state.isQuerying = true;

        // Add loading message
        const loadingId = addMessage('system', '<i class="fa-solid fa-spinner fa-spin"></i> Researching...');

        try {
            const res = await fetch('/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question: text,
                    n_chunks: parseInt(elements.chat.chunks.value),
                    include_security: elements.chat.security.checked
                })
            });

            const data = await res.json();

            // Remove loading
            document.getElementById(loadingId).remove();

            if (res.ok) {
                let content = `<p>${data.answer}</p>`;

                if (data.sources && data.sources.length) {
                    content += `<div class="sources"><strong>Sources:</strong><ul>`;
                    data.sources.forEach((s, i) => {
                        content += `<li>[${i + 1}] ${s.source} (Chunk ${s.chunk_index}) - ${Math.round(s.relevance_score * 100)}% match</li>`;
                    });
                    content += `</ul></div>`;
                }

                if (data.security_warnings && data.security_warnings.length) {
                    content += `<div class="warnings"><strong>⚠️ Security Warnings:</strong><ul>`;
                    data.security_warnings.forEach(w => {
                        content += `<li>${w.severity}: ${w.message}</li>`;
                    });
                    content += `</ul></div>`;
                }

                addMessage('system', content, true);
            } else {
                addMessage('system', `❌ Error: ${data.detail || 'Query failed'}`);
            }

        } catch (e) {
            document.getElementById(loadingId).remove();
            addMessage('system', `❌ Connection Error: ${e.message}`);
        } finally {
            state.isQuerying = false;
        }
    }

    function addMessage(type, html, isHtml = false) {
        const id = 'msg-' + Date.now();
        const div = document.createElement('div');
        div.className = `message ${type}`;
        div.id = id;

        div.innerHTML = `
            <div class="avatar">
                <i class="fa-solid ${type === 'user' ? 'fa-user' : 'fa-robot'}"></i>
            </div>
            <div class="content">
                ${isHtml ? html : `<p>${html}</p>`}
            </div>
        `;

        elements.chat.history.appendChild(div);
        elements.chat.history.scrollTop = elements.chat.history.scrollHeight;
        return id;
    }

    // System Buttons
    elements.buttons.refresh.addEventListener('click', () => {
        fetchStats();
        // Add rotation animation
        elements.buttons.refresh.querySelector('i').classList.add('fa-spin');
        setTimeout(() => elements.buttons.refresh.querySelector('i').classList.remove('fa-spin'), 1000);
    });

    elements.buttons.clear.addEventListener('click', async () => {
        if (!confirm('Are you sure you want to clear the database? This cannot be undone.')) return;

        try {
            await fetch('/clear', { method: 'DELETE' });
            alert('System cleared.');
            fetchStats();
            elements.chat.history.innerHTML = '';
        } catch (e) {
            alert('Failed to clear system');
        }
    });

    // Initial Load
    fetchStats();
});
