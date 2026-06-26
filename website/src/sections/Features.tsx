
import { motion } from 'framer-motion';
import { Database, Search, Shield, Zap, Workflow, Cpu } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription } from '../components/ui/card';

export function Features() {
  const features = [
    {
      icon: Search,
      title: "Hybrid Search Architecture",
      desc: "Combines dense vectors (embeddings) with sparse keyword search (BM25) for unparalleled retrieval precision."
    },
    {
      icon: Shield,
      title: "Identity-Aware Retrieval",
      desc: "Deep integration with your IdP ensures granular RBAC filtering happens before LLM generation."
    },
    {
      icon: Workflow,
      title: "Agentic Workflows",
      desc: "LangGraph-powered multi-agent orchestration for complex multi-step reasoning and tool use."
    },
    {
      icon: Database,
      title: "Universal Connectors",
      desc: "Native integrations for structured (Postgres, Snowflake) and unstructured (Confluence, Notion) data."
    },
    {
      icon: Cpu,
      title: "Local LLM Support",
      desc: "Run completely offline with local models (Qwen, Llama 3) for highly sensitive air-gapped environments."
    },
    {
      icon: Zap,
      title: "Cross-Encoder Reranking",
      desc: "Second-stage reranking model instantly surfaces the most contextually relevant chunks."
    }
  ];

  return (
    <section id="features" className="py-24 relative overflow-hidden">
      <div className="container px-4 mx-auto">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-5xl font-bold tracking-tight mb-4"
          >
            Engineering Excellence, <br/><span className="text-muted-foreground">Built-In.</span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-lg text-muted-foreground"
          >
            A comprehensive suite of tools designed for production-grade enterprise intelligence.
          </motion.p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -5 }}
            >
              <Card className="h-full bg-card/50 backdrop-blur-sm border-border/50 hover:border-primary/50 transition-colors cursor-default group overflow-hidden relative">
                <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                <CardHeader>
                  <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                    <feature.icon className="w-6 h-6 text-primary" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                  <CardDescription className="text-base mt-2 leading-relaxed">
                    {feature.desc}
                  </CardDescription>
                </CardHeader>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
