import { motion } from 'framer-motion';

export const Roadmap = () => {
  const roadmapItems = [
    {
      quarter: "Q1 2024",
      status: "Released",
      title: "Core RAG Engine",
      features: ["Vector Search", "Basic Access Control", "PDF & Text Extraction"]
    },
    {
      quarter: "Q2 2024",
      status: "Released",
      title: "Enterprise Graph",
      features: ["Agentic Routing", "Cross-Encoder Reranking", "SQL Database Integration"]
    },
    {
      quarter: "Q3 2024",
      status: "Current",
      title: "Advanced Security",
      features: ["Zero-Leak Policies", "Granular RBAC", "SOC2 Compliance Tracking"]
    },
    {
      quarter: "Q4 2024",
      status: "Planned",
      title: "Predictive Intelligence",
      features: ["Predictive Analytics", "Automated Workflows", "Custom Model Fine-tuning"]
    }
  ];

  return (
    <section className="py-24 bg-background relative border-t border-white/5" id="roadmap">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-5xl font-semibold tracking-tight mb-4"
          >
            Product Roadmap
          </motion.h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Our vision for the future of enterprise knowledge intelligence.
          </p>
        </div>

        <div className="grid md:grid-cols-4 gap-6">
          {roadmapItems.map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className={`glass-card p-6 rounded-2xl border ${item.status === 'Current' ? 'border-purple-500/50 bg-purple-500/5' : 'border-white/5'} relative`}
            >
              <div className="flex justify-between items-center mb-4">
                <span className="font-mono text-sm text-muted-foreground">{item.quarter}</span>
                <span className={`text-xs px-2 py-1 rounded-full ${
                  item.status === 'Released' ? 'bg-green-500/20 text-green-400' :
                  item.status === 'Current' ? 'bg-purple-500/20 text-purple-400' :
                  'bg-white/10 text-white/60'
                }`}>
                  {item.status}
                </span>
              </div>
              <h3 className="text-xl font-semibold mb-4">{item.title}</h3>
              <ul className="space-y-2">
                {item.features.map((feature, j) => (
                  <li key={j} className="flex items-start gap-2 text-sm text-muted-foreground">
                    <span className="text-purple-500 mt-0.5">•</span>
                    {feature}
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};
