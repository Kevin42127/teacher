let scrapedData = [];

const elements = {
    urlInput: document.getElementById('urlInput'),
    scrapeBtn: document.getElementById('scrapeBtn'),
    exportBtn: document.getElementById('exportBtn'),
    notification: document.getElementById('notification'),
    loadingState: document.getElementById('loadingState'),
    emptyState: document.getElementById('emptyState'),
    resultsTable: document.getElementById('resultsTable'),
    tableBody: document.getElementById('tableBody'),
    totalCount: document.getElementById('totalCount')
};

function showNotification(message, type = 'success') {
    elements.notification.textContent = message;
    elements.notification.className = `notification ${type} show`;
    
    setTimeout(() => {
        elements.notification.classList.remove('show');
    }, 5000);
}

function toggleLoading(isLoading) {
    if (isLoading) {
        elements.loadingState.style.display = 'flex';
        elements.emptyState.style.display = 'none';
        elements.resultsTable.style.display = 'none';
        elements.scrapeBtn.disabled = true;
        elements.scrapeBtn.innerHTML = '<span class="material-icons">hourglass_empty</span>採集中...';
    } else {
        elements.loadingState.style.display = 'none';
        elements.scrapeBtn.disabled = false;
        elements.scrapeBtn.innerHTML = '<span class="material-icons">search</span>開始採集';
    }
}

function renderTable(data) {
    if (!data || data.length === 0) {
        elements.emptyState.style.display = 'flex';
        elements.resultsTable.style.display = 'none';
        elements.exportBtn.style.display = 'none';
        return;
    }
    
    elements.emptyState.style.display = 'none';
    elements.resultsTable.style.display = 'block';
    elements.exportBtn.style.display = 'inline-flex';
    
    elements.tableBody.innerHTML = data.map((prof, index) => `
        <tr>
            <td>${index + 1}</td>
            <td>${prof.name || '-'}</td>
            <td>${prof.email || '-'}</td>
            <td>${prof.department || '-'}</td>
        </tr>
    `).join('');
    
    elements.totalCount.textContent = data.length;
}

async function handleScrape() {
    const url = elements.urlInput.value.trim();
    
    if (!url) {
        showNotification('請輸入網址', 'error');
        return;
    }
    
    try {
        new URL(url);
    } catch (e) {
        showNotification('請輸入有效的網址格式', 'error');
        return;
    }
    
    toggleLoading(true);
    
    try {
        const response = await fetch('/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            scrapedData = result.data;
            renderTable(scrapedData);
            showNotification(`成功採集 ${result.count} 筆教授資料`, 'success');
        } else {
            scrapedData = [];
            renderTable([]);
            showNotification(result.error || '採集失敗', 'error');
        }
    } catch (error) {
        scrapedData = [];
        renderTable([]);
        showNotification('網路連接失敗，請檢查連線', 'error');
        console.error('Scrape error:', error);
    } finally {
        toggleLoading(false);
    }
}

async function handleExport() {
    if (!scrapedData || scrapedData.length === 0) {
        showNotification('沒有資料可匯出', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                data: scrapedData,
                format: 'csv'
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
            a.download = `professors_${timestamp}.csv`;
            
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            showNotification('成功匯出 CSV 檔案', 'success');
        } else {
            const result = await response.json();
            showNotification(result.error || '匯出失敗', 'error');
        }
    } catch (error) {
        showNotification('匯出失敗，請稍後再試', 'error');
        console.error('Export error:', error);
    }
}

elements.scrapeBtn.addEventListener('click', handleScrape);

document.querySelectorAll('.btn-secondary').forEach(btn => {
    if (btn.id === 'exportBtn' || btn.textContent.includes('匯出')) {
        btn.addEventListener('click', handleExport);
    }
});

elements.urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleScrape();
    }
});

