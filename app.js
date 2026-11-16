/**
 * Marketing Attribution & ROI Intelligence - Dashboard Controller
 * Connects embedded data to Chart.js and drives multi-page navigation.
 */

document.addEventListener("DOMContentLoaded", () => {
    const data = window.DASHBOARD_DATA;
    if (!data) {
        console.error("Dashboard data not loaded!");
        return;
    }

    // Chart instances store
    const charts = {};

    // 1. Navigation Controller
    const navItems = document.querySelectorAll(".nav-item");
    const pages = document.querySelectorAll(".dashboard-page");
    const pageTitle = document.getElementById("page-title");
    const pageDesc = document.getElementById("page-desc");

    const pageMeta = {
        "page-overview": {
            title: "Executive Overview",
            desc: "High-level digital marketing spend, revenue generation, and portfolio ROI metrics"
        },
        "page-channels": {
            title: "Channel Performance",
            desc: "Comparative channel efficiency, ROI multiples, and funnel conversion velocities"
        },
        "page-campaigns": {
            title: "Campaign Analysis",
            desc: "Granular audit of top star performers and underperforming budget bleeders"
        },
        "page-attribution": {
            title: "Marketing Attribution Models",
            desc: "Customer journey multi-touch attribution: First-Touch vs. Last-Touch vs. Position-Based"
        }
    };

    navItems.forEach(item => {
        item.addEventListener("click", () => {
            navItems.forEach(i => i.classList.remove("active"));
            pages.forEach(p => p.classList.remove("active"));

            item.classList.add("active");
            const targetPage = item.getAttribute("data-page");
            document.getElementById(targetPage).classList.add("active");

            pageTitle.textContent = pageMeta[targetPage].title;
            pageDesc.textContent = pageMeta[targetPage].desc;

            // Trigger chart resize / update on page switch
            window.dispatchEvent(new Event('resize'));
        });
    });

    // 2. Formatters
    const fmtCurrency = num => "$" + Number(num).toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 });
    const fmtDec = num => "$" + Number(num).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const fmtInt = num => Number(num).toLocaleString();
    const fmtPct = num => Number(num).toFixed(1) + "%";
    const fmtMult = num => Number(num).toFixed(2) + "x";

    // 3. Populate Executive Table
    const tableOverviewBody = document.querySelector("#table-overview tbody");
    if (tableOverviewBody) {
        tableOverviewBody.innerHTML = "";
        data.channels.forEach(ch => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>${ch["Marketing Channel"]}</strong></td>
                <td>${fmtCurrency(ch["Marketing Spend"])}</td>
                <td>${fmtCurrency(ch["Revenue"])}</td>
                <td><strong class="text-green">${fmtCurrency(ch["Net Profit"])}</strong></td>
                <td><strong>${fmtMult(ch["roas"])}</strong></td>
                <td>${fmtPct(ch["roi_pct"])}</td>
                <td>${fmtInt(ch["Conversions"])}</td>
                <td>${fmtDec(ch["cac"])}</td>
                <td>${fmtPct(ch["conv_rate"])}</td>
            `;
            tableOverviewBody.appendChild(tr);
        });
    }

    // 4. Populate Top & Bottom Campaigns Tables
    const tableTopBody = document.querySelector("#table-top-campaigns tbody");
    if (tableTopBody) {
        tableTopBody.innerHTML = "";
        data.top_campaigns.forEach(c => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>${c["Campaign Name"].split("_").slice(-2).join("_")}</strong></td>
                <td>${c["Marketing Channel"]}</td>
                <td>${fmtCurrency(c["Marketing Spend"])}</td>
                <td>${fmtCurrency(c["Revenue"])}</td>
                <td><strong class="text-green">${fmtCurrency(c["Net Profit"])}</strong></td>
                <td><strong>${fmtMult(c["roas"])}</strong></td>
            `;
            tableTopBody.appendChild(tr);
        });
    }

    const tableBottomBody = document.querySelector("#table-bottom-campaigns tbody");
    if (tableBottomBody) {
        tableBottomBody.innerHTML = "";
        data.bottom_campaigns.forEach(c => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>${c["Campaign Name"].split("_").slice(-2).join("_")}</strong></td>
                <td>${c["Marketing Channel"]}</td>
                <td>${fmtCurrency(c["Marketing Spend"])}</td>
                <td>${fmtCurrency(c["Revenue"])}</td>
                <td>${fmtCurrency(c["Net Profit"])}</td>
                <td><strong class="text-red">${fmtMult(c["roas"])}</strong></td>
            `;
            tableBottomBody.appendChild(tr);
        });
    }

    // 5. Populate Attribution Table
    const tableAttrBody = document.querySelector("#table-attribution tbody");
    if (tableAttrBody) {
        tableAttrBody.innerHTML = "";
        data.attribution.forEach(a => {
            const shift = a["Last_Touch_Revenue"] - a["First_Touch_Revenue"];
            const shiftText = shift > 0 ? "🟢 Bottom-Funnel Closer" : "🔵 Top-Funnel Introducer";
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>${a["Marketing Channel"]}</strong></td>
                <td>${fmtCurrency(a["First_Touch_Revenue"])}</td>
                <td>${fmtPct(a["First_Touch_Revenue_Share_Pct"])}</td>
                <td>${fmtCurrency(a["Last_Touch_Revenue"])}</td>
                <td>${fmtPct(a["Last_Touch_Revenue_Share_Pct"])}</td>
                <td>${fmtCurrency(a["Linear_Revenue"])}</td>
                <td>${fmtPct(a["Linear_Revenue_Share_Pct"])}</td>
                <td><strong>${fmtCurrency(a["Position_Based_Revenue"])}</strong></td>
                <td><strong>${fmtPct(a["Position_Based_Revenue_Share_Pct"])}</strong></td>
                <td><span style="font-size:11px;font-weight:600;">${shiftText}</span></td>
            `;
            tableAttrBody.appendChild(tr);
        });
    }

    // -------------------------------------------------------------
    // 6. Chart.js Initialization
    // -------------------------------------------------------------

    // Page 1: Monthly Trends (Combo Bar & Line)
    const ctxMonthly = document.getElementById("chart-monthly-trends");
    if (ctxMonthly) {
        charts.monthly = new Chart(ctxMonthly, {
            type: "bar",
            data: {
                labels: data.monthly.map(m => m["Month_Name"]),
                datasets: [
                    {
                        type: "bar",
                        label: "Spend ($)",
                        data: data.monthly.map(m => m["Marketing Spend"]),
                        backgroundColor: "rgba(59, 130, 246, 0.75)",
                        borderColor: "#3b82f6",
                        borderWidth: 1,
                        yAxisID: "y"
                    },
                    {
                        type: "bar",
                        label: "Revenue ($)",
                        data: data.monthly.map(m => m["Revenue"]),
                        backgroundColor: "rgba(16, 185, 129, 0.8)",
                        borderColor: "#10b981",
                        borderWidth: 1,
                        yAxisID: "y"
                    },
                    {
                        type: "line",
                        label: "ROAS (x)",
                        data: data.monthly.map(m => m["roas"]),
                        borderColor: "#8b5cf6",
                        backgroundColor: "#8b5cf6",
                        borderWidth: 2.5,
                        tension: 0.3,
                        yAxisID: "y1"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { callback: v => "$" + (v / 1000) + "k" }
                    },
                    y1: {
                        position: "right",
                        beginAtZero: true,
                        grid: { drawOnChartArea: false },
                        ticks: { callback: v => v + "x" }
                    }
                }
            }
        });
    }

    // Page 1: Revenue Donut
    const ctxDonut = document.getElementById("chart-revenue-donut");
    if (ctxDonut) {
        charts.donut = new Chart(ctxDonut, {
            type: "doughnut",
            data: {
                labels: data.channels.map(c => c["Marketing Channel"]),
                datasets: [{
                    data: data.channels.map(c => c["Revenue"]),
                    backgroundColor: [
                        "#10b981", "#3b82f6", "#8b5cf6", "#f59e0b", "#ef4444", "#06b6d4"
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "right" }
                }
            }
        });
    }

    // Page 2: Channel ROI Bar Chart
    const ctxRoi = document.getElementById("chart-channel-roi");
    if (ctxRoi) {
        charts.roi = new Chart(ctxRoi, {
            type: "bar",
            data: {
                labels: data.channels.map(c => c["Marketing Channel"]),
                datasets: [{
                    label: "ROI (%)",
                    data: data.channels.map(c => c["roi_pct"]),
                    backgroundColor: "#3b82f6"
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { ticks: { callback: v => v + "%" } }
                }
            }
        });
    }

    // Page 2: Channel ROAS Bar Chart
    const ctxRoas = document.getElementById("chart-channel-roas");
    if (ctxRoas) {
        charts.roas = new Chart(ctxRoas, {
            type: "bar",
            data: {
                labels: data.channels.map(c => c["Marketing Channel"]),
                datasets: [{
                    label: "ROAS (x)",
                    data: data.channels.map(c => c["roas"]),
                    backgroundColor: "#10b981"
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { ticks: { callback: v => v + "x" } }
                }
            }
        });
    }

    // Page 2: CAC vs CPC
    const ctxCacCpc = document.getElementById("chart-cac-cpc");
    if (ctxCacCpc) {
        charts.cacCpc = new Chart(ctxCacCpc, {
            type: "bar",
            data: {
                labels: data.channels.map(c => c["Marketing Channel"]),
                datasets: [
                    {
                        label: "CAC ($)",
                        data: data.channels.map(c => c["cac"]),
                        backgroundColor: "#f59e0b"
                    },
                    {
                        label: "CPC ($)",
                        data: data.channels.map(c => c["cpc"]),
                        backgroundColor: "#06b6d4"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { ticks: { callback: v => "$" + v } }
                }
            }
        });
    }

    // Page 2: Funnel Rates
    const ctxFunnel = document.getElementById("chart-funnel-rates");
    if (ctxFunnel) {
        charts.funnel = new Chart(ctxFunnel, {
            type: "bar",
            data: {
                labels: data.channels.map(c => c["Marketing Channel"]),
                datasets: [
                    {
                        label: "CTR (%)",
                        data: data.channels.map(c => c["ctr"]),
                        backgroundColor: "#3b82f6"
                    },
                    {
                        label: "Conversion Rate (%)",
                        data: data.channels.map(c => c["conv_rate"]),
                        backgroundColor: "#10b981"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { ticks: { callback: v => v + "%" } }
                }
            }
        });
    }

    // Page 4: Attribution Comparison Multi-Bar
    const ctxAttrComp = document.getElementById("chart-attribution-comparison");
    if (ctxAttrComp) {
        charts.attrComp = new Chart(ctxAttrComp, {
            type: "bar",
            data: {
                labels: data.attribution.map(a => a["Marketing Channel"]),
                datasets: [
                    {
                        label: "First-Touch",
                        data: data.attribution.map(a => a["First_Touch_Revenue"]),
                        backgroundColor: "#3b82f6"
                    },
                    {
                        label: "Last-Touch",
                        data: data.attribution.map(a => a["Last_Touch_Revenue"]),
                        backgroundColor: "#ef4444"
                    },
                    {
                        label: "Linear",
                        data: data.attribution.map(a => a["Linear_Revenue"]),
                        backgroundColor: "#f59e0b"
                    },
                    {
                        label: "Position-Based (40-40-20)",
                        data: data.attribution.map(a => a["Position_Based_Revenue"]),
                        backgroundColor: "#10b981"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { ticks: { callback: v => "$" + (v / 1000) + "k" } }
                }
            }
        });
    }

    // Page 4: Attribution Shift Bar
    const ctxAttrShift = document.getElementById("chart-attribution-shift");
    if (ctxAttrShift) {
        const shifts = data.attribution.map(a => a["Last_Touch_Revenue"] - a["First_Touch_Revenue"]);
        charts.attrShift = new Chart(ctxAttrShift, {
            type: "bar",
            data: {
                labels: data.attribution.map(a => a["Marketing Channel"]),
                datasets: [{
                    label: "Shift ($)",
                    data: shifts,
                    backgroundColor: shifts.map(s => s >= 0 ? "#10b981" : "#ef4444")
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { ticks: { callback: v => "$" + (v / 1000) + "k" } }
                }
            }
        });
    }

    // Slicers interaction
    const channelSlicer = document.getElementById("channel-slicer");
    if (channelSlicer) {
        channelSlicer.addEventListener("change", e => {
            const selected = e.target.value;
            if (selected === "ALL") {
                document.getElementById("kpi-spend").textContent = fmtCurrency(data.kpis.total_spend);
                document.getElementById("kpi-revenue").textContent = fmtCurrency(data.kpis.total_revenue);
                document.getElementById("kpi-roi").textContent = fmtPct(data.kpis.roi_pct);
                document.getElementById("kpi-roas").textContent = fmtMult(data.kpis.roas);
                document.getElementById("kpi-conv").textContent = fmtInt(data.kpis.conversions);
                document.getElementById("kpi-leads").textContent = fmtInt(data.kpis.leads);
            } else {
                const ch = data.channels.find(c => c["Marketing Channel"] === selected);
                if (ch) {
                    document.getElementById("kpi-spend").textContent = fmtCurrency(ch["Marketing Spend"]);
                    document.getElementById("kpi-revenue").textContent = fmtCurrency(ch["Revenue"]);
                    document.getElementById("kpi-roi").textContent = fmtPct(ch["roi_pct"]);
                    document.getElementById("kpi-roas").textContent = fmtMult(ch["roas"]);
                    document.getElementById("kpi-conv").textContent = fmtInt(ch["Conversions"]);
                    document.getElementById("kpi-leads").textContent = fmtInt(ch["Leads"]);
                }
            }
        });
    }
});
