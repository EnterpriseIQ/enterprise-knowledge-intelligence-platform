import { motion } from 'framer-motion';
import { Search, ShieldCheck, Link, Database, WifiOff, Route, List, Terminal } from 'lucide-react';

const features = [
  {
    icon: <Search className="w-5 h-5" />,
    title: "Hybrid Retrieval Engine",
    description: "Min-max fused dense vectors and BM25 sparse search finds exact matches alongside semantic intent.",
    className: "md:col-span-2 md:row-span-2",
  },
  {
    icon: <ShieldCheck className="w-5 h-5" />,
    title: "Defence-in-Depth RBAC",
    description: "Document-level access control enforced before and after retrieval.",
    className: "md:col-span-1",
  },
  {
    icon: <Link className="w-5 h-5" />,
    title: "Verifiable Citations",
    description: "Every generated answer includes exact document and snippet links.",
    className: "md:col-span-1",
  },
  {
    icon: <Database className="w-5 h-5" />,
    title: "Universal Ingestion",
    description: "Unified processing for PDFs, CSVs, SQL, and JSON logs into a single graph.",
    className: "md:col-span-2",
  },
  {
    icon: <WifiOff className="w-5 h-5" />,
    title: "Offline-First Resilience",
    description: "Runs entirely offline with graceful fallbacks. Zero cloud APIs required.",
    className: "md:col-span-1",
  },
  {
    icon: <Route className="w-5 h-5" />,
    title: "Intent Routing",
    description: "Transparent classifier boosts relevant departments automatically.",
    className: "md:col-span-1",
  },
  {
    icon: <List className="w-5 h-5" />,
    title: "Comprehensive Audit",
    description: "Every access decision and generation is logged and explainable.",
    className: "md:col-span-1",
  },
  {
    icon: <Terminal className="w-5 h-5" />,
    title: "Developer-Ready",
    description: "Deploys instantly via Docker, with a typed FastAPI backend.",
    className: "md:col-span-1",
  }
];

export const Features = () => {
  return (
    <section className="py-24 bg-background" id="features">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-5xl font-semibold tracking-tight mb-4"
          >
            Engineered for absolute trust.
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-lg text-muted-foreground max-w-2xl mx-auto"
          >
            A cohesive platform bridging state-of-the-art retrieval with enterprise-grade governance.
          </motion.p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 auto-rows-[200px] gap-4">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className={`glass-card p-6 rounded-2xl flex flex-col justify-between group overflow-hidden relative ${feature.className}`}
            >
              <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative z-10">
                <div className="mb-4 bg-white/5 w-10 h-10 rounded-lg flex items-center justify-center text-white/80 group-hover:text-white transition-colors border border-white/10 group-hover:border-white/20">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};