
import { motion } from 'framer-motion';
import { ArrowRight, Terminal } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';

export function Hero() {
  return (
    <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden flex flex-col items-center justify-center min-h-[90vh]">
      <div className="container px-4 md:px-6 flex flex-col items-center text-center z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="mt-8 mb-6"
        >
          <Badge variant="secondary" className="rounded-full px-4 py-1 border border-border/50 bg-secondary/50 backdrop-blur-sm shadow-sm">
            <span className="flex h-2 w-2 rounded-full bg-primary mr-2 animate-pulse"></span>
            EnterpriseIQ 2.0 is now available
          </Badge>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1, ease: "easeOut" }}
          className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight max-w-4xl bg-clip-text text-transparent bg-gradient-to-b from-foreground to-foreground/90"
        >
          The Enterprise Knowledge Intelligence Platform
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2, ease: "easeOut" }}
          className="mt-6 text-xl tracking-tight text-muted-foreground max-w-2xl leading-relaxed"
        >
          Securely search, analyze, and automate your enterprise structured and unstructured data with agentic RAG and hybrid retrieval.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3, ease: "easeOut" }}
          className="mt-10 flex flex-col sm:flex-row gap-4 w-full sm:w-auto"
        >
          <Button size="lg" className="gap-2 rounded-full h-12 px-8 text-base shadow-[0_0_20px_rgba(255,255,255,0.1)] hover:shadow-[0_0_30px_rgba(255,255,255,0.2)] transition-shadow">
            Start Building
            <ArrowRight className="w-4 h-4" />
          </Button>
          <Button size="lg" variant="outline" className="gap-2 rounded-full h-12 px-8 text-base bg-background/50 backdrop-blur-sm">
            <Terminal className="w-4 h-4" />
            Read the Docs
          </Button>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.7, delay: 0.5, ease: "easeOut" }}
          className="mt-20 w-full max-w-5xl relative rounded-xl border border-border bg-card/50 backdrop-blur-xl shadow-2xl overflow-hidden"
        >
          <div className="absolute top-0 left-0 w-full h-12 border-b border-border bg-muted/50 flex items-center px-4 gap-2">
            <div className="flex gap-1.5">
              <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
            </div>
            <div className="mx-auto text-xs text-muted-foreground font-mono bg-background/50 px-3 py-1 rounded-md border border-border/50">
              agent.execute(query="Analyze Q3 earnings")
            </div>
          </div>
          <div className="p-6 pt-16 h-[400px] flex items-center justify-center text-muted-foreground font-mono text-sm bg-gradient-to-b from-transparent to-background/50">
            <div className="text-left w-full max-w-2xl space-y-4">
              <p className="text-primary/70">$ Initialize EnterpriseIq...</p>
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1, duration: 0.5 }}
                className="text-green-400"
              >
                ✓ Connected to structured data sources (Postgres, Snowflake)
              </motion.p>
              <motion.p
                 initial={{ opacity: 0 }}
                 animate={{ opacity: 1 }}
                 transition={{ delay: 1.5, duration: 0.5 }}
                 className="text-green-400"
              >
                ✓ Connected to unstructured data sources (Confluence, Jira)
              </motion.p>
               <motion.p
                 initial={{ opacity: 0 }}
                 animate={{ opacity: 1 }}
                 transition={{ delay: 2, duration: 0.5 }}
                 className="text-blue-400"
              >
                &gt; Executing Agentic RAG Pipeline...
              </motion.p>
              <motion.div
                 initial={{ opacity: 0 }}
                 animate={{ opacity: 1 }}
                 transition={{ delay: 2.5, duration: 0.5 }}
                 className="pl-4 border-l-2 border-border/50 text-foreground"
              >
                Found 14 relevant documents. Reranking with Cross-Encoder...<br/>
                Generating synthesized response with strict RBAC filtering.
              </motion.div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
