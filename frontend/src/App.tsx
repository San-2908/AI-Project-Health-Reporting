import React, { useState } from 'react';
import axios from 'axios';
import { UploadCloud, FileText, Download, Activity, Brain, AlertTriangle, ArrowLeft, X, Zap } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import ReactMarkdown from 'react-markdown';

const API_BASE = 'http://localhost:8000/api/v1';

function App() {
  const [files, setFiles] = useState<FileList | null>(null);
  const [loading, setLoading] = useState(false);
  const [projects, setProjects] = useState<any[]>([]);

  // Recovery Plan State
  const [activeRecoveryProject, setActiveRecoveryProject] = useState<string | null>(null);
  const [recoveryPlanContent, setRecoveryPlanContent] = useState<string>('');
  const [isRecoveryLoading, setIsRecoveryLoading] = useState(false);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!files || files.length === 0) return;
    
    setLoading(true);
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }

    try {
      const response = await axios.post(`${API_BASE}/upload`, formData);
      setProjects(response.data);
    } catch (error) {
      console.error('Error uploading:', error);
      alert('Upload failed. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPPT = async () => {
    try {
      const response = await axios.get(`${API_BASE}/download-ppt`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'Portfolio_Report.pptx');
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error('Download failed', error);
      alert('Could not download presentation.');
    }
  };
  
  const handleStartOver = () => {
    setProjects([]);
    setFiles(null);
  };

  const handleGenerateRecoveryPlan = async (projectName: string) => {
    setActiveRecoveryProject(projectName);
    setIsRecoveryLoading(true);
    setRecoveryPlanContent('');
    try {
      const response = await axios.post(`${API_BASE}/recovery-plan/${encodeURIComponent(projectName)}`);
      setRecoveryPlanContent(response.data.recovery_plan);
    } catch (error) {
      console.error('Error generating recovery plan:', error);
      setRecoveryPlanContent('Failed to generate plan. Please try again.');
    } finally {
      setIsRecoveryLoading(false);
    }
  };

  const closeRecoveryModal = () => {
    setActiveRecoveryProject(null);
    setRecoveryPlanContent('');
  };

  const chartData = projects.map(p => ({
    name: p.project_name,
    completion: p.completion_percentage
  }));
  
  // Calculate RAG distribution for the new Pie Chart feature
  const ragCounts = projects.reduce((acc, p) => {
    const status = p.status?.rag_score || 'Unknown';
    acc[status] = (acc[status] || 0) + 1;
    return acc;
  }, {});
  
  const pieData = Object.keys(ragCounts).map(key => ({
    name: key,
    value: ragCounts[key]
  }));

  const COLORS: Record<string, string> = {
    GREEN: 'var(--green-text)',
    AMBER: 'var(--amber-text)',
    RED: 'var(--red-text)',
    Unknown: 'var(--text-tertiary)'
  };

  return (
    <div style={{ padding: '2.5rem', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Modal Overlay */}
      {activeRecoveryProject && (
        <div className="modal-overlay" onClick={closeRecoveryModal}>
          <div className="modal-content markdown-body" onClick={e => e.stopPropagation()}>
            <button className="modal-close" onClick={closeRecoveryModal}>
              <X size={24} />
            </button>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem', color: 'var(--accent-color)' }}>
              <Zap size={28} />
              <h2 style={{ margin: 0, color: 'var(--text-primary)' }}>AI Recovery Action Plan</h2>
            </div>
            <h3 style={{ marginTop: 0, marginBottom: '2rem', color: 'var(--text-secondary)' }}>Project: {activeRecoveryProject}</h3>
            
            {isRecoveryLoading ? (
              <div style={{ textAlign: 'center', padding: '3rem 0', color: 'var(--text-tertiary)' }}>
                <Brain size={48} className="animate-pulse" style={{ margin: '0 auto 1rem', color: 'var(--accent-color)', animation: 'pulse 1.5s infinite' }} />
                <p>Analyzing blockers and generating 30-day tactical plan...</p>
              </div>
            ) : (
              <ReactMarkdown>{recoveryPlanContent}</ReactMarkdown>
            )}
          </div>
        </div>
      )}

      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          {projects.length > 0 && (
            <button 
              onClick={handleStartOver} 
              style={{ background: 'transparent', boxShadow: 'none', padding: '0.5rem', marginRight: '0.5rem' }}
              title="Start Over"
            >
              <ArrowLeft size={24} color="var(--text-secondary)" />
            </button>
          )}
          <Activity size={36} color="var(--primary-color)" style={{ filter: 'drop-shadow(0 0 8px var(--primary-glow))' }} />
          <h1>AI Project Health Reporting</h1>
        </div>
        {projects.length > 0 && (
          <button onClick={handleDownloadPPT} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Download size={18} /> Export PPT
          </button>
        )}
      </header>

      {projects.length === 0 ? (
        <div className="glass-card" style={{ maxWidth: '600px', margin: '0 auto', textAlign: 'center' }}>
          <div className="upload-zone">
            <UploadCloud size={64} style={{ color: 'var(--primary-color)', marginBottom: '1rem', filter: 'drop-shadow(0 0 10px var(--primary-glow))' }} />
            <h2>Upload Project Plans</h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>Upload one or multiple Excel project plans to generate AI health reports.</p>
            <form onSubmit={handleUpload}>
              <input 
                type="file" 
                multiple 
                accept=".xls,.xlsx"
                onChange={(e) => setFiles(e.target.files)}
                style={{ 
                  display: 'block', 
                  margin: '0 auto 1.5rem',
                  padding: '1rem',
                  background: 'rgba(255,255,255,0.05)',
                  borderRadius: '0.5rem',
                  border: '1px solid rgba(255,255,255,0.1)',
                  color: 'var(--text-primary)'
                }}
              />
              <button type="submit" disabled={!files || loading}>
                {loading ? 'Analyzing Projects...' : 'Analyze Projects'}
              </button>
            </form>
          </div>
        </div>
      ) : (
        <>
          <div className="dashboard-grid">
            {projects.map((project, idx) => (
              <div key={idx} className={`glass-card animate-delay-${(idx % 3) + 1}`} style={{ display: 'flex', flexDirection: 'column' }}>
                <div style={{ flexGrow: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.25rem' }}>
                    <h3 style={{ marginRight: '1rem' }}>{project.project_name}</h3>
                    <span className={`badge rag-${project.status?.rag_score.toLowerCase()}`}>
                      <Activity size={14} />
                      {project.status?.rag_score}
                    </span>
                  </div>
                  
                  <div style={{ marginBottom: '1.25rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '0.25rem', color: 'var(--text-secondary)' }}>
                      <span>Completion</span>
                      <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{project.completion_percentage.toFixed(1)}%</span>
                    </div>
                    <div className="progress-container">
                      <div className="progress-fill" style={{ width: `${project.completion_percentage}%` }}></div>
                    </div>
                  </div>

                  <p style={{ color: '#e2e8f0', fontSize: '0.95rem', lineHeight: '1.5' }}><strong>Summary:</strong> {project.status?.summary}</p>
                  
                  {project.status?.reasoning && (
                    <div className="reasoning-box">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', color: 'var(--accent-color)', fontWeight: 600 }}>
                        <Brain size={16} />
                        AI Reasoning
                      </div>
                      {project.status.reasoning}
                    </div>
                  )}
                  
                  <div style={{ marginTop: '1.5rem', marginBottom: '1.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--amber-text)', fontWeight: 600, fontSize: '0.95rem' }}>
                      <AlertTriangle size={16} />
                      Top Risks
                    </div>
                    <ul style={{ paddingLeft: '1.5rem', marginTop: '0.5rem', fontSize: '0.9rem' }}>
                      {project.status?.top_risks.map((risk: string, i: number) => (
                        <li key={i}>{risk}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                
                {(project.status?.rag_score === 'RED' || project.status?.rag_score === 'AMBER') && (
                  <button 
                    onClick={() => handleGenerateRecoveryPlan(project.project_name)}
                    style={{ width: '100%', marginTop: 'auto', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                  >
                    <Zap size={16} />
                    Generate Action Plan
                  </button>
                )}
              </div>
            ))}
          </div>
          
          <div className="dashboard-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))' }}>
            <div className="glass-card animate-delay-2" style={{ marginTop: '1rem', height: '400px' }}>
              <h3 style={{ marginBottom: '1.5rem' }}>RAG Status Distribution</h3>
              <ResponsiveContainer width="100%" height="85%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={70}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    labelStyle={{ fill: 'var(--text-primary)', fontSize: '0.9rem' }}
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[entry.name] || COLORS.Unknown} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'var(--bg-mid)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: 'var(--text-primary)' }} 
                    itemStyle={{ color: 'var(--text-primary)' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="glass-card animate-delay-3" style={{ marginTop: '1rem', height: '400px' }}>
              <h3 style={{ marginBottom: '1.5rem' }}>Portfolio Completion Status</h3>
              <ResponsiveContainer width="100%" height="85%">
                <BarChart data={chartData}>
                  <XAxis dataKey="name" stroke="var(--text-secondary)" tick={{ fill: 'var(--text-secondary)' }} />
                  <YAxis stroke="var(--text-secondary)" tick={{ fill: 'var(--text-secondary)' }} domain={[0, 100]} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'var(--bg-mid)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: 'var(--text-primary)' }} 
                    itemStyle={{ color: 'var(--text-primary)' }}
                  />
                  <Bar dataKey="completion" fill="var(--primary-color)" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
