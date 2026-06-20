import { motion } from 'framer-motion';
import { ArrowRight, Terminal } from 'lucide-react';

const pipelineSteps = [
  { name: "Ingestion", desc: "PDF / SQL / CSV / JSON" },
  { name: "Chunking", desc: "Semantic splitting" },
  { name: "Embedding", desc: "all-MiniLM-L6-v2" },
  { name: "Vector Store", desc: "ChromaDB + BM25" },
  { name: "Hybrid Retrieval", desc: "Dense + Sparse Fusion" },
  { name: "RBAC", desc: "Clearance + ACL Check" },
  { name: "Assembly", desc: "Context formatting" },
  { name: "Generation", desc: "Extractive Grounding" },
];

export const Architecture = () => {
  return (
    <section className="py-24 bg-background relative overflow-hidden border-t border-white/5" id="architecture">
      <div className="absolute left-1/2 top-0 -translate-x-1/2 w-full max-w-3xl h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent" />

      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-5xl font-semibold tracking-tight mb-4"
          >
            A transparent, offline-first pipeline.
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-lg text-muted-foreground max-w-2xl mx-auto"
          >
            Kortex is built on a methodical 8-step architecture. Data flows through a verifiable path, ensuring security and exact citations before an LLM is ever invoked.
          </motion.p>
        </div>

        <div className="relative py-12">
          {/* Connecting line */}
          <div className="hidden md:block absolute top-1/2 left-[5%] right-[5%] h-px bg-white/10 -translate-y-1/2 z-0" />

          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4 relative z-10">
            {pipelineSteps.map((step, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-100px" }}
                transition={{ delay: i * 0.1 }}
                className="flex flex-col items-center group cursor-default"
              >
                <div className="w-12 h-12 rounded-full glass flex items-center justify-center mb-4 border-white/20 group-hover:border-white/50 group-hover:bg-white/10 transition-all relative">
                  <span className="text-sm font-mono">{i + 1}</span>
                  {i < pipelineSteps.length - 1 && (
                    <ArrowRight className="absolute -right-6 md:hidden w-4 h-4 text-white/20" />
                  )}
                </div>
                <h4 className="text-sm font-semibold text-white mb-1 text-center">{step.name}</h4>
                <p className="text-xs text-muted-foreground text-center max-w-[100px]">{step.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-16 glass-card rounded-2xl p-8 max-w-3xl mx-auto border-white/10 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 p-4 opacity-10">
             <Terminal className="w-32 h-32" />
          </div>
          <h3 className="text-xl font-semibold mb-2">Graceful Degradation Built-In</h3>
          <p className="text-muted-foreground mb-4">
            If HuggingFace models or ChromaDB become unavailable, Kortex automatically falls back to deterministic hashing and in-memory stores. It always runs. No internet connection required.
          </p>
          <div className="bg-black/50 rounded-lg p-4 font-mono text-sm border border-white/5">
            <span className="text-muted-foreground">$</span> curl -s localhost:8000/health<br/>
            <span className="text-green-400">{"{"}</span><br/>
            <span className="text-blue-400">  "status"</span>: <span className="text-yellow-300">"healthy"</span>,<br/>
            <span className="text-blue-400">  "vector_store"</span>: <span className="text-yellow-300">"chroma"</span>,<br/>
            <span className="text-blue-400">  "embedder"</span>: <span className="text-yellow-300">"sentence-transformers"</span><br/>
            <span className="text-green-400">{"}"}</span>
          </div>
        </motion.div>
      </div>
    </section>
  );
};