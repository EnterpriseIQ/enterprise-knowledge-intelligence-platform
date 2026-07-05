import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Loader2, ShieldCheck, ShieldAlert, FileText, Check, Sparkles, Copy, ThumbsUp, ThumbsDown, RefreshCw, Clock, Cpu, History, Activity, Terminal } from 'lucide-react';
import { Button } from './ui/button';

// Add explicit types for the result to avoid any
interface Citation {
  document_id: string;
}

interface QueryResult {
  answer: string;
  confidence: { score: number };
  routing?: { route_type: string };
  access_summary?: {
    authorised_chunks: number;
    denied_chunks: number;
  };
  citations?: Citation[];
  metadata?: {
    execution_time_ms: number;
    tokens_used: number;
    model: string;
  };
}

const suggestedQueries = [
  "What were our Q3 earnings?",
  "Summarize the new remote work policy",
  "Explain the backend architecture",
  "Generate a Python script for data processing",
  "How do I setup SSO?"
];

const getMockResponse = (q: string): QueryResult => {
  const lowerQ = q.toLowerCase();

  const baseMetadata = {
    execution_time_ms: Math.floor(Math.random() * (1200 - 400 + 1) + 400),
    tokens_used: Math.floor(Math.random() * (800 - 150 + 1) + 150),
    model: "llama-3-70b-instruct"
  };

  if (lowerQ.includes('earning') || lowerQ.includes('revenue') || lowerQ.includes('financial') || lowerQ.includes('q3')) {
    return {
      answer: "Based on the Q3 financial reports, EnterpriseIQ's revenue grew by 24% year-over-year to $14.2M. The enterprise software division was the primary driver, accounting for 65% of total revenue. Operating margins improved from 18% to 22% due to optimized cloud infrastructure costs.",
      confidence: { score: 0.94 },
      routing: { route_type: "financial_structured_data" },
      access_summary: { authorised_chunks: 12, denied_chunks: 0 },
      citations: [{ document_id: "Q3_Earnings_Report_Final.pdf" }, { document_id: "Financial_Metrics_Dashboard_2023.xlsx" }],
      metadata: { ...baseMetadata, execution_time_ms: 1240, tokens_used: 450 }
    };
  } else if (lowerQ.includes('policy') || lowerQ.includes('leave') || lowerQ.includes('hr') || lowerQ.includes('remote')) {
     return {
      answer: "According to the updated employee handbook (v2.1), full-time employees are entitled to 20 days of paid time off (PTO) annually, plus 10 public holidays. The new remote work policy allows up to 3 days of work-from-home per week. Parental leave has been expanded to 16 weeks fully paid for the primary caregiver.",
      confidence: { score: 0.98 },
      routing: { route_type: "hr_policy_unstructured" },
      access_summary: { authorised_chunks: 5, denied_chunks: 2 },
      citations: [{ document_id: "Employee_Handbook_v2.1.pdf" }, { document_id: "HR_Benefits_Update_Memo.docx" }],
      metadata: { ...baseMetadata, execution_time_ms: 850, tokens_used: 320 }
    };
  } else if (lowerQ.includes('architecture') || lowerQ.includes('tech') || lowerQ.includes('stack')) {
    return {
      answer: "The platform's architecture is built on a microservices model. The backend utilizes Python and FastAPI, deployed via Kubernetes. The frontend is a React application built with Vite, TypeScript, and Tailwind CSS. Data is stored in PostgreSQL, with Redis for caching and Elasticsearch for document retrieval.",
      confidence: { score: 0.91 },
      routing: { route_type: "engineering_wiki" },
      access_summary: { authorised_chunks: 8, denied_chunks: 0 },
      citations: [{ document_id: "Architecture_Overview_v3.md" }, { document_id: "Tech_Stack_Proposal.pdf" }],
      metadata: { ...baseMetadata, execution_time_ms: 920, tokens_used: 380 }
    };
  } else if (lowerQ.includes('python') || lowerQ.includes('script') || lowerQ.includes('code')) {
    return {
      answer: "Here is a Python script that uses pandas to process the dataset:\n\n```python\nimport pandas as pd\n\ndef process_data(file_path):\n    df = pd.read_csv(file_path)\n    df.dropna(inplace=True)\n    df['Total'] = df['Quantity'] * df['Price']\n    return df.groupby('Category').sum()\n```\n\nThis script reads a CSV file, removes rows with missing values, calculates a 'Total' column, and aggregates the results by 'Category'.",
      confidence: { score: 0.88 },
      routing: { route_type: "code_generation" },
      access_summary: { authorised_chunks: 2, denied_chunks: 0 },
      citations: [{ document_id: "Data_Processing_Guidelines.md" }],
      metadata: { ...baseMetadata, execution_time_ms: 1800, tokens_used: 650, model: "qwen-2.5-coder-32b" }
    };
  } else if (lowerQ.includes('sso') || lowerQ.includes('saml') || lowerQ.includes('auth')) {
    return {
      answer: "To set up Single Sign-On (SSO) via SAML 2.0:\n\n1. Navigate to the Admin Console -> Security -> Identity Providers.\n2. Click 'Add Provider' and select SAML.\n3. Enter your IdP metadata URL or upload the XML file.\n4. Map the email and group attributes to `user.email` and `user.groups` respectively.\n5. Test the connection before enforcing SSO globally.",
      confidence: { score: 0.95 },
      routing: { route_type: "admin_documentation" },
      access_summary: { authorised_chunks: 4, denied_chunks: 1 },
      citations: [{ document_id: "SSO_Configuration_Guide_v2.pdf" }],
      metadata: { ...baseMetadata, execution_time_ms: 700, tokens_used: 280 }
    };
  }

  return {
    answer: `Here is a synthesized response for your query: "${q}".\n\nThe platform has retrieved relevant information from your enterprise data sources. It utilizes a hybrid search approach combining dense vector embeddings and keyword matching to find the most accurate context before synthesizing this response using the configured LLM.`,
    confidence: { score: 0.85 },
    routing: { route_type: "general_knowledge_rag" },
    access_summary: { authorised_chunks: 4, denied_chunks: 1 },
    citations: [{ document_id: "Enterprise_Knowledge_Base.md" }],
    metadata: baseMetadata
  };
}

export const QueryForm = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QueryResult | null>(null);
  const [history, setHistory] = useState<string[]>([]);
  const [currentStep, setCurrentStep] = useState<string>('');

  // Use env var or default to the hosted api URL if public
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const executeSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    setResult(null);
    setCurrentStep('Analyzing intent...');

    // Add to history if unique
    setHistory(prev => {
      const filtered = prev.filter(q => q !== searchQuery);
      return [searchQuery, ...filtered].slice(0, 5); // Keep last 5
    });

    try {
      const res = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery }),
      });
      if (!res.ok) throw new Error('API not available');
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.warn("Backend not reachable, using simulated response for playground.", err);
      // Simulate agentic steps delay
      await new Promise(resolve => setTimeout(resolve, 500));
      setCurrentStep('Retrieving contexts...');
      await new Promise(resolve => setTimeout(resolve, 600));
      setCurrentStep('Reranking documents...');
      await new Promise(resolve => setTimeout(resolve, 500));
      setCurrentStep('Synthesizing response...');
      await new Promise(resolve => setTimeout(resolve, 800));

      setResult(getMockResponse(searchQuery));
    } finally {
      setLoading(false);
      setCurrentStep('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    executeSearch(query);
  };

  return (
    <div className="w-full h-full flex flex-col p-4 opacity-100 bg-[#0A0A0A] rounded-2xl relative">
      {/* Header */}
      <div className="flex items-center gap-2 mb-4 border-b border-white/5 pb-4">
        <div className="w-3 h-3 rounded-full bg-red-500" />
        <div className="w-3 h-3 rounded-full bg-yellow-500" />
        <div className="w-3 h-3 rounded-full bg-green-500" />
        <div className="ml-4 text-xs font-mono text-muted-foreground flex items-center gap-2">
          agent.execute(query="<span className="text-white">{query || '...'}</span>")
        </div>
        <div className="ml-auto text-xs font-mono text-blue-400/70 flex items-center gap-1.5 bg-blue-500/10 px-2 py-1 rounded-md border border-blue-500/20">
          <Sparkles className="w-3 h-3" />
          Interactive Playground
        </div>
      </div>

      {/* Search Input */}
      <form onSubmit={handleSubmit} className="relative mb-3">
        <div className="relative flex items-center">
          <Search className="absolute left-4 w-5 h-5 text-muted-foreground" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about enterprise data, earnings, or policies..."
            className="w-full bg-white/5 border border-white/10 rounded-xl py-4 pl-12 pr-32 text-sm text-white placeholder:text-white/40 focus:outline-none focus:border-white/20 transition-colors"
          />
          <Button
            type="submit"
            disabled={loading || !query.trim()}
            className="absolute right-2 top-2 bottom-2 rounded-lg bg-primary hover:bg-primary/90 text-primary-foreground font-medium px-4 py-2"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Search'}
          </Button>
        </div>
      </form>

      {/* History */}
      {history.length > 0 && (
        <div className="flex items-center gap-2 mb-3 overflow-x-auto scrollbar-none pb-1">
          <History className="w-3.5 h-3.5 text-muted-foreground flex-shrink-0" />
          <div className="flex gap-2">
            {history.map((h, i) => (
              <button
                key={`hist-${i}`}
                type="button"
                onClick={() => {
                  setQuery(h);
                  executeSearch(h);
                }}
                className="whitespace-nowrap text-xs px-2.5 py-1 rounded-md bg-white/[0.03] border border-white/5 text-white/60 hover:bg-white/10 hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background"
              >
                {h}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Suggested Queries */}
      <div className="flex flex-wrap gap-2 mb-6">
        {suggestedQueries.map((sq, i) => (
          <button
            key={i}
            type="button"
            onClick={() => {
              setQuery(sq);
              executeSearch(sq);
            }}
            className="text-xs px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-white/70 hover:bg-white/10 hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background"
          >
            {sq}
          </button>
        ))}
      </div>

      {/* Results Area */}
      <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent pr-2 space-y-4">
        <AnimatePresence mode="wait">
          {!result && !loading && (
             <motion.div
               initial={{ opacity: 0 }}
               animate={{ opacity: 1 }}
               exit={{ opacity: 0 }}
               className="h-full flex flex-col items-center justify-center text-muted-foreground gap-4 pb-12"
             >
               <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center border border-white/10 relative">
                 <div className="absolute inset-0 rounded-full border border-white/5 animate-ping opacity-20" />
                 <Search className="w-8 h-8 opacity-50" />
               </div>
               <p>Enter a query to run the agentic RAG pipeline.</p>
             </motion.div>
          )}

          {loading && (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center h-full gap-6 pb-12"
            >
              <div className="relative flex items-center justify-center">
                <Loader2 className="w-10 h-10 text-primary animate-spin" />
                <Terminal className="w-4 h-4 text-primary absolute" />
              </div>
              <div className="flex flex-col items-center gap-2">
                <p className="text-sm font-mono text-white/80 animate-pulse">{currentStep}</p>
                <div className="flex gap-1">
                   <div className="w-1.5 h-1.5 rounded-full bg-primary/50 animate-bounce" style={{ animationDelay: '0ms' }} />
                   <div className="w-1.5 h-1.5 rounded-full bg-primary/50 animate-bounce" style={{ animationDelay: '150ms' }} />
                   <div className="w-1.5 h-1.5 rounded-full bg-primary/50 animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </motion.div>
          )}

          {result && !loading && (
            <motion.div
              key="result"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6 pb-8"
            >
              {/* Answer */}
              <div className="bg-white/[0.02] border border-white/10 rounded-xl p-6 relative group">
                <h3 className="text-sm font-semibold text-white/70 uppercase tracking-wider mb-3 flex items-center gap-2">
                  <Check className="w-4 h-4 text-green-400" />
                  Synthesized Answer
                </h3>
                <p className="text-white text-base leading-relaxed whitespace-pre-wrap">{result.answer}</p>
                <div className="mt-6 pt-4 border-t border-white/5 flex items-center justify-between">
                  <div className="flex items-center gap-4 text-xs font-mono text-muted-foreground">
                    <span className="flex items-center gap-1.5"><div className={`w-2 h-2 rounded-full ${result.confidence?.score > 0.8 ? 'bg-green-400' : 'bg-yellow-400'}`} /> Confidence: {((result.confidence?.score || 0) * 100).toFixed(0)}%</span>
                    <span>Route: {result.routing?.route_type || 'Unknown'}</span>
                  </div>
                  <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button className="p-1.5 rounded bg-white/5 hover:bg-white/10 text-white/70 hover:text-white transition-colors" title="Copy to clipboard">
                      <Copy className="w-4 h-4" />
                    </button>
                    <button className="p-1.5 rounded bg-white/5 hover:bg-white/10 text-white/70 hover:text-white transition-colors" title="Good response">
                      <ThumbsUp className="w-4 h-4" />
                    </button>
                    <button className="p-1.5 rounded bg-white/5 hover:bg-white/10 text-white/70 hover:text-white transition-colors" title="Bad response">
                      <ThumbsDown className="w-4 h-4" />
                    </button>
                    <button className="p-1.5 rounded bg-white/5 hover:bg-white/10 text-white/70 hover:text-white transition-colors" title="Regenerate" onClick={() => executeSearch(query)}>
                      <RefreshCw className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>

              <div className={`grid grid-cols-1 ${result.metadata ? 'md:grid-cols-3' : 'md:grid-cols-2'} gap-4`}>
                {/* Access Summary */}
                <div className="bg-white/[0.02] border border-white/10 rounded-xl p-6">
                   <h3 className="text-sm font-semibold text-white/70 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-blue-400" />
                    RBAC Trace
                  </h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 rounded-lg bg-green-500/10 border border-green-500/20">
                      <span className="text-sm text-green-400 flex items-center gap-2"><ShieldCheck className="w-4 h-4" /> Authorised Chunks</span>
                      <span className="font-mono text-green-400 font-semibold">{result.access_summary?.authorised_chunks || 0}</span>
                    </div>
                    <div className="flex items-center justify-between p-3 rounded-lg bg-red-500/10 border border-red-500/20 opacity-80">
                      <span className="text-sm text-red-400 flex items-center gap-2"><ShieldAlert className="w-4 h-4" /> Denied Chunks</span>
                      <span className="font-mono text-red-400 font-semibold">{result.access_summary?.denied_chunks || 0}</span>
                    </div>
                  </div>
                </div>

                {/* Citations */}
                <div className="bg-white/[0.02] border border-white/10 rounded-xl p-6">
                  <h3 className="text-sm font-semibold text-white/70 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <FileText className="w-4 h-4 text-purple-400" />
                    Sources Used
                  </h3>
                  <div className="space-y-2 max-h-[120px] overflow-y-auto scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent pr-2">
                    {result.citations?.map((c: Citation, i: number) => (
                      <div key={i} className="flex items-center justify-between p-2 rounded bg-white/5 border border-white/5 text-sm">
                        <span className="text-white/80 truncate max-w-[200px]">{c.document_id}</span>
                        <span className="text-xs text-muted-foreground font-mono">[{i + 1}]</span>
                      </div>
                    ))}
                    {(!result.citations || result.citations.length === 0) && (
                      <p className="text-sm text-muted-foreground">No specific sources cited.</p>
                    )}
                  </div>
                </div>

                {/* Metadata */}
                {result.metadata && (
                  <div className="bg-white/[0.02] border border-white/10 rounded-xl p-6">
                    <h3 className="text-sm font-semibold text-white/70 uppercase tracking-wider mb-4 flex items-center gap-2">
                      <Activity className="w-4 h-4 text-orange-400" />
                      Execution Meta
                    </h3>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between p-2.5 rounded-lg bg-white/5 border border-white/5">
                        <span className="text-sm text-white/60 flex items-center gap-2"><Clock className="w-4 h-4" /> Latency</span>
                        <span className="font-mono text-white/90 text-sm">{result.metadata.execution_time_ms}ms</span>
                      </div>
                      <div className="flex items-center justify-between p-2.5 rounded-lg bg-white/5 border border-white/5">
                        <span className="text-sm text-white/60 flex items-center gap-2"><Cpu className="w-4 h-4" /> Tokens</span>
                        <span className="font-mono text-white/90 text-sm">{result.metadata.tokens_used}</span>
                      </div>
                      <div className="flex items-center justify-between p-2.5 rounded-lg bg-white/5 border border-white/5">
                        <span className="text-sm text-white/60 flex items-center gap-2"><Terminal className="w-4 h-4" /> Model</span>
                        <span className="font-mono text-white/90 text-xs truncate max-w-[100px]" title={result.metadata.model}>{result.metadata.model}</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};
