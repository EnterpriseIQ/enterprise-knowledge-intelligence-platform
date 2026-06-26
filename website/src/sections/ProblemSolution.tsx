
import { motion } from 'framer-motion';
import { SearchX, Lock, Zap, CheckCircle2, Shield, BrainCircuit } from 'lucide-react';
import { Card,   } from '../components/ui/card';

export function ProblemSolution() {
  const problems = [
    { icon: SearchX, title: "Siloed Knowledge", desc: "Data is scattered across structured databases and unstructured wikis, making unified search impossible." },
    { icon: Lock, title: "Security Risks", desc: "Traditional RAG pipelines leak sensitive data by ignoring granular role-based access controls." },
    { icon: Zap, title: "Inefficient Retrieval", desc: "Basic vector search returns irrelevant context, causing LLM hallucinations and degraded performance." }
  ];

  const solutions = [
    { icon: BrainCircuit, title: "Hybrid Agentic RAG", desc: "Combines dense vector search with sparse BM25 and Cross-Encoder reranking for pinpoint accuracy." },
    { icon: Shield, title: "Strict RBAC Pipeline", desc: "Identity-aware retrieval ensures users only see data they are explicitly authorized to access." },
    { icon: CheckCircle2, title: "Unified Interface", desc: "A single, highly performant API to query across Postgres, Snowflake, Jira, and Confluence." }
  ];

  return (
    <section className="py-24 md:py-32 relative">
      <div className="container px-4 mx-auto">
        <div className="grid lg:grid-cols-2 gap-16 md:gap-24 items-center">

          {/* Problem Side */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight mb-4">The Enterprise AI Dilemma</h2>
            <p className="text-lg text-muted-foreground mb-8">Building reliable AI for the enterprise is hard. Out-of-the-box solutions fail at scale, security, and precision.</p>

            <div className="space-y-6">
              {problems.map((item, i) => (
                <div key={i} className="flex gap-4 p-4 rounded-xl border border-destructive/20 bg-destructive/5">
                  <div className="mt-1 bg-destructive/20 p-2 rounded-lg text-destructive h-fit">
                    <item.icon className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">{item.title}</h3>
                    <p className="text-muted-foreground text-sm mt-1">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Solution Side */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="relative"
          >
            <div className="absolute inset-0 bg-primary/5 rounded-[2rem] -rotate-3 scale-105 blur-xl -z-10"></div>
            <Card className="border-primary/20 bg-card/80 backdrop-blur-xl shadow-2xl p-8 rounded-[2rem]">
              <h2 className="text-2xl md:text-3xl font-bold tracking-tight mb-8 bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary/60">The KnowledgeX Standard</h2>

              <div className="space-y-6">
                {solutions.map((item, i) => (
                  <div key={i} className="flex gap-4">
                    <div className="mt-1 bg-primary/20 p-2 rounded-lg text-primary h-fit">
                      <item.icon className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-foreground">{item.title}</h3>
                      <p className="text-muted-foreground text-sm mt-1">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </motion.div>

        </div>
      </div>
    </section>
  );
}
