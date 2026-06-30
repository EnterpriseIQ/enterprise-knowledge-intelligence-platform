import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Loader2, ShieldCheck, ShieldAlert, FileText, Check } from 'lucide-react';
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

export const QueryForm = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QueryResult | null>(null);

  // Use env var or default to the hosted api URL if public
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
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
      </div>

      {/* Search Input */}
      <form onSubmit={handleSubmit} className="relative mb-6">
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

      {/* Results Area */}
      <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent pr-2 space-y-4">
        <AnimatePresence mode="wait">
          {!result && !loading && (
             <motion.div
               initial={{ opacity: 0 }}
               animate={{ opacity: 1 }}
               exit={{ opacity: 0 }}
               className="h-full flex flex-col items-center justify-center text-muted-foreground gap-4"
             >
               <div className="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center border border-white/10">
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
