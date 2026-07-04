import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Loader2, ShieldCheck, ShieldAlert, FileText, Check, Sparkles } from 'lucide-react';
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
}

const suggestedQueries = [
  "What were our Q3 earnings?",
  "Summarize the new remote work policy",
  "Explain the backend architecture"
];

const getMockResponse = (q: string): QueryResult => {
  const lowerQ = q.toLowerCase();

  if (lowerQ.includes('earning') || lowerQ.includes('revenue') || lowerQ.includes('financial') || lowerQ.includes('q3')) {
    return {
      answer: "Based on the Q3 financial reports, EnterpriseIQ's revenue grew by 24% year-over-year to $14.2M. The enterprise software division was the primary driver, accounting for 65% of total revenue. Operating margins improved from 18% to 22% due to optimized cloud infrastructure costs.",
      confidence: { score: 0.94 },
      routing: { route_type: "financial_structured_data" },
      access_summary: { authorised_chunks: 12, denied_chunks: 0 },
      citations: [{ document_id: "Q3_Earnings_Report_Final.pdf" }, { document_id: "Financial_Metrics_Dashboard_2023.xlsx" }]
    };
  } else if (lowerQ.includes('policy') || lowerQ.includes('leave') || lowerQ.includes('hr') || lowerQ.includes('remote')) {
     return {
      answer: "According to the updated employee handbook (v2.1), full-time employees are entitled to 20 days of paid time off (PTO) annually, plus 10 public holidays. The new remote work policy allows up to 3 days of work-from-home per week. Parental leave has been expanded to 16 weeks fully paid for the primary caregiver.",
      confidence: { score: 0.98 },
      routing: { route_type: "hr_policy_unstructured" },
      access_summary: { authorised_chunks: 5, denied_chunks: 2 },
      citations: [{ document_id: "Employee_Handbook_v2.1.pdf" }, { document_id: "HR_Benefits_Update_Memo.docx" }]
    };
  } else if (lowerQ.includes('architecture') || lowerQ.includes('tech') || lowerQ.includes('stack')) {
    return {
      answer: "The platform's architecture is built on a microservices model. The backend utilizes Python and FastAPI, deployed via Kubernetes. The frontend is a React application built with Vite, TypeScript, and Tailwind CSS. Data is stored in PostgreSQL, with Redis for caching and Elasticsearch for document retrieval.",
      confidence: { score: 0.91 },
      routing: { route_type: "engineering_wiki" },
      access_summary: { authorised_chunks: 8, denied_chunks: 0 },
      citations: [{ document_id: "Architecture_Overview_v3.md" }, { document_id: "Tech_Stack_Proposal.pdf" }]
    };
  }

  return {
    answer: `Here is a synthesized response for your query: "${q}".\n\nThe platform has retrieved relevant information from your enterprise data sources. It utilizes a hybrid search approach combining dense vector embeddings and keyword matching to find the most accurate context before synthesizing this response using the configured LLM.`,
    confidence: { score: 0.85 },
    routing: { route_type: "general_knowledge_rag" },
    access_summary: { authorised_chunks: 4, denied_chunks: 1 },
    citations: [{ document_id: "Enterprise_Knowledge_Base.md" }]
  };
}

export const QueryForm = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QueryResult | null>(null);

  // Use env var or default to the hosted api URL if public
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const executeSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;

    setLoading(true);
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
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      setResult(getMockResponse(searchQuery));
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    executeSearch(query);
  };

  return (
    <div className="w-full h-full flex flex-col p-4 opacity-100 bg-[#0A0A0A] rounded-2xl relative">
      {/* Header */}
      <div className="flex flex-col gap-3 mb-4 border-b border-white/5 pb-4">
        <div className="flex items-center gap-2">
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

        {/* Informational Banner */}
        <div className="flex items-start gap-2 bg-blue-500/5 border border-blue-500/10 rounded-lg p-3 text-xs text-blue-200/70">
          <ShieldCheck className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
          <p className="leading-relaxed">
            <strong>Why a backend?</strong> Unlike simple client-side tools, EnterpriseIQ runs a heavy enterprise RAG pipeline. It requires secure backend infrastructure to host gigabyte-sized vector databases, machine learning embedding models, and strict RBAC enforcement components that cannot safely or performantly run in a web browser. This playground connects to a simulated/live backend to demonstrate the experience.
          </p>
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
            className="text-xs px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-white/70 hover:bg-white/10 hover:text-white transition-colors"
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
              className="space-y-4"
            >
              <div className="h-24 w-full bg-white/5 rounded-xl border border-white/5 animate-pulse" />
              <div className="h-12 w-3/4 bg-white/5 rounded-xl border border-white/5 animate-pulse" />
              <div className="h-12 w-full bg-white/5 rounded-xl border border-white/5 animate-pulse" />
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
              <div className="bg-white/[0.02] border border-white/10 rounded-xl p-6">
                <h3 className="text-sm font-semibold text-white/70 uppercase tracking-wider mb-3 flex items-center gap-2">
                  <Check className="w-4 h-4 text-green-400" />
                  Synthesized Answer
                </h3>
                <p className="text-white text-base leading-relaxed whitespace-pre-wrap">{result.answer}</p>
                <div className="mt-4 flex items-center gap-4 text-xs font-mono text-muted-foreground">
                  <span className="flex items-center gap-1.5"><div className={`w-2 h-2 rounded-full ${result.confidence?.score > 0.8 ? 'bg-green-400' : 'bg-yellow-400'}`} /> Confidence: {((result.confidence?.score || 0) * 100).toFixed(0)}%</span>
                  <span>Route: {result.routing?.route_type || 'Unknown'}</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
              </div>

            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};
