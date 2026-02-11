import axios from "axios";
import React, { useState } from "react";
import "./Summarizer.css";

interface RiskItem {
  description: string;
  severity: "Low" | "Medium" | "High" | "Critical";
}

const Summarizer = () => {
  const [inputText, setInputText] = useState("");
  const [data, setData] = useState<any>(null);
  const [status, setStatus] = useState<"idle" | "working" | "done">("idle");

  const handleSummarizer = async () => {
    setData(null);
    setStatus("working");
    try {
      const response = await axios.post("http://127.0.0.1:8000/summarize", {
        text: inputText,
      });
      setData(response.data);
      setStatus("done");
    } catch (error) {
      console.log("Error", error);
      setStatus("idle");
    }
  };

  const handleClear = () => {
    setInputText("");
    setData(null);
    setStatus("idle");
  };

  // Helper to get border colors for the risk cards
  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case "critical":
        return "#dc2626";
      case "high":
        return "#ea580c";
      case "medium":
        return "#ca8a04";
      case "low":
        return "#0284c7";
      default:
        return "#9ca3af";
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Compliance Auditor</h1>
        <p>AI-Powered 3-Pass Reflection Pipeline</p>
      </header>
      <div className="input-section">
        <textarea
          autoFocus
          placeholder="Paste document text here....."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          className="textArea"
        />
        <br />
        <div className="button-group">
          <button
            onClick={handleSummarizer}
            disabled={status === "working" || !inputText}
            className={`btn ${status === "working" ? "btn-loading" : "btn-primary"}`}
          >
            {status === "working"
              ? "Auditing (3-Pass Reflection)..."
              : "Generate Summary"}
          </button>
          <button onClick={handleClear} className="btn-secondary ">
            Clear All
          </button>
        </div>
      </div>

      {status !== "idle" && (
        <div className="trace-container">
          <div className="card draft-card">
            <span className="badge">Step 1: Initial Draft</span>
            <p>{status === "working" ? "Generating..." : data?.draft}</p>
          </div>
          <div className="card critique-card">
            <span className="badge">Step 2: Internal Audit</span>
            <p className="italic">
              {status === "working" ? "Waiting..." : data?.critique}
            </p>
          </div>
          <div className="card final-card">
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <span className="badge">Step 3: Verified Compliance Report</span>
              {status === "working" && <div className="spinner-small"></div>}
            </div>
            {data?.final?.key_risks.length === 0 &&
            data?.final?.obligations.length === 0 ? (
              <div className="no-compliance-alert">
                <strong>Notice:</strong> This document does not appear to
                contain regulatory compliance data.
              </div>
            ) : data?.final ? (
              <div className="report-grid">
                <div className="report-item">
                  <h4>Executive Summary</h4>
                  <p>{data?.final?.summary}</p>
                </div>

                <div className="report-item obligation-section">
                  <h4>Legal Obligations</h4>
                  <div className="obligation-list">
                    {data?.final.obligations.map((ob: string, i: number) => (
                      <div key={i} className="obligation-card">
                        <span className="check-icon">✓</span> {ob}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="report-row">
                  <div className="report-item risk">
                    <h4>Key Risks</h4>
                    <ul>
                      {data?.final.key_risks.map((r: RiskItem, i: number) => {
                        const sevClass = r.severity.toLowerCase();
                        const isCritical = sevClass === "critical";
                        return (
                          <div
                            key={i}
                            className={`risk-card ${isCritical ? "pulse-critical" : ""}`}
                            style={{
                              border: `1px solid ${getSeverityColor(r.severity)}`,
                            }}
                          >
                            <span className={`severity-badge ${sevClass}`}>
                              {r.severity}
                            </span>
                            <p>{r.description}</p>
                          </div>
                        );
                      })}
                    </ul>
                  </div>
                  <div className="report-item action">
                    <h4>Recommended Actions</h4>
                    <ul>
                      {data?.final.recommended_actions.map(
                        (a: string, i: number) => (
                          <li key={i}>{a}</li>
                        ),
                      )}
                    </ul>
                  </div>
                </div>
                <div className="disclaimer">
                  <strong>Safety Disclaimer:</strong> AI-generated content. If
                  missing info is detected: {data?.final?.missing_info}
                </div>
              </div>
            ) : (
              <p className="italic">Waiting for final synthesis...</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Summarizer;
