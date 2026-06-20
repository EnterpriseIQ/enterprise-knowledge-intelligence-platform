import { motion } from 'framer-motion';
import { ArrowRight, ChevronRight, Terminal } from 'lucide-react';
import { Button } from '../components/Button';

export const Hero = () => {
  return (
    <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-hero-glow opacity-[0.15] blur-[100px] rounded-full pointer-events-none" />

      <div className="max-w-7xl mx-auto px-6 relative z-10 flex flex-col items-center text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-sm mb-8 hover:bg-white/10 transition-colors cursor-pointer"
        >
          <span className="flex h-2 w-2 rounded-full bg-success"></span>
          Introducing Kortex 1.0 — The zero-leak enterprise RAG platform
          <ArrowRight className="w-4 h-4 ml-1 text-muted-foreground" />
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-5xl md:text-7xl font-semibold tracking-tight max-w-4xl mb-6 leading-[1.1]"
        >
          Intelligence you can trust.<br className="hidden md:block" /> Access you can control.
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-10"
        >
          Unify your fragmented PDFs, databases, and logs into a single, intelligent graph.
          Kortex enforces strict role-based access control inside the retrieval engine, delivering perfectly cited answers with zero hallucinations.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex flex-col sm:flex-row gap-4"
        >
          <Button size="lg" className="group">
            View Documentation
            <ChevronRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
          </Button>
          <Button size="lg" variant="secondary">
            Request Enterprise Demo
          </Button>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.5 }}
          className="w-full max-w-4xl mt-20 relative"
        >
          <div className="absolute inset-0 bg-gradient-to-t from-background to-transparent z-10 bottom-[-1px] pointer-events-none" />
          <div className="rounded-xl border border-white/10 bg-black/50 backdrop-blur-xl overflow-hidden shadow-2xl">
            <div className="flex items-center px-4 py-3 border-b border-white/10 bg-white/5">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500/80" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                <div className="w-3 h-3 rounded-full bg-green-500/80" />
              </div>
              <div className="mx-auto text-xs text-muted-foreground font-mono flex items-center gap-2">
                <Terminal className="w-3 h-3" /> kortex-cli
              </div>
            </div>
            <div className="p-6 font-mono text-sm text-left">
              <div className="text-muted-foreground mb-2">$ kortex query "Show finance budget allocations" --role Finance</div>
              <div className="text-green-400 mb-4">&gt; Authenticated as Finance. Clearance: confidential.</div>
              <div className="text-white mb-2 leading-relaxed">
                The Q3 budget allocation for the engineering department is $4.2M <span className="text-blue-400 cursor-pointer hover:underline">[1]</span>, primarily allocated to cloud infrastructure and new hires <span className="text-blue-400 cursor-pointer hover:underline">[2]</span>.
              </div>
              <div className="mt-6 pt-4 border-t border-white/10">
                <div className="text-xs text-muted-foreground mb-1">CITATIONS</div>
                <div className="text-xs text-muted-foreground hover:text-white transition-colors cursor-pointer">[1] FIN-2023-Q3-Budget.pdf (Page 4, Snippet: "Engineering allocation totals $4.2M...")</div>
                <div className="text-xs text-muted-foreground hover:text-white transition-colors cursor-pointer">[2] FIN-2023-Q3-Budget.pdf (Page 5, Snippet: "Breakdown: 60% cloud, 40% headcount...")</div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};