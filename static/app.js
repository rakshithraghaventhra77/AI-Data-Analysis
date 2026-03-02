let statusChart, deliveryChart, trendChart;
let allData = {};

async function getJSON(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Request failed: ${url}`);
  return response.json();
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function renderStatusTable(obj) {
  const tbody = document.getElementById("status-table");
  if (!tbody) return;
  tbody.innerHTML = "";
  const total = Object.values(obj).reduce((a, b) => a + b, 0);
  Object.entries(obj).forEach(([status, count]) => {
    const pct = ((count / total) * 100).toFixed(1);
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${status}</td><td>${count}</td><td>${pct}%</td>`;
    tbody.appendChild(tr);
  });
}

function renderDeliveryList(obj) {
  const el = document.getElementById("delivery-list");
  if (!el) return;
  el.innerHTML = "";
  Object.entries(obj).forEach(([key, value]) => {
    const li = document.createElement("li");
    const label = key.replace(/_/g, " ").toUpperCase();
    li.innerHTML = `<span class="label">${label}</span><span class="value">${value.toLocaleString()}</span>`;
    el.appendChild(li);
  });
}

function renderQualityReport(report) {
  const el = document.getElementById("quality-report");
  if (!el || !report) return;
  el.innerHTML = "";
  
  const card = document.createElement("div");
  card.className = "quality-item";
  card.innerHTML = `
    <p><strong>Total Rows:</strong> ${report.total_rows?.toLocaleString() || "N/A"}</p>
    <p><strong>Total Columns:</strong> ${report.total_columns || "N/A"}</p>
  `;
  el.appendChild(card);
}

function renderPredictions(predictions) {
  const el = document.getElementById("predictions");
  if (!el || !predictions || !predictions.forecast) return;
  el.innerHTML = "";
  
  predictions.forecast.slice(0, 6).forEach(forecast => {
    const div = document.createElement("div");
    div.className = "prediction-item";
    div.innerHTML = `
      <div><strong>${forecast.year}-${String(forecast.month).padStart(2, '0')}</strong></div>
      <div>${forecast.predicted_orders.toLocaleString()} orders</div>
      <div style="font-size: 0.8rem; color: #6b7280;">Confidence: ${(forecast.confidence * 100).toFixed(0)}%</div>
    `;
    el.appendChild(div);
  });
}

function renderAnomalies(anomalies) {
  const el = document.getElementById("anomalies");
  if (!el || !anomalies || anomalies.error) return;
  el.innerHTML = "";
  
  const items = [
    { label: "Anomalies Found", value: anomalies.anomalies_detected },
    { label: "Anomaly Rate", value: `${anomalies.anomaly_percentage}%` },
    { label: "Fast Deliveries", value: anomalies.details.fast_deliveries },
    { label: "Slow Deliveries", value: anomalies.details.slow_deliveries }
  ];
  
  items.forEach(item => {
    const div = document.createElement("div");
    div.className = "anomaly-item";
    div.innerHTML = `<span>${item.label}</span><strong>${item.value}</strong>`;
    el.appendChild(div);
  });
}

function renderClustering(clustering) {
  const el = document.getElementById("clustering");
  if (!el || !clustering || clustering.error) return;
  el.innerHTML = "";
  
  let html = `<p><strong>Clusters Found:</strong> ${clustering.clusters}</p>`;
  html += `<p><strong>Model Inertia:</strong> ${clustering.inertia?.toFixed(2) || 'N/A'}</p>`;
  html += `<table class="cluster-table"><thead><tr><th>Cluster</th><th>Size</th><th>Avg Days</th><th>Std Dev</th></tr></thead><tbody>`;
  
  if (clustering.cluster_details) {
    clustering.cluster_details.forEach(cluster => {
      html += `
        <tr>
          <td>#${cluster.cluster}</td>
          <td>${cluster.size}</td>
          <td>${cluster.avg_delivery_days}</td>
          <td>${cluster.std_delivery_days}</td>
        </tr>
      `;
    });
  }
  
  html += '</tbody></table>';
  el.innerHTML = html;
}

function initStatusChart(status) {
  const ctx = document.getElementById("statusChart");
  if (!ctx || !status) return;
  
  if (statusChart) statusChart.destroy();
  statusChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: Object.keys(status),
      datasets: [{
        data: Object.values(status),
        backgroundColor: ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8"],
        borderWidth: 2,
        borderColor: "#fff"
      }]
    },
    options: { responsive: true, plugins: { legend: { position: "bottom" } } }
  });
}

function initDeliveryChart(delivery) {
  const ctx = document.getElementById("deliveryChart");
  if (!ctx || !delivery) return;
  
  if (deliveryChart) deliveryChart.destroy();
  const total = delivery.on_time_deliveries + delivery.late_deliveries;
  deliveryChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["On-Time", "Late"],
      datasets: [{
        label: "Deliveries",
        data: [delivery.on_time_deliveries, delivery.late_deliveries],
        backgroundColor: ["#4ECDC4", "#FF6B6B"],
        borderRadius: 8,
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      indexAxis: "y",
      plugins: { legend: { display: true } }
    }
  });
}

function initTrendChart(trends) {
  const ctx = document.getElementById("trendChart");
  if (!ctx || !trends || !Array.isArray(trends)) return;
  
  if (trendChart) trendChart.destroy();
  trends.sort((a, b) => {
    const aDate = new Date(a.purchase_year, a.purchase_month - 1);
    const bDate = new Date(b.purchase_year, b.purchase_month - 1);
    return aDate - bDate;
  });

  const labels = trends.map(t => `${t.purchase_year}-${String(t.purchase_month).padStart(2, "0")}`);
  const data = trends.map(t => t.order_count);

  trendChart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Monthly Orders",
        data,
        borderColor: "#1f4a8a",
        backgroundColor: "rgba(31, 74, 138, 0.1)",
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: "#1f4a8a",
        pointBorderColor: "#fff",
        pointBorderWidth: 2,
        pointRadius: 5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: { legend: { display: true } }
    }
  });
}

function exportCSV() {
  if (!allData.status) {
    alert("Data not loaded yet");
    return;
  }
  
  let csv = "Order Status Report\n";
  csv += "Status,Count\n";
  Object.entries(allData.status).forEach(([status, count]) => {
    csv += `${status},${count}\n`;
  });
  
  csv += "\n\nMonthly Trend\n";
  csv += "Year,Month,Orders\n";
  if (Array.isArray(allData.trend)) {
    allData.trend.forEach(row => {
      csv += `${row.purchase_year},${row.purchase_month},${row.order_count}\n`;
    });
  }
  
  const blob = new Blob([csv], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `order-analytics-${new Date().toISOString().split("T")[0]}.csv`;
  a.click();
}

function downloadPDF() {
  setText("status", "Generating PDF...");
  window.location.href = "/report";
  setTimeout(() => setText("status", "Ready"), 2000);
}

async function refreshData() {
  setText("status", "Loading...");
  try {
    const [metrics, status, trend, insights, delivery, quality, predictions, anomalies, clustering] = await Promise.all([
      getJSON("/metrics"),
      getJSON("/order-status"),
      getJSON("/monthly-trend"),
      getJSON("/insights"),
      getJSON("/delivery-breakdown"),
      getJSON("/data-quality"),
      getJSON("/predict"),
      getJSON("/anomalies"),
      getJSON("/clustering")
    ]);

    allData = { status, trend, metrics };

    setText("total-orders", metrics.total_orders?.toLocaleString() || "-");
    setText("avg-delivery", metrics.average_delivery_days || "-");
    setText("late-pct", (metrics.late_delivery_percentage || 0).toFixed(2) + "%");
    setText("on-time-count", (delivery.on_time_deliveries || 0).toLocaleString());

    renderStatusTable(status);
    renderDeliveryList(delivery);
    renderQualityReport(quality);
    renderPredictions(predictions);
    renderAnomalies(anomalies);
    renderClustering(clustering);
    
    initStatusChart(status);
    initDeliveryChart(delivery);
    initTrendChart(trend);

    setText("insight-text", insights.insight || "No insights available");
    setText("status", "Ready");
  } catch (error) {
    setText("insight-text", `Error: ${error.message}`);
    setText("status", "Error");
  }
}

document.addEventListener("DOMContentLoaded", refreshData);

// ===========================
// Chatbot Functions
// ===========================

async function sendChatMessage() {
  const input = document.getElementById("chatInput");
  const message = input.value.trim();
  
  if (!message) return;
  
  const chatMessages = document.getElementById("chatMessages");
  
  // Add user message to chat
  addChatMessage(message, "user");
  input.value = "";
  input.focus();
  
  try {
    // Show typing indicator
    const typingMsg = addChatMessage("🤖 Thinking...", "bot");
    
    const response = await fetch("/chatbot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: message })
    });
    
    const result = await response.json();
    
    // Remove typing indicator
    typingMsg.remove();
    
    if (!response.ok) {
      addChatMessage(`❌ Error: ${result.error}`, "bot");
      return;
    }
    
    // Add bot response with formatted answer
    const answer = formatBotAnswer(result.answer);
    addChatMessage(answer, "bot");
    
  } catch (error) {
    addChatMessage(`❌ Connection error: ${error.message}`, "bot");
  }
  
  // Scroll to latest message
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addChatMessage(text, sender) {
  const chatMessages = document.getElementById("chatMessages");
  const messageDiv = document.createElement("div");
  messageDiv.className = `chat-message ${sender}`;
  
  // Check if the text contains code/tables
  if (text.includes("\n") && (text.includes("-") || text.includes("|") || text.includes("*"))) {
    messageDiv.innerHTML = `<pre>${escapeHtml(text)}</pre>`;
  } else if (text.includes("**")) {
    // Handle markdown-style bold
    const formattedText = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    messageDiv.innerHTML = `<p>${formattedText}</p>`;
  } else {
    messageDiv.innerHTML = `<p>${escapeHtml(text)}</p>`;
  }
  
  chatMessages.appendChild(messageDiv);
  return messageDiv;
}

function formatBotAnswer(answer) {
  // Format the answer for better display
  return answer;
}

function escapeHtml(text) {
  const map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}

// Allow Enter key to send message
document.addEventListener("DOMContentLoaded", function() {
  const chatInput = document.getElementById("chatInput");
  if (chatInput) {
    chatInput.addEventListener("keypress", function(e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendChatMessage();
      }
    });
  }
});

